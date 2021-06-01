from fastapi import FastAPI, Header, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from typing import Optional, List
from modelREST import PenRESTStep1Model, PenRESTStep1AckModel
from modelREST import PenRESTStep2AuthModel, PenRESTStep2Model
import aiohttp
import aiofile
import util
from xtoken_map import XTokenMap

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

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        content = jsonable_encoder(exc.errors())
        logger.error(f"Model Validation Error: {content}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": content},
        )

    async def get_item_by_xpath(xpath: str):
        """
        get item by xpath.
        raise an exception if any item doesn't exist.
        """
        logger.debug(f"get_item_by_xpath: {xpath}")
        url = f"{config.be_api_url}/a/xpath/{xpath}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=config.enable_tls) as response:
                content = await response.json()
                logger.debug(f"RET: status={response.status} data={content}")
                if response.status != status.HTTP_200_OK:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"xpath not found: {xpath}")
        return content

    def validate_token(token, xpath=None):
        if not xtmap.validate_token(token, xpath):
            logger.error(f"Not acceptable token: token={token} xpath={xpath}")
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"token not acceptable")

    async def validate_token_and_get_item(token, xpath):
        """
        validation of token and xpath.
        raise an exception if token is not valid.
        and raise an exception if xpath is passed and xpath doesn't exist.
        """
        logger.debug(f"validate token: {token}")
        validate_token(token, xpath)
        if xpath is None:
            return True
        else:
            return await get_item_by_xpath(xpath)


    async def post_item(url: str, in_json: dict, out_json: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=in_json,
                                    ssl=config.enable_tls) as response:
                content = await response.json()
                logger.debug(f"RET: status={response.status} content={content}")
                # copy in_data again to avoid leaking internal field.
                if response.status != status.HTTP_201_CREATED:
                    raise HTTPException(status_code=response.status,
                                        detail=out_json)

    #
    # API
    #
    @app.get(
        "/1",
        response_description="Get a page for STEP1.",
        response_class=HTMLResponse,
        status_code=status.HTTP_200_OK,
    )
    async def get_step1(request: Request):
        logger.debug(f"APP get_step1")
        token = xtmap.generate_token()
        # read file and embed token.
        html_content = None
        async with aiofile.async_open(STEP1_INDEX_FILE, "r") as fd:
            html_content = await fd.read()
        return HTMLResponse(content=html_content.replace("__HKD_TOKEN__",token))

    @app.post(
        "/1",
        response_description="Add new item as STEP1.",
        status_code=status.HTTP_201_CREATED,
        response_model=PenRESTStep1AckModel,
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
        logger.debug(f"POST: trying: {in_json}")
        url = f"{config.be_api_url}/1"
        out_json = jsonable_encoder(in_data)
        content = await post_item(url, in_json, out_json)
        # submit a request to the reporter for sending a mail out.
        # creating QR code.
        out_json["xpath"] = in_json["xpath"]
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=out_json)

    @app.get(
        "/2/x/{xpath}",
        response_description="Get an authentication page for STEP2.",
        response_class=HTMLResponse,
        status_code=status.HTTP_200_OK,
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
        status_code=status.HTTP_200_OK,
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
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"not acceptable")
        # remove and add fields the response according to the model.
        for k in [ "pid", "tsStep1", "tsStep2", "tsUpdated" ]:
            k in content and content.pop(k)
        return content

    @app.post(
        "/2",
        response_description="Update an item as STEP2.",
        response_model=PenRESTStep2Model,
        status_code=status.HTTP_200_OK,
    )
    async def post_step2(in_data: PenRESTStep2Model = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        in_json = jsonable_encoder(in_data)
        logger.debug(f"APP post_step2: {in_json}")
        xpath = in_json["xpath"]
        content = await validate_token_and_get_item(x_csrf_token, xpath)
        # fix the data to submit.
        in_json["pid"] = content["pid"]
        in_json["tsStep1"] = content["tsStep1"]
        if not content.get("tsStep2"):
            # if tsStep2 doesn't exist or its value is None,
            # it's first time to update this step2 item.
            in_json["tsStep2"] = util.get_timestamp(config.tz)
        else:
            in_json["tsStep2"] = content["tsStep2"]
            in_json["tsUpdated"] = util.get_timestamp(config.tz)
        #
        logger.debug(f"POST: trying: {in_json}")
        url = f"{config.be_api_url}/2"
        out_json = jsonable_encoder(in_data)
        content = await post_item(url, in_json, out_json)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=out_json)

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
