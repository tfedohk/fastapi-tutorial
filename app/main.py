# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.core.lifespan import lifespan
# from app.routers import router
# from app.core.errors.error import BaseAPIException, BaseAuthException
# from app.core.errors.handler import api_error_handler, api_auth_error_handler
# from app.core.middlewares.sqlalchemy import SQLAlchemyMiddleware
# from app.core.container import Container

# from app.core.config import config
# from starlette_context.middleware import ContextMiddleware

# app = FastAPI(lifespan=lifespan, **config.fastapi_kwargs)

# app.include_router(router)
# app.add_exception_handler(BaseAPIException, api_error_handler)
# app.add_exception_handler(BaseAuthException, api_auth_error_handler)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.add_middleware(SQLAlchemyMiddleware)
# app.add_middleware(ContextMiddleware)
# """
# 뒤에까지 간다음에 돌아오면서 재귀적으로 호출된다. 따라서 app.add_middleware(ContextMiddleware)가 맨 밑에 있어야 한다.

# """


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# # 테스트를 위해 추가됨
# from app.core.db.session import AsyncScopedSession
# from app.core.logger import logger


# @app.get("/session/test")
# async def session_test():
#     async with AsyncScopedSession() as session:
#         logger.debug(session)

#     async with AsyncScopedSession() as session:
#         logger.debug(session)

#     async with AsyncScopedSession() as session:
#         logger.debug(session)

#     async with AsyncScopedSession() as session:
#         logger.debug(session)

#     async with AsyncScopedSession() as session:
#         logger.debug(session)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_context.middleware import ContextMiddleware

from app.core.config import config
from app.core.lifespan import lifespan
from app.core.container import Container
from app.core.middlewares.sqlalchemy import SQLAlchemyMiddleware
from app.core.errors.error import BaseAPIException, BaseAuthException
from app.core.errors.handler import api_error_handler, api_auth_error_handler
from app.routers import router


def create_app(container=Container()) -> FastAPI:
    app = FastAPI(lifespan=lifespan, **config.fastapi_kwargs)

    # container = Container()
    container.config.from_dict(config.model_dump())

    app.include_router(router)
    app.add_exception_handler(BaseAPIException, api_error_handler)
    app.add_exception_handler(BaseAuthException, api_auth_error_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SQLAlchemyMiddleware)
    app.add_middleware(ContextMiddleware)

    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
