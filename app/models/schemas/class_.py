from datetime import datetime
from typing import Optional


from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from typing import List

from app.models.dtos.class_ import (
    ClassDTO,
    ClassNoticeDTO,
    ClassListDTO,
    ClassNoticeListDTO,
)
from app.models.schemas.common import PageResp
from uuid import uuid4


class ClassReq(BaseModel):  # postfix로 Req, Resp는 각각 요청, 응답이다. 식별을 위함.
    # 요청은 Pydantic의 BaseModel을 그대로 쓴다.
    className: str = Field(
        ..., description="Class Name"
    )  # 외부 통신은 서로 다른 언어와 통신한다. 팀바팀, 사바사로 카멜/스네이크를 따라라.
    teacherId: str = Field(
        ..., description="Teacher ID"
    )  # 필드에 대한 정보들을 파라미터로 추가할 수 있다. 파라미터 목록 살펴보기.

    def to_dto(self) -> ClassDTO:
        return ClassDTO(
            class_id=uuid4().hex,
            class_name=self.className,
            teacher_id=self.teacherId,
        )


@dataclass
class ClassResp:  # 실제 반환은 ORJSONResponse로 한다.
    classId: str = Field(..., description="Class ID")
    className: str = Field(..., description="Class Name")
    teacherId: str = Field(..., description="Teacher ID")
    createdAt: datetime = Field(..., description="Created At")
    # dataclass로 정의하면 바로 JSON으로 변환돼서 성능이 개선된다.

    @classmethod  # 아직 ClassResp 인스턴스가 없는 상태이기 때문에, classmethod로 정의한다. 인스턴스 메소드, 클래스 메소드를 공부해라.
    # Java의 static 같은 역할을 한다. 파이썬에도 static은 있다.
    # classmethod와 static method 둘 다 존재한다. : @staticmethod
    #
    def from_dto(
        cls, dto: ClassDTO
    ) -> (
        "ClassResp"
    ):  # 앞서서 정의되지 않았기 때문에, 문법 에러를 피하기 위해 쌍따옴표를 한다.
        return cls(
            classId=dto.class_id,
            className=dto.class_name,
            teacherId=dto.teacher_id,
            createdAt=dto.created_at,
        )


@dataclass
class ClassListResp:
    data: List[ClassResp] = Field(..., description="Data")
    page: PageResp = Field(..., description="Page")

    @classmethod
    def from_dto(cls, dto: ClassListDTO) -> "ClassListResp":
        return cls(
            data=[ClassResp.from_dto(class_) for class_ in dto.data],
            page=PageResp.from_dto(dto.page),
        )


class ClassNoticeReq(BaseModel):
    message: str = Field(..., description="Message")

    def to_dto(self, class_id: str = None, notice_id: int = None) -> ClassNoticeDTO:
        return ClassNoticeDTO(
            notice_id=notice_id,
            class_id=class_id,
            message=self.message,
        )


@dataclass
class ClassNoticeResp:
    id: int = Field(..., description="ID")
    classId: str = Field(..., description="Class ID")
    message: str = Field(..., description="Message")
    createdAt: datetime = Field(..., description="Created At")
    updatedAt: Optional[datetime] = Field(None, description="Updated At")

    @classmethod
    def from_dto(cls, dto: ClassNoticeDTO) -> "ClassNoticeResp":
        return cls(
            id=dto.notice_id,
            classId=dto.class_id,
            message=dto.message,
            createdAt=dto.created_at,
            updatedAt=dto.updated_at,
        )


@dataclass
class ClassNoticeListResp:
    data: List[ClassNoticeResp] = Field(..., description="Data")
    page: PageResp = Field(..., description="Page")

    @classmethod
    def from_dto(cls, dto: ClassNoticeListDTO) -> "ClassNoticeListResp":
        return cls(
            data=[ClassNoticeResp.from_dto(class_notice) for class_notice in dto.data],
            page=PageResp.from_dto(dto.page),
        )
