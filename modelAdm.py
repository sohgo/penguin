from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional
from datetime import date
from modelDB import PenDBStep2Model
import re

class PenAdmDownloadResponseModel(PenDBStep2Model):
    pass

class PenAdmCopyReqModel(PenDBStep2Model):
    pass

class PenAdmStatAckModel(BaseModel):
    pass

