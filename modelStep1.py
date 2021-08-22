from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional

"""
Model for the communication betwen a user and the entry server.
"""
class PenRESTStep1Model(BaseModel):
    emailAddr: EmailStr

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "emailAddr": "taro@hokkai.do.jp",
            }
        }

class PenRESTStep1AckModel(BaseModel):
    emailAddr: EmailStr
    xpath: str = Field(min_length=64, max_length=64)
    redirectHost: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "emailAddr": "taro@hokkai.do.jp",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd"
            }
        }
