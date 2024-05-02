from pydantic import BaseModel
from typing import Generic, Optional, TypeVar, Optional
from fastapi.responses import ORJSONResponse


T = TypeVar("T")
# 파이썬 제네릭 타입에 대해 따로 공부하기
#


class BaseResponse(
    BaseModel, Generic[T]
):  # Pydantic의 validation 기능을 이용하기 위해 BaseModel을 사용
    message: str = "OK"
    statusCode: str = "200"
    data: Optional[T] = (
        None  # 응답 데이터가 들어가는 부분. 내가 정의하는 이 순간에는 이 변수에 무슨 타입이 들어갈지는 모르겠어. 전달한 데이터의 타입으로 정의해줘.
    )


class ErrorResponse(BaseModel):
    message: str
    statusCode: str


class HttpResponse(
    ORJSONResponse
):  # Pydantic의 Response Model의 성능 개선을 위해 실제 리턴은 ORJSONResponse를 이용
    def __init__(self, content: Optional[T] = None, **kwargs):
        super().__init__(
            content={
                "message": "OK",
                "statusCode": "200",
                "data": content,
            },
            **kwargs
        )
