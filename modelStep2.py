from pydantic import BaseModel, Field, EmailStr, Extra
from pydantic import validator
from typing import Optional, List, Dict
from datetime import date
import re

"""
Model for the communication betwen users and FrontEnd server.

    UI                           Server
    | -- PenRESTAuthReqModel -->
    | <-- PenRESTStep2Model --
    |    (only required fields)
    |
    | -- PenRESTStep2Model -->
    | <-- OK 201 --
"""

class PenRESTStep2AuthReqModel(BaseModel):
    emailAddr: EmailStr
    xpath: str = Field(min_length=64, max_length=64)
    authcode: str

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "emailAddr": "taro@hokkai.do.jp",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "authcode": "1234-5678-9012",
            }
        }

class Activity(BaseModel):
    placename: Optional[str]
    type: Optional[str]
    profile: Optional[str]
    detail: Optional[str]

class HealthRecordItemModel(BaseModel):
    question: Optional[str]
    text: Optional[str]

class DailyActivityWhat(BaseModel):
    label: Optional[str]
    text: Optional[str]
    selected: Optional[List[str]]

class DailyActivityWhen(BaseModel):
    label: Optional[str]
    timeFrom: Optional[str]
    timeTo: Optional[str]

class DailyActivityWhere(BaseModel):
    text: Optional[str]
    address: Optional[str]

class DailyActivityWhom(BaseModel):
    attendants: Optional[List]
    numPeople: Optional[str]

class DeilyActivityItem(BaseModel):
    what: DailyActivityWhat
    when: DailyActivityWhen
    where: DailyActivityWhere
    whom: DailyActivityWhom
    comment: Optional[str]

class PenRESTStep2Model(BaseModel):
    """
    once auth has been succeeded, the token in header is checked whether
    the submission is acceptable or not.
    so, authtoken is not needed.
    """
    emailAddr: EmailStr
    xpath: str = Field(min_length=64, max_length=64)
    onsetDate: Optional[str]
    birthday: Optional[str]
    sex: Optional[str]
    citizenship: Optional[str]
    livingArea: Optional[str]
    profession: Optional[str]
    communityLife: Optional[str]
    attendantName: Optional[str]
    attendantRelationship: Optional[str]
    attendantAddress: Optional[str]
    attendantPhone: Optional[str]
    activities: Optional[List[Activity]]
    healthRecord: Optional[Dict[str, HealthRecordItemModel]]
    locations: Optional[Dict[str, List[bool]]]
    dailyActivities: Optional[Dict[str, List[DeilyActivityItem]]]

    @classmethod
    def validate_datestr(cls, v):
        """
        v: e.g. "1967-12-25"
        """
        if v is None:
            return None
        else:
            if len(v) != 10:
                return False
            try:
                y, m, d = v.split('-')
                date(int(y), int(m), int(d))
                return v
            except:
                return False

    @validator("onsetDate", pre=True)
    def validate_onsetDate(cls, v):
        ret = cls.validate_datestr(v)
        if ret == False:
            raise ValueError(f"ERROR: invalid onsetDate: {v}")
        else:
            return v

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "emailAddr": "taro@hokkai.do.jp",
                "xpath": "dd6fd57989fabca282b257460f8cc9538f7c770e81ef9dc5aaa5e3d7b4d985bd",
                "authcode": "1234-5678-9012",
                "onsetDate": "2021-08-01",
                "birthday": "1967-12-25",
                "sex": "男",
                "citizenship": "日本",
                "livingArea": "北海道札幌市",
                "profession": "会社員",
                "communityLife": "特になし",
                "attendantName": "",
                "attendantRelationship": "",
                "attendantAddress": "",
                "attendantPhone": "",
                "activityList": [
                    {
                        "placename": "株式会社〇〇",
                        "type": "会社での業務",
                        "profile": "人にあまり会わない活動・仕事（リモートワークを含む）",
                        "detail": "",
                    }
                ],
                "healthRecord": {
                    "該当しない": {
                        "question": None,
                        "text": None
                    },
                    "糖尿病": {
                        "question": "具体的に教えてください",
                        "text": "注射をしている"
                    }
                },
                "locations": {
                    "〇〇総合病院": [ False, True, False ],
                    "〇〇タクシー": [ True, True, True ],
                },
                "dailyActivities": [
                    {
                        "date": "2021-07-31",
                        "detail": {
                            "what": {
                                "label": "",
                                "text": "",
                                "selected": "",
                            },
                            "when": {
                                "label": "",
                                "timeFrom": "",
                                "timeTo": "",
                            },
                            "where": {
                                "text": "",
                                "address": "",
                            },
                            "whom": {
                                "attendants": [ "", "" ],
                                "numPeople": "",
                            },
                            "comment": ""
                        },
                    }
                ]
            }
        }

