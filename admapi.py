from fastapi import FastAPI, Header, Body, Request, HTTPException
from fastapi import status as httpcode
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from modelAdm import PenAdmDownloadResponseModel
from modelAdm import PenAdmCopyReqModel
from modelAdm import PenAdmStatAckModel
import asyncio
import aiohttp
import util

class PenAdmStat(BaseModel):
    epoch: datetime
    #uptime: str

def api(config):

    logger = config.logger

    fastapi_kwargs = {}
    #fastapi_kwargs = dict(docs_url=None, redoc_url=None, openapi_url=None)

    app = FastAPI(**fastapi_kwargs)

    stat = PenAdmStat(epoch=datetime.now())

    # initializing house keeper
    #hk = Housekeepter.CodeWordMap("codeNwords/word_list.txt")

    # status reporter
    async def lab_copy_worker():
        while True:
            # get items from DB. /4/list
            # put items to Lab DB.
            await asyncio.sleep(config.lab_copy_interval)
            logger.info(f"COPY: nb_items=0")

    config.loop.create_task(lab_copy_worker())

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

    #
    # API
    #
    @app.get(
        "/dl/{c3w_words}",
        response_description="Download the patient data specified by 3-word-code.",
        response_model=PenAdmDownloadResponseModel,
        status_code=httpcode.HTTP_200_OK,
    )
    async def get_patient_data(request: Request, c3w_words: str):
        logger.debug(f"APP get_patient_data by c3w_words: {c3w_words}")
        logger.debug(f"Accessed: {request.client.host}")
        if (len(config.allow_ip_addrs) > 0 and
            request.client.host not in config.allow_ip_addrs):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"{request.client.host} not allowed")
        url = f"{config.db_api_url}/a/c3ww/{c3w_words}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=config.enable_tls) as response:
                logger.debug(f"RET: code={response.status} "
                             f"type={response.content_type}")
                if response.status != httpcode.HTTP_200_OK:
                    raise HTTPException(status_code=httpcode.HTTP_404_NOT_FOUND,
                                    detail=f"c3w_words not found: {c3w_words}")
                if response.content_type != "application/json":
                    raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"invalid content-type (system)")
                content = await response.json()
        # update tsStep3 and post DB
        in_json = {
                "pid": content["pid"],
                "tsStep3": util.get_timestamp(config.tz)
                }
        logger.debug(f"POST DB: trying: {in_json}")
        url = f"{config.db_api_url}/3"
        status, content = await util.post_item(url, in_json,
                                               enable_tls=config.enable_tls)
        if status != httpcode.HTTP_200_OK:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"failed to update tsStep3 for {c3w_words}")
        return content

    @app.get(
        "/stat",
        response_description="Get the stat.",
        response_model=PenAdmStatAckModel,
        status_code=httpcode.HTTP_200_OK
        )
    async def get_stat(request: Request):
        logger.debug(f"APP get_stat")
        return { "uptime": "__test__" }

    return app
