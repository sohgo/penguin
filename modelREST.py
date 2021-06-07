from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional
from datetime import date
import re

"""
Model for the communication betwen users and FrontEnd server.

    UI                           Server
    | -- PenRESTStep1Model --> 
    | <-- PenRESTStep1AckModel --
    |
    | -- PenRESTStep2AuthModel -->
    | <-- PenRESTStep2Model --
    |
    | -- PenRESTStep2Model -->
    | <-- PenRESTStep2Model --
"""

class PenRESTStep1Model(BaseModel):
    name: str
    birthM: str
    birthD: str
    emailAddr: EmailStr

    @validator("birthD")
    def validate_date(cls, birthD, values):
        # brief check.
        # in this stage, accept 2/29 in any year.
        date(2000, int(values["birthM"]), int(birthD))
        return birthD

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "北海太郎",
                "birthM": "12",
                "birthD": "25",
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenRESTStep1AckModel(PenRESTStep1Model):
    """
    PenRESTStep1Model +
    """
    xpath: str = Field(min_length=64, max_length=64)

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "name": "北海太郎",
                "birthM": "12",
                "birthD": "25",
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenRESTStep2AuthModel(BaseModel):
    xpath: str = Field(min_length=64, max_length=64)
    birthM: str
    birthD: str
    authcode: str

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "birthM": "12",
                "birthD": "25",
                "authcode": "1234-5678-9012",
            }
        }

class PenRESTStep2Model(PenRESTStep1AckModel):
    """
    PenRESTStep1AckModel +

    NOTE: kana, birthY : Step2のPOST以降は必須フィールド。
    """
    kana: Optional[str]
    onsetY: Optional[str]
    onsetM: Optional[str]
    onsetD: Optional[str]
    birthY: Optional[str]
    citizenship: Optional[str]
    postcode: Optional[str]
    addrPref: Optional[str]
    addrCity: Optional[str]
    pregnant: Optional[bool]
    smoker: Optional[bool]
    smokerDetail: Optional[str]
    # XXX needs to add more fields.

    @validator("birthY")
    def validate_date(cls, birthY, values):
        date(int(birthY), int(values["birthM"]), int(values["birthD"]))
        return birthY

    @classmethod
    def validate_strnum(cls, v, size):
        if v is None:
            return v
        else:
            regex = f"^\d{{{size}}}$"
            if re.match(regex, v):
                return v
            else:
                raise ValueError(f"ERROR: invalid onset: {v}")

    @validator("onsetY", pre=True)
    def validate_onsetY(cls, v):
        return cls.validate_strnum(v, 4)

    @validator("onsetM", "onsetD", pre=True)
    def validate_onsetM(cls, v):
        return cls.validate_strnum(v, 2)

    @validator("postcode", pre=True)
    def validate_postcode(cls, v):
        if v:
            if re.match("^(\d{7}|\d{3}-\d{4})$", v):
                return v.replace("-","")
            else:
                raise ValueError(f"ERROR: invalid postcode: {v}")
        else:
            return v

    @validator("kana", pre=True)
    def validate_kana(cls, v):
        if v is None:
            return v
        else:
            if re.match("^[ぁ-ゔー\s\u3000・]*$", text):
                return v
            else:
                raise ValueError(f"ERROR: invalid kana: {v}")

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "name": "北海太郎",
                "kana": "ほっかいたろう",
                "birthY": "1999",
                "birthM": "12",
                "birthD": "25",
                "emailAddr": "taro@hokkai.do.jp",
                "citizenship": "日本",
                "postcode": "0100001",
            }
        }

