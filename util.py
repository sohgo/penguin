from typing import Literal, Union, Tuple
from dateutil import tz
from hashlib import sha256
from datetime import datetime
from random import random
import aiohttp

def get_hash() -> str:
    m = sha256()
    m.update((str(random())+str(datetime.now().timestamp())).encode())
    return m.hexdigest()

def get_timestamp(TZ: str = "Asia/Tokyo") -> str:
    return datetime.now(tz=tz.gettz(TZ)).isoformat(timespec="seconds")

async def get_item(
        url: str,
        res_type: Literal["html","json"] = "html",
        enable_tls: bool = False,
        ) -> Tuple[int, Union[str, dict]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=enable_tls) as response:
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

