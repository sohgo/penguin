from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional
from bson import ObjectId
import re

"""
Model for the users and FrontEnd
"""

class PenRESTStep1Model(BaseModel):
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
                "name": "北海太郎",
                "kana": "ほっかいたろう",
                "birthM": "12",
                "birthD": "25",
                "favColor": "orange",
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
                "kana": "ほっかいたろう",
                "birthM": "12",
                "birthD": "25",
                "favColor": "orange",
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenRESTStep2AuthModel(BaseModel):
    xpath: str = Field(min_length=64, max_length=64)
    birthM: str
    birthD: str
    favColor: str

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "birthM": "12",
                "birthD": "25",
                "favColor": "orange",
            }
        }

class PenRESTStep2Model(PenRESTStep1AckModel):
    """
    PenRESTStep1AckModel +
    """
    onsetY: Optional[str]
    onsetM: Optional[str]
    onsetD: Optional[str]
    birthY: Optional[str]
    citizenship: Optional[str]
    postcode: Optional[str]
    addrPref: Optional[str]
    addrCity: Optional[str]

    @classmethod
    def validate_strnum(cls, v, size):
        if v is None:
            return v
        else:
            regex = f"^\d{{{size}}}$"
            if re.match(regex, v):
                return v
            else:
                raise ValueError(f"ERROR: invalid onsetY: {v}")

    @validator('onsetY', pre=True)
    def validate_onsetY(cls, v):
        return cls.validate_strnum(v, 4)

    @validator('onsetM', pre=True)
    def validate_onsetM(cls, v):
        return cls.validate_strnum(v, 2)

    @validator('onsetD', pre=True)
    def validate_onsetD(cls, v):
        return cls.validate_strnum(v, 2)

    @validator('postcode', pre=True)
    def validate_postcode(cls, v):
        if v:
            if re.match("^(\d{7}|\d{3}-\d{4})$", v):
                return v.replace("-","")
            else:
                raise ValueError(f"ERROR: invalid postcode: {v}")
        else:
            return v

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
                "favColor": "orange",
                "emailAddr": "taro@hokkai.do.jp",
                "citizenship": "日本",
                "postcode": "0100001",
            }
        }

class PenRESTStep2AckModel(PenRESTStep2Model):
    """
    PenRESTStep2Model +
    """

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
                "favColor": "orange",
                "emailAddr": "taro@hokkai.do.jp",
                "citizenship": "日本",
                "postcode": "0100001",
            }
        }

