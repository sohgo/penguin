from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional
from modelREST import PenRESTStep2Model
from datetime import datetime

"""
Model for the FrontEnd and Database

XXX:
onsider whether DB model should inherit the field of the REST Model.
field consistency vs leak control..
"""


class PenDBStep1Model(BaseModel):
    """
    pid: 普遍のユニークID
    xpath: tsStep1からn日間(=30?)で無効になる。
    tsStep1: Step1がPOSTされたタイムスタンプ
    emailAddr: Eメールアドレスもユニークになる。
        XXX 同じ患者で別症例の場合は重複を許すことになるか？
    """
    pid: str = Field(min_length=64, max_length=64)
    xpath: str
    tsStep1: datetime
    name: str
    kana: str
    birthM: str
    birthD: str
    favColor: str
    emailAddr: EmailStr

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "pid": "6e96f62a4d66ee4f3b017463208fbee8f9fa7a6bbf719e833c61af5c35443b31",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "tsStep1": "2021-05-18T12:11:35+09:00",
                "name": "北海太郎",
                "kana": "ほっかいたろう",
                "birthM": "12",
                "birthD": "25",
                "favColor": "orange",
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenDBStep2Model(PenRESTStep2Model, PenDBStep1Model):
    """
    PenDBStep1Model +
    tsStep2: 最初にStep2の情報が書き込まれたタイムスタンプ
    tsUpdated: 情報が更新された日付。更新されていく。
    """
    tsStep2: datetime
    tsUpdated: Optional[datetime]

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
                "favColor": "orange",
                "emailAddr": "taro@hokkai.do.jp",
                "onsetDate": "2021-05-18",
                "citizenship": "日本",
                "postcode": "0100001",
            }
        }

