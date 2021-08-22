from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional

class PenMMRESTRequestModel(BaseModel):
    xpath: str
    emailAddr: str
    authcode: str
    c3w_words: str

    class Config:
        extra = Extra.ignore

class PenMMRESTStatusModel(BaseModel):
    pass

