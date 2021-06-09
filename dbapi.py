from fastapi import FastAPI, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from typing import Optional, List, Union
from modelDB import PenDBStep1Model, PenDBStep2Model, PenDBStep3UpdateModel
import dateutil.parser
import motor.motor_asyncio
from pymongo import ReturnDocument

def api(config):

    logger = config.logger

    app = FastAPI()

    x_client = motor.motor_asyncio.AsyncIOMotorClient(config.mongodb_url,
                                                      io_loop=config.loop)
    x_db = x_client[config.db_name]
    x_tab = x_db[config.table_name]

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
        "/1",
        response_description="Add new STEP1 item. TBD: xpath must be unique.",
        status_code=status.HTTP_201_CREATED,
        response_model=PenDBStep1Model,
        )
    async def post_step1(in_data: PenDBStep1Model = Body(...)):
        logger.debug(f"APP POST STEP1:")
        # See IMPLEMENTATION.md
        pid = in_data.pid
        xpath = in_data.xpath
        c3w_words = in_data.c3w_words
        result = await x_tab.count_documents({"$or":[
                {"pid":pid},
                {"xpath":xpath},
                {"c3w_words":c3w_words},
                ]})
        if result > 0:
            logger.debug(f"keys: pid={pid} xpath={xpath} c3w_words={c3w_words}")
            logger.debug(f"count: {result}")
            msg = f"POST STEP1: pid, xpath, or c3w_words already exist"
            logger.error(msg)
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"{msg}")
        # post the info.
        in_json = jsonable_encoder(in_data)
        in_json["tsStep1"] = dateutil.parser.parse(in_json["tsStep1"])
        logger.debug(f"insert_one: trying: {in_json}")
        result = await x_tab.insert_one(in_json)
        logger.debug(f"RET: id={result.inserted_id} ack={result.acknowledged} "
                    f"data={in_json}")
        # copy in_data again to avoid leaking "_id".
        out_json = jsonable_encoder(in_data)
        if result.acknowledged == True:
            return out_json
        else:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=out_json)

    @app.get(
        "/a/xpath/{xpath}",
        response_description="Get a single item by xpath.",
        status_code=status.HTTP_200_OK,
        response_model=Union[PenDBStep1Model,PenDBStep2Model]
        )
    async def get_entry_by_xpath(xpath: str):
        logger.debug(f"APP GET xpath: {xpath}")
        item = await x_tab.find_one({"xpath": xpath})
        logger.debug(f"RET: {item}")
        if item:
            item.pop("_id")
            return item
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"not found xpath:{xpath}")

    @app.get(
        "/a/c3ww/{c3w_words}",
        response_description="Get a single item by c3w_words.",
        status_code=status.HTTP_200_OK,
        response_model=PenDBStep2Model
        )
    async def get_entry_by_c3ww(c3w_words: str):
        logger.debug(f"APP GET c3w_words: {c3w_words}")
        item = await x_tab.find_one({"c3w_words": c3w_words})
        logger.debug(f"RET: {item}")
        if item:
            item.pop("_id")
            return item
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"not found c3w_words: {c3w_words}")

    @app.post(
        "/2",
        response_description="update a SPTE1 item for STEP2.",
        status_code=status.HTTP_200_OK,
        response_model=PenDBStep2Model,
        )
    async def post_step2(in_data: PenDBStep2Model = Body(...)):
        logger.debug(f"APP POST STEP2:")
        pid = in_data.pid
        # post the info.
        in_json = jsonable_encoder(in_data)
        logger.debug(f"find_one_and_replace: trying: {in_json}")
        #result = await x_tab.find_one_and_replace(
        result = await x_tab.replace_one(
                {"pid":pid},
                in_json,
                upsert=False)
        if result.modified_count == 0:
            msg = f"POST STEP2: pid doesn't exist: {pid}"
            logger.error(msg)
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"detail": msg})
        elif result.modified_count > 1:
            msg = f"POST STEP2: pid matched more than 1 items: {pid}"
            logger.error(msg)
            return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": msg})
        # copy in_data again to avoid leaking "_id".
        return jsonable_encoder(in_data)

    @app.post(
        "/3",
        response_description="Update tsStep3 for STEP3.",
        status_code=status.HTTP_200_OK,
        response_model=PenDBStep2Model,
        )
    async def post_step3(in_data: PenDBStep3UpdateModel = Body(...)):
        logger.debug(f"APP POST STEP3:")
        pid = in_data.pid
        ts_step3 = in_data.tsStep3
        # update the item.
        logger.debug(f"trying find_one_and_update: {pid}")
        result = await x_tab.find_one_and_update(
                {"pid": pid},
                {"$set": {"tsStep3": ts_step3}},
                upsert=False,
                return_document=ReturnDocument.AFTER)
        if result is None:
            msg = f"POST STEP3: pid doesn't exist: {pid}"
            logger.error(msg)
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"detail": msg})
        # copy in_data again to avoid leaking "_id".
        result.pop("_id")
        return result

    @app.get(
        "/1/list",
        response_description=f"List recent 100 items of STEP1.",
        status_code=status.HTTP_200_OK,
        response_model=List[PenDBStep1Model],
        )
    async def list_step1():
        logger.debug(f"GET STEP1 LIST")
        items = await x_tab.find(
                { "$and" : [
                        { "tsStep1": { "$ne": None } },
                        { "tsStep2": None }
                        ] }
                ).sort([("tsStep1",-1)]).limit(100).to_list(100)
        logger.debug(f"RET: count={len(items)}")
        if items:
            for i in items:
                i.pop("_id")
            return items
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"no entries")

    @app.get(
        "/2/list",
        response_description=f"List recent 100 items of STEP2.",
        status_code=status.HTTP_200_OK,
        response_model=List[PenDBStep2Model],
        )
    async def list_entry():
        logger.debug(f"GET STEP2 LIST")
        items = await x_tab.find(
                { "$and" : [
                        { "tsStep2": { "$ne": None } },
                        { "tsStep3": None }
                        ] }
                ).sort([("tsStep2",-1)]).limit(100).to_list(100)
        logger.debug(f"RET: count={len(items)}")
        if items:
            for i in items:
                i.pop("_id")
            return items
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"no entries")

    @app.get(
        "/3/list",
        response_description=f"List recent 100 items of STEP3.",
        status_code=status.HTTP_200_OK,
        response_model=List[PenDBStep2Model],
        )
    async def list_entry():
        logger.debug(f"GET STEP3 LIST")
        items = await x_tab.find(
                { "$and" : [
                        { "tsStep3": { "$ne": None } },
                        { "tsStep4": None }
                        ] }
                ).sort([("tsStep3",-1)]).limit(100).to_list(100)
        logger.debug(f"RET: count={len(items)}")
        if items:
            for i in items:
                i.pop("_id")
            return items
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"no entries")


    @app.delete(
        "/a/xpath/{xpath}",
        response_description="Delete a single item by xpath",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        )
    async def delete_entry(xpath: str):
        logger.debug(f"DELETE: trying: xpath:{xpath}")
        result = await x_tab.delete_one({"xpath": xpath})
        logger.debug(f"RET: count={result.deleted_count} ack={result.acknowledged}")
        if result.deleted_count == 1:
            return
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"not found xpath:{xpath}")

    #
    return app
