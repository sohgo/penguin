from fastapi import FastAPI, Header, Body, Request, HTTPException
from fastapi import status as httpcode
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from typing import Optional, List
from modelREST import PenRESTStep1Model, PenRESTStep1AckModel
from modelREST import PenRESTStep2AuthModel, PenRESTStep2Model
from modelMM import PenMMRESTRequestModel
import asyncio
import aiohttp
import aiofile
import util
from xtoken_map import XTokenMap
import codeNwords

STEP1_INDEX_FILE = "ui/step1/dist/index.html"
STEP2_INDEX_FILE = "ui/step2/dist/index.html"

def api(config):

    logger = config.logger

    fastapi_kwargs = {}
    #fastapi_kwargs = dict(docs_url=None, redoc_url=None, openapi_url=None)

    app = FastAPI(**fastapi_kwargs)
    app.add_middleware(
            CORSMiddleware,
            allow_origins=config.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
    )
    xtmap = XTokenMap()

    # initializing codeNwords
    cwm = codeNwords.CodeWordMap("codeNwords/word_list.txt")

    # status reporter
    async def status_reporter():
        while True:
            await asyncio.sleep(config.status_report_interval)
            logger.info(f"STATUS: nb_token={xtmap.counts()}")

    config.loop.create_task(status_reporter())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        content = jsonable_encoder(exc.errors())
        logger.error(f"Model Validation Error: {content}")
        return JSONResponse(
            status_code=httpcode.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": content},
        )

    async def get_item_by_xpath(xpath: str):
        """
        get item by xpath.
        raise an exception if any item doesn't exist.
        """
        logger.debug(f"get_item_by_xpath: {xpath}")
        url = f"{config.db_api_url}/a/xpath/{xpath}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=config.enable_tls) as response:
                content = await response.json()
                logger.debug(f"RET: code={response.status} data={content}")
                if response.status != httpcode.HTTP_200_OK:
                    raise HTTPException(status_code=httpcode.HTTP_404_NOT_FOUND,
                                        detail=f"xpath not found: {xpath}")
        return content

    def validate_token(
            token: str,
            xpath: Optional[str] = None
            ) -> None:
        """
        validate token and raise an exception if not valid.
        """
        if not xtmap.validate_token(token, xpath):
            logger.error(f"Not acceptable token: token={token} xpath={xpath}")
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"token not acceptable")

    async def validate_token_and_get_item(
            token: str,
            xpath: str
            ) -> dict:
        """
        validation of token and xpath.
        raise an exception if token is not valid.
        and raise an exception if xpath is passed and xpath doesn't exist.
        """
        logger.debug(f"validate token: {token}")
        # raise an exception if token is not valid.
        validate_token(token, xpath)
        return await get_item_by_xpath(xpath)

    #
    # API
    #
    @app.get(
        "/1",
        response_description="Get a page for STEP1.",
        response_class=HTMLResponse,
        status_code=httpcode.HTTP_200_OK,
    )
    async def get_step1(request: Request):
        logger.debug(f"APP get_step1")
        token = xtmap.generate_token()
        # read file and embed token.
        html_content = None
        async with aiofile.async_open(STEP1_INDEX_FILE, "r") as fd:
            html_content = await fd.read()
        return html_content.replace("__HKD_TOKEN__",token)

    @app.post(
        "/1",
        response_description="Add new item as STEP1.",
        response_model=PenRESTStep1AckModel,
        status_code=httpcode.HTTP_201_CREATED,
        )
    async def post_step1(in_data: PenRESTStep1Model = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        logger.debug(f"APP post_step1: token={x_csrf_token}")
        in_json = jsonable_encoder(in_data)
        validate_token(x_csrf_token)
        # post the info.
        in_json["pid"] = util.get_hash()
        in_json["tsStep1"] = util.get_timestamp(config.tz)
        in_json["xpath"] = util.get_hash()
        # 3-words-code
        c3w = cwm.gencode()
        in_json["c3w_code"] = c3w["code"]
        in_json["c3w_words"] = c3w["words"]
        # submitting
        logger.debug(f"POST DB: trying: {in_json}")
        url = f"{config.db_api_url}/1"
        out_json = jsonable_encoder(in_data)
        status, content = await util.post_item(url, in_json,
                                               enable_tls=config.enable_tls)
        if status != httpcode.HTTP_201_CREATED:
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"not acceptable")
        # submit a request to the reporter for sending a mail out.
        mm_json = jsonable_encoder(PenMMRESTRequestModel.parse_obj(in_json))
        logger.debug(f"POST MM: trying: {mm_json}")
        url = f"{config.mm_api_url}/m"
        status, content = await util.post_item(url, mm_json,
                                               enable_tls=config.enable_tls)
        if status != 200:
            raise HTTPException(status_code=httpcode.HTTP_502_BAD_GATEWAY,
                                detail=f"accepted, but error on mail.")
        # reply json
        # XXX with xpath if successful.
        # XXX 別パス認証が必要ならばここでxpathは返すべきではない。
        out_json["xpath"] = in_json["xpath"]
        return out_json

    @app.get(
        "/2/x/{xpath}",
        response_description="Get an authentication page for STEP2.",
        response_class=HTMLResponse,
        status_code=httpcode.HTTP_200_OK,
    )
    async def get_step2_by_xpath(xpath: str):
        logger.debug(f"APP get_step2_by_xpath: {xpath}")
        content = await get_item_by_xpath(xpath)
        token = xtmap.generate_token(content["xpath"])
        # read file and embed token.
        html_content = None
        async with aiofile.async_open(STEP2_INDEX_FILE, "r") as fd:
            html_content = await fd.read()
        return HTMLResponse(content=html_content.replace("__HKD_TOKEN__",token))

    @app.post(
        "/a",
        response_description="Authenticate the request for STEP2.",
        response_model=PenRESTStep2Model,
        status_code=httpcode.HTTP_200_OK,
    )
    async def auth_access(in_data: PenRESTStep2AuthModel = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        in_json = jsonable_encoder(in_data)
        logger.debug(f"APP auth_access: {in_json}")
        xpath = in_json["xpath"]
        content = await validate_token_and_get_item(x_csrf_token, xpath)
        # check if the key contents were valid.
        if not (content["birthM"] == in_data.birthM and
                content["birthD"] == in_data.birthD and
                content["favColor"] == in_data.favColor):
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"not acceptable")
        # remove and add fields the response according to the model.
        for k in [ "pid", "tsStep1", "tsStep2", "tsUpdate", "tsStep3",
                  "c3w_code", "c3w_words" ]:
            k in content and content.pop(k)
        return content

    @app.post(
        "/2",
        response_description="Update an item as STEP2.",
        response_model=PenRESTStep2Model,
        status_code=httpcode.HTTP_200_OK,
    )
    async def post_step2(in_data: PenRESTStep2Model = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        in_json = jsonable_encoder(in_data)
        logger.debug(f"APP post_step2: {in_json}")
        xpath = in_json["xpath"]
        old_json = await validate_token_and_get_item(x_csrf_token, xpath)
        # fix the hidden fields to submit.
        in_json["pid"] = old_json["pid"]
        in_json["tsStep1"] = old_json["tsStep1"]
        # if tsStep2 doesn't exist or its value is None,
        # it's first time to update this step2 item.
        # otherwise, update tsUpdate.
        if old_json.get("tsStep2") is None:
            in_json["tsStep2"] = util.get_timestamp(config.tz)
        else:
            in_json["tsStep2"] = old_json["tsStep2"]
            in_json["tsUpdate"] = util.get_timestamp(config.tz)
        # copy tsStep3, c3w_code, c3w_words if exists.
        for k in [ "tsStep3", "c3w_code", "c3w_words" ]:
            if k in old_json:
                in_json[k] = old_json[k]
        #
        logger.debug(f"POST DB: trying: {in_json}")
        url = f"{config.db_api_url}/2"
        status, content = await util.post_item(url, in_json,
                                               enable_tls=config.enable_tls)
        if status == httpcode.HTTP_201_CREATED:
            # just return in_data as it is.
            return jsonable_encoder(in_data)
        else:
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail="not acceptable")

    from fastapi.responses import Response
    @app.get("/1/favicon.ico")
    @app.get("/2/favicon.ico")
    async def read_file():
        async with aiofile.async_open("./ui/favicon.ico", "rb") as fd:
            content = await fd.read()
        return Response(content=content, media_type="image/vnd.microsoft.icon")

    from fastapi.staticfiles import StaticFiles
    app.mount("/1", StaticFiles(directory="./ui/step1/dist", html=True), name="step1ui")
    app.mount("/2", StaticFiles(directory="./ui/step2/dist", html=True), name="step2ui")

    return app
