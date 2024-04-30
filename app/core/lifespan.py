from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.db.session import ping_db, close_db


@asynccontextmanager  # 함수에 함수로 감싸는 데코레이터. 지금은 큰 기능은 없더라도, 더 복잡한 기능 구현에 쓰일 것이다.
async def lifespan(app: FastAPI):
    await ping_db()

    yield

    await close_db()
