from fastapi import Request
from fastapi.responses import ORJSONResponse
from starlette import status
from app.core.errors.error import BaseAPIException, BaseAuthExeption


async def api_error_handler(_: Request, exc: BaseAPIException) -> ORJSONResponse:
    """
    _.base_url.path 등으로 접근 가능
    Request는 반드시 받아야만 하는 것
    """
    return ORJSONResponse(
        content={"statusCode": exc.code, "message": exc.message},
        status_code=status.HTTP_400_BAD_REQUEST,  # 400
    )
    """
        응답의 형태를 맞춰준다.
        BaseResponseModel에서 띠온다.
        내부로직에서 에러가 발생하면, BaseAPIException에게 던져주는 게 필요하다.
    """


async def api_auth_error_handler(_: Request, exc: BaseAuthExeption) -> ORJSONResponse:
    return ORJSONResponse(
        content={
            "statusCode": exc.code,
            "message": exc.message,
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
