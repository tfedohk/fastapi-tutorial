from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_context import context


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        context["session_id"] = uuid4().hex
        """
        우리가 필요한 로직을 context에 넣어준다.
        유일한 값을 넣어준다.
        각 요청마다 유지되는 컨텍스트 값이다.

        """

        return await call_next(request)
