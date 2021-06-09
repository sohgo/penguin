from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional
from modelREST import PenRESTStep2Model
from datetime import datetime

"""
Model for the FrontEnd and Database

See IMPLEMENTATION.md

Here define the model for DB apart from the REST Model.

Consider whether DB model should inherit the field of the REST Model.
field consistency vs leak control..
"""

HIDDEN_FIELDS = [ "pid", "tsStep1", "c3w_code", "c3w_words", "authcode",
                 "tsStep2", "tsUpdate", "tsStep3", "tsStep4" ]

class PenDBStep1Model(BaseModel):
    pid: str = Field(min_length=64, max_length=64)
    xpath: str
    tsStep1: datetime
    c3w_code: str
    c3w_words: str
    authcode: str
    name: str
    birthM: str
    birthD: str
    emailAddr: EmailStr

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "pid": "6e96f62a4d66ee4f3b017463208fbee8f9fa7a6bbf719e833c61af5c35443b31",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "authcode": "orange",
                "tsStep1": "2021-05-18T12:11:35+09:00",
                "name": "北海太郎",
                "birthM": "12",
                "birthD": "25",
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenDBStep2Model(PenRESTStep2Model, PenDBStep1Model):
    """
    PenDBStep1Model +
    """
    tsStep2: datetime
    tsUpdate: Optional[datetime]
    tsStep3: Optional[datetime]
    tsStep4: Optional[datetime]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "pid": "6e96f62a4d66ee4f3b017463208fbee8f9fa7a6bbf719e833c61af5c35443b31",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "tsStep1": "2021-05-18T12:11:35+09:00",
                "tsStep2": "2021-05-21T16:23:48+09:00",
                "name": "北海太郎",
                "kana": "ほっかいたろう",
                "birthM": "12",
                "birthD": "25",
                "emailAddr": "taro@hokkai.do.jp",
                "onsetDate": "2021-05-18",
                "citizenship": "日本",
                "postcode": "0100001",
            }
        }

"""
--- GET /x/c3ww/xxx-xxxx-xxxx --->
<--- HTTP 200 OK PenDBStep2Model ---
--- POST /3 PenDBStep3UpdateModel -->
<--- HTTP 200 OK PenDBStep2Model ---
"""
class PenDBStep3UpdateModel(BaseModel):
    pid: str
    tsStep3: datetime

    class Config:
        extra = Extra.forbid

