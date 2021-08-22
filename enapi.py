from fastapi import FastAPI, Header, Body, Request, HTTPException
from fastapi import status as httpcode
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from typing import Optional, List
from modelStep1 import PenRESTStep1Model, PenRESTStep1AckModel
from modelStep2 import PenRESTStep2AuthReqModel, PenRESTStep2Model
from modelDB import PenDBStep1Model, PenDBStep2Model, HIDDEN_FIELDS
from modelMM import PenMMRESTRequestModel
import asyncio
import aiofile
import util
from random import randint
from xtoken_map import XTokenMap
import codeNwords

STEP1_INDEX_FILE = "ui/step1/dist/index.html"

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

    def validate_token(
            token: str,
            xpath: Optional[str] = None,
            remove_token: bool = True,
            ) -> None:
        """
        validate token and raise an exception if not valid.
        """
        if not xtmap.validate_token(token, xpath, remove_token):
            logger.error(f"Not acceptable token: token={token} xpath={xpath}")
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"invalid token.")

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
        # generate auth code.
        in_json["authcode"] = "-".join([str(randint(1000,9999))
                                        for i in range(3)])
        # tiny check
        PenDBStep1Model.parse_obj(in_json)
        # submitting
        logger.debug(f"POST DB: trying: {in_json}")
        url = f"{config.db_api_url}/1"
        status, content = await util.post_item(url, in_json,
                                               enable_tls=config.enable_tls)
        if status != httpcode.HTTP_201_CREATED:
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"invalid data submitted.")
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
        out_json = jsonable_encoder(in_data)
        out_json["xpath"] = in_json["xpath"]
        if config.fe_api_url:
            out_json["redirectHost"] = config.fe_api_url
        return out_json

    from fastapi.responses import Response
    @app.get("/1/favicon.ico")
    async def read_file():
        async with aiofile.async_open("./ui/favicon.ico", "rb") as fd:
            content = await fd.read()
        return Response(content=content, media_type="image/vnd.microsoft.icon")

    from fastapi.staticfiles import StaticFiles
    app.mount("/1", StaticFiles(directory="./ui/step1/dist", html=True), name="step1ui")

    return app
