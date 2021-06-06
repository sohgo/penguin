from fastapi import FastAPI, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from typing import Optional, List, Union
from modelMM import PenMMRESTRequestModel, PenMMRESTStatusModel
import dateutil.parser
import asyncio
from mmworker import SendMessage

def api(config):

    logger = config.logger

    config.queue =  asyncio.Queue(maxsize=config.max_queue_size)
    config.queue._loop = config.loop    # XXX good way ?
    # create sendmsg object.
    sendmsg = SendMessage(config)
    # start sendmsg worker.
    config.loop.create_task(sendmsg.worker())

    app = FastAPI()

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

    #
    # API
    #
    @app.post(
        "/m",
        response_description="Post new request.",
        status_code=status.HTTP_200_OK,
        response_class=JSONResponse,
        )
    async def post_request(in_data: PenMMRESTRequestModel = Body(...)):
        logger.debug(f"APP POST REQ: {in_data}")
        ret = await sendmsg.request(in_data)
        if ret == True:
            return {"status":"OK"}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"message queue is full")

    @app.get(
        "/s",
        response_description="Get status.",
        status_code=status.HTTP_200_OK,
        response_model=PenMMRESTStatusModel,
        )
    async def get_entry_by_xpath(xpath: str):
        logger.debug(f"APP GET STATUS:")
        if True:
            pass
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"not found status")

    #
    return app

