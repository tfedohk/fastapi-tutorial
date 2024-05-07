# tests/conftest.py

import pytest_asyncio

# import pytest로 해도 됨
# 비동기 커넥션 엔진을 쓰려면 asyncio를 사용해야 함

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


@pytest_asyncio.fixture
async def async_engine():
    engine = create_async_engine(
        url="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    yield engine
    # yield는 제너레이터 문법임
    # engine을 잠깐 리턴한다.
    # 코드 종료 시 리턴했던 것이 다시 반환되면서 await을 실행한다.
    # 미들웨어, 라이프스팬 함수도 제너리이터와 비슷하다.

    await engine.dispose()
    # yield없이 return engine으로 해도 된다.


@pytest_asyncio.fixture
async def async_session(
    async_engine,
):  # `async_engine`이라는 매개변수 이름을 사용하면 위의 `async def async_engine` 으로 정의한 fixture가 자동으로 주입됩니다.
    # fixture에 의해 async_engine이 알아서 이 함수의 파라미터로 들어간다.
    session = AsyncSession(bind=async_engine)

    yield session

    await session.close()
