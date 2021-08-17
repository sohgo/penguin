from typing import Literal, Union, Tuple
from dateutil import tz
from hashlib import sha256
from datetime import datetime
from random import random
import aiohttp
from logging import Logger

def get_hash() -> str:
    m = sha256()
    m.update((str(random())+str(datetime.now().timestamp())).encode())
    return m.hexdigest()

def get_timestamp(TZ: str = "Asia/Tokyo") -> str:
    return datetime.now(tz=tz.gettz(TZ)).isoformat(timespec="seconds")

async def get_item(
        url: str,
        logger: Logger,
        enable_tls: bool = False,
        ) -> Tuple[int, Union[str, dict]]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=enable_tls) as response:
                logger.debug(f"GET RES: code={response.status} "
                            f"type={response.content_type}")
                if response.content_type == "application/json":
                    content = await response.json()
                elif response.content_type == "text/html":
                    content = await response.text()
                elif response.content_type == "text/plain":
                    content = await response.text()
                else:
                    raise ValueError(
                            f"unknown content-type {response.content_type}")
                #
                return response.status, response.content_type, content
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            logger.error("Server disconnected. You may use HTTPS, instead.")
            raise
        except aiohttp.client_exceptions.ClientConnectorError as e:
            logger.error(f"Cannot connect to host. You may use HTTP, instead.")
            raise

async def post_item(
        url: str,
        data: dict,
        headers: dict = {},
        res_type: Literal["html","json"] = "json",
        enable_tls: bool = False,
        ) -> Tuple[int, Union[str, dict]]:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers,
                                ssl=enable_tls) as response:
            if response.status < 200 and response.status > 299:
                raise ValueError(f"ERROR: response={response.status}")
            if res_type == "html":
                content = await response.text()
            elif res_type == "json":
                content = await response.json()
            else:
                raise SystemError(f"ERROR: content-type={response.content_type}")
            #
            return response.status, content

