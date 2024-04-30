from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


class ClassReq(BaseModel):  # postfix로 Req, Resp는 각각 요청, 응답이다. 식별을 위함.
    # 요청은 Pydantic의 BaseModel을 그대로 쓴다.
    className: str = Field(
        ..., title="Class Name"
    )  # 외부 통신은 서로 다른 언어와 통신한다. 팀바팀, 사바사로 카멜/스네이크를 따라라.
    teacherId: str = Field(
        ..., title="Teacher ID"
    )  # 필드에 대한 정보들을 파라미터로 추가할 수 있다. 파라미터 목록 살펴보기.


@dataclass
class ClassResp:  # 실제 반환은 ORJSONResponse로 한다.
    classId: str = Field(..., title="Class ID")
    className: str = Field(..., title="Class Name")
    teacherId: str = Field(..., title="Teacher ID")
    createdAt: datetime = Field(..., title="Created At")
    # dataclass로 정의하면 바로 JSON으로 변환돼서 성능이 개선된다.


class ClassNoticeReq(BaseModel):
    message: str = Field(..., title="Message")


@dataclass
class ClassNoticeResp:
    id: int = Field(..., title="ID")
    classId: str = Field(..., title="Class ID")
    message: str = Field(..., title="Message")
    createdAt: datetime = Field(..., title="Created At")
    updatedAt: Optional[datetime] = Field(None, title="Updated At")
