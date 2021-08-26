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
        status, ctype, content = await util.get_item(
                url, logger, config.enable_tls)
        if status != httpcode.HTTP_200_OK:
            raise HTTPException(status_code=httpcode.HTTP_404_NOT_FOUND,
                                detail=f"invalid xpath")
        if ctype != "application/json":
            raise HTTPException(
                    status_code=httpcode.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"invalid content-type (system)")
        logger.debug(f"RET: data={content}")
        return content

    def validate_token(
            token: str,
            xpath: Optional[str] = None,
            remove_token: bool = True,
            check_authed: bool = False,
            ) -> None:
        """
        validate token and raise an exception if not valid.
        """
        if not xtmap.validate_token(token, xpath, remove_token, check_authed):
            logger.error(f"Not acceptable token: token={token} xpath={xpath}")
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"invalid token")

    async def validate_token_and_get_item(
            token: str,
            xpath: str,
            remove_token: bool = True,
            check_authed: bool = False,
            ) -> dict:
        """
        validation of token and xpath.
        raise an exception if token is not valid.
        and raise an exception if xpath is passed and xpath doesn't exist.
        """
        logger.debug(f"validate token: {token}")
        # raise an exception if token is not valid.
        validate_token(token, xpath, remove_token, check_authed)
        return await get_item_by_xpath(xpath)

    @app.get(
        "/2/x/{xpath}",
        response_description="Get an authentication page for STEP2.",
        response_class=HTMLResponse,
        status_code=httpcode.HTTP_200_OK,
    )
    async def get_step2_by_xpath(xpath: str, em: str = None):
        logger.debug(f"APP get_step2_by_xpath: {xpath}")
        content = await get_item_by_xpath(xpath)
        token = xtmap.generate_token(content["xpath"])
        # read file and embed token.
        html_content = None
        async with aiofile.async_open(f"{config.ui_step2_path}/index.html",
                                      "r") as fd:
            html_content = await fd.read()
        # make the content.
        content = html_content.replace("__HKD_TOKEN__", token, 1)
        if em is not None:
            content = content.replace("__HKD_GIVEN_EM__", em, 1)
        if config.google_apikey:
            content = content.replace("__HKD_GKEY__", config.google_apikey, 1)
        return HTMLResponse(content)

    @app.post(
        "/a",
        response_description="Authenticate the request for STEP2.",
        response_model=PenRESTStep2Model,
        status_code=httpcode.HTTP_200_OK,
    )
    async def auth_access(in_data: PenRESTStep2AuthReqModel = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        in_json = jsonable_encoder(in_data)
        logger.debug(f"APP auth_access: {in_json}")
        xpath = in_json["xpath"]
        content = await validate_token_and_get_item(x_csrf_token, xpath,
                                                    remove_token=False)
        # check if the key contents were valid.
        if not (content["emailAddr"] == in_data.emailAddr and
                content["authcode"] == in_data.authcode):
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"invalid authcode")
        # set authed flag to the token.
        xtmap.token_set_authed(x_csrf_token)
        # remove hidden fields from the response.
        for k in HIDDEN_FIELDS:
            k in content and content.pop(k)
        return content

    @app.post(
        "/2",
        response_description="Update an item as STEP2.",
        #response_model=PenRESTStep2Model,
        status_code=httpcode.HTTP_200_OK,
    )
    async def post_step2(in_data: PenRESTStep2Model = Body(...),
                        x_csrf_token: Optional[str] = Header(None)):
        in_json = jsonable_encoder(in_data)
        logger.debug(f"APP post_step2: {in_json}")
        xpath = in_json["xpath"]
        # check and remove token
        old_json = await validate_token_and_get_item(x_csrf_token, xpath,
                                                     remove_token=False,
                                                     check_authed=True)
        # fix the hidden fields to submit.
        for k in HIDDEN_FIELDS:
            if k in old_json:
                in_json[k] = old_json[k]
        # update special fields.
        # if tsStep2 doesn't exist or its value is None,
        # it's first time to update this step2 item.
        # otherwise, update tsUpdate.
        if old_json.get("tsStep2") is None:
            in_json["tsStep2"] = util.get_timestamp(config.tz)
        else:
            in_json["tsStep2"] = old_json["tsStep2"]
            in_json["tsUpdate"] = util.get_timestamp(config.tz)
        # tiny check
        PenDBStep2Model.parse_obj(in_json)
        # submitting
        logger.debug(f"POST DB: trying: {in_json}")
        url = f"{config.db_api_url}/2"
        status, content = await util.post_item(url, in_json,
                                               enable_tls=config.enable_tls)
        if status == httpcode.HTTP_200_OK:
            # just return in_data as it is.
            return
        else:
            raise HTTPException(status_code=httpcode.HTTP_406_NOT_ACCEPTABLE,
                                detail="invalid data submitted")

    from fastapi.staticfiles import StaticFiles
    app.mount("/2", StaticFiles(directory=config.ui_step2_path, html=True), name="step2ui")

    return app
