from uuid import uuid4
from typing import List

from fastapi import APIRouter
from sqlalchemy import select, insert, update, delete

from app.core.errors import error
from app.core.logger import logger
from app.core.redis import redis_cache, key_builder
from app.core.db.session import AsyncScopedSession
from app.models.schemas.common import BaseResponse, HttpResponse, ErrorResponse  #
from app.models.schemas.class_ import (
    ClassReq,
    ClassResp,
    ClassNoticeReq,
    ClassNoticeResp,
)
from app.models.db.class_ import Class, ClassNotice

router = APIRouter()


@router.post(
    "",
    response_model=BaseResponse[ClassResp],
    responses={400: {"model": ErrorResponse}},
)  # /class/. class 생성 post. ClassResp: 넣고 싶은 타입 부분-> 제네릭 T 부분이 ClassResp로 치환됨. Validation, Swagger에 들어가게 됨
async def create_class(  # endpoint
    request_body: ClassReq,  # 클래스 생성 시 요청할 클래스
) -> BaseResponse[ClassResp]:
    class_id = (
        uuid4().hex
    )  # hexa decimal uuid 스트링 그냥 쓰기 보단, hexa decimal로 별도로 한 번 더 만들어서 쓴다. 스타일적인 부분.
    async with AsyncScopedSession() as session:
        #     stmt = (
        #         insert(Class)
        #         .values(
        #             class_id=class_id,
        #             class_name=request_body.className,
        #             teacher_id=request_body.teacherId,
        #         )
        #         .returning(Class)
        #     )

        #     result: Class = (await session.execute(stmt)).scalar()
        #     await session.commit()  # write 연산이기 때문에 반드시 커밋해야 함
        #     # try-except로 롤백 기능도 반드시 넣어야 함
        try:
            stmt = (
                insert(Class)
                .values(
                    class_id=class_id,
                    class_name=request_body.className,
                    teacher_id=request_body.teacherId,
                )
                .returning(Class)
            )
            """ 에러가 발생할 수 있는 부분"""

            result: Class = (await session.execute(stmt)).scalar()
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()  # 커밋이 안찍혔을 수도 있으나, 확실하게 하기 위해 롤백
            raise error.ClassCreationFailed()

    return HttpResponse(  # HttpResponse: ORJSONResponse를 상속받아 만들어짐
        content=ClassResp(
            classId=result.class_id,
            className=result.class_name,
            teacherId=result.teacher_id,
            createdAt=result.created_at,
        )
    )


@router.get(
    "/list",
    response_model=BaseResponse[List[ClassResp]],
    responses={400: {"model": ErrorResponse}},
)  # 전체 클래스 리스트를 가져오라: get("/list", List[ClassResp]].
async def read_class_list() -> BaseResponse[List[ClassResp]]:
    _key = key_builder("read_class_list")

    if await redis_cache.exists(_key):
        result = await redis_cache.get(_key)
        logger.debug(f"Cache hit: {_key}")

    else:
        async with AsyncScopedSession() as session:
            stmt = select(Class)
            result = (
                (await session.execute(stmt)).scalars().all()
            )  # all select는 위험하긴 함. 그래서 페이지네이션이 필요->다음 시간.

        await redis_cache.set(_key, result, ttl=60)
        logger.debug(f"Cache miss: {_key}")

    return HttpResponse(
        content=[
            ClassResp(
                classId=class_.class_id,
                className=class_.class_name,
                teacherId=class_.teacher_id,
                createdAt=class_.created_at,
            )
            for class_ in result
        ]
    )


# @router.get(
#     "/{class_id}", response_model=BaseResponse[ClassResp]
# )  # 특정 class에 대한 정보만 리턴한다. List로 리턴안하고 있음.
# async def read_class(
#     class_id: str,
# ) -> BaseResponse[ClassResp]:
#     _key = key_builder("read_class", class_id)
#     if redis_cache.exists(_key):
#         result = await redis_cache.get(_key)
#         logger.debug(f"Cache hit: {_key}")

#     else:
#         async with AsyncScopedSession() as session:
#             stmt = select(Class).where(Class.class_id == class_id)
#             result = (await session.execute(stmt)).scalar()
#             # 에러가 발생할 가능성이 적다.

#         if result is not None: # DB에 있을 때(None이 아닐 떄) 캐싱을 해라.
#             await redis_cache.set(_key, result, ttl=60)
#         logger.debug(f"Cache miss: {_key}")

#     if result is None: # 결과값을 검사한다. 반환받는 게 없으면 None을 받기 때문.
#         raise error.ClassNotFoundException()
#     ''' 네가 찾는 게 없다는 의미의 400에러를 준다는 식으로 방어 로직을 만든다.'''

#     return HttpResponse(
#         content=ClassResp(
#             classId=result.class_id,
#             className=result.class_name,
#             teacherId=result.teacher_id,
#             createdAt=result.created_at,
#         )
#     )


# @router.post("/notice/{class_id}", response_model=BaseResponse[ClassNoticeResp])
# async def create_class_notice(
#     class_id: str,
#     request_body: ClassNoticeReq,
# ) -> BaseResponse[ClassNoticeResp]:
#     async with AsyncScopedSession() as session:
#         # stmt = (
#         #     insert(ClassNotice)
#         #     .values(class_id=class_id, message=request_body.message)
#         #     .returning(ClassNotice)
#         # )

#         # result: ClassNotice = (await session.execute(stmt)).scalar()
#         # await session.commit()
#         try:
#             stmt = (
#                 insert(ClassNotice)
#                 .values(class_id=class_id, message=request_body.message)
#                 .returning(ClassNotice)
#             )

#             result: ClassNotice = (await session.execute(stmt)).scalar()
#             await session.commit()
#         except Exception as e:
#             logger.error(e)
#             await session.rollback()
#             raise error.ClassNoticeCreationFailed()

#     '''
#     CUD 작업은 항상 try-except를 하는 것으로 이해하면 되나?
#     '''
#     return HttpResponse(
#         content=ClassNoticeResp(
#             id=result.id,
#             classId=result.class_id,
#             message=result.message,
#             createdAt=result.created_at,
#             updatedAt=result.updated_at,
#         )
#     )


# @router.get(
#     "/notice/{class_id}/list", response_model=BaseResponse[List[ClassNoticeResp]]
# )
# async def read_class_notice_list(
#     class_id: str,
# ) -> BaseResponse[List[ClassNoticeResp]]:
#     _key = key_builder("read_class_notice_list", class_id)
#     if redis_cache.exists(_key):
#         result = await redis_cache.get(_key)
#         logger.debug(f"Cache hit: {_key}")

#     else:
#         async with AsyncScopedSession() as session:
#             stmt = (
#                 select(ClassNotice)
#                 .where(ClassNotice.class_id == class_id)
#                 .order_by(ClassNotice.created_at.desc())
#             )
#             result = (await session.execute(stmt)).scalars().all()

#         if result:
#             await redis_cache.set(_key, result, ttl=60)
#         logger.debug(f"Cache miss: {_key}")

#     if not result: # if result is None:
#         raise error.ClassNoticeNotFound()

#     return HttpResponse(
#         content=[
#             ClassNoticeResp(
#                 id=notice.id,
#                 classId=notice.class_id,
#                 message=notice.message,
#                 createdAt=notice.created_at,
#                 updatedAt=notice.updated_at,
#             )
#             for notice in result
#         ]
#     )


# @router.put("/notice/{class_id}/{notice_id}", response_model=ClassNoticeResp)
# async def update_class_notice(
#     class_id: str,
#     notice_id: int,
#     request_body: ClassNoticeReq,
# ) -> ClassNoticeResp:
#     async with AsyncScopedSession() as session:
#         try:
#             stmt = (
#                 update(ClassNotice)
#                 .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
#                 .values(message=request_body.message)
#                 .returning(ClassNotice)
#             )
#             result: ClassNotice = (await session.execute(stmt)).scalar()
#             await session.commit()
#         except Exception as e:
#             logger.error(e)
#             await session.rollback()
#             # raise error.ClassNoticeDeleteFailed()

#     return HttpResponse(
#         content=ClassNoticeResp(
#             id=result.id,
#             classId=result.class_id,
#             message=result.message,
#             createdAt=result.created_at,
#             updatedAt=result.updated_at,
#         )
#     )


# @router.delete("/notice/{class_id}/{notice_id}", response_model=ClassNoticeResp)
# async def delete_class_notice(
#     class_id: str,
#     notice_id: int,
# ) -> ClassNoticeResp:
#     async with AsyncScopedSession() as session:
#         try:
#             stmt = (
#                 delete(ClassNotice)
#                 .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
#                 .returning(ClassNotice)
#             )
#             result: ClassNotice = (await session.execute(stmt)).scalar()
#             await session.commit()
#         except Exception as e:
#             logger.error(e)
#             await session.rollback()
#             raise error.ClassNoticeDeleteFailed()

#     return HttpResponse(
#         content=ClassNoticeResp(
#             id=result.id,
#             classId=result.class_id,
#             message=result.message,
#             createdAt=result.created_at,
#             updatedAt=result.updated_at,
#         )
#     )


@router.get("/{class_id}", response_model=BaseResponse[ClassResp])
async def read_class(
    class_id: str, responses={400: {"model": ErrorResponse}}
) -> BaseResponse[ClassResp]:
    _key = key_builder("read_class", class_id)

    if await redis_cache.exists(_key):
        logger.debug("Cache hit")
        result = await redis_cache.get(_key)
    else:
        logger.debug("Cache miss")
        async with AsyncScopedSession() as session:
            stmt = select(Class).where(Class.class_id == class_id)
            result = (await session.execute(stmt)).scalar()

        await redis_cache.set(_key, result, ttl=60)

    if result is None:
        raise error.ClassNotFoundException()

    return HttpResponse(
        content=ClassResp(
            classId=result.class_id,
            className=result.class_name,
            teacherId=result.teacher_id,
            createdAt=result.created_at,
        )
    )


@router.post("/notice/{class_id}", response_model=BaseResponse[ClassNoticeResp])
async def create_class_notice(
    class_id: str,
    request_body: ClassNoticeReq,
    responses={400: {"model": ErrorResponse}},
) -> BaseResponse[ClassNoticeResp]:
    async with AsyncScopedSession() as session:
        try:
            stmt = (
                insert(ClassNotice)
                .values(class_id=class_id, message=request_body.message)
                .returning(ClassNotice)
            )

            result: ClassNotice = (await session.execute(stmt)).scalar()
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise error.ClassNoticeCreationFailed()

    return HttpResponse(
        content=ClassNoticeResp(
            id=result.id,
            classId=result.class_id,
            message=result.message,
            createdAt=result.created_at,
            updatedAt=result.updated_at,
        )
    )


@router.get(
    "/notice/{class_id}/list", response_model=BaseResponse[List[ClassNoticeResp]]
)
async def read_class_notice_list(
    class_id: str, responses={400: {"model": ErrorResponse}}
) -> BaseResponse[List[ClassNoticeResp]]:
    _key = key_builder("read_class_notice_list", class_id)

    if await redis_cache.exists(_key):
        logger.debug("Cache hit")
        result = await redis_cache.get(_key)
    else:
        logger.debug("Cache miss")
        async with AsyncScopedSession() as session:
            stmt = (
                select(ClassNotice)
                .where(ClassNotice.class_id == class_id)
                .order_by(ClassNotice.created_at.desc())
            )
            result = (await session.execute(stmt)).scalars().all()

        await redis_cache.set(_key, result, ttl=60)

    if not result:
        raise error.ClassNoticeNotFound()

    return HttpResponse(
        content=[
            ClassNoticeResp(
                id=notice.id,
                classId=notice.class_id,
                message=notice.message,
                createdAt=notice.created_at,
                updatedAt=notice.updated_at,
            )
            for notice in result
        ]
    )


@router.put("/notice/{class_id}/{notice_id}", response_model=ClassNoticeResp)
async def update_class_notice(
    class_id: str,
    notice_id: int,
    request_body: ClassNoticeReq,
    responses={400: {"model": ErrorResponse}},
) -> ClassNoticeResp:
    async with AsyncScopedSession() as session:
        try:
            stmt = (
                update(ClassNotice)
                .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
                .values(message=request_body.message)
                .returning(ClassNotice)
            )
            result: ClassNotice = (await session.execute(stmt)).scalar()
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise error.ClassNoticeUpdateFailed()

    if result is None:
        raise error.ClassNoticeNotFound()

    return HttpResponse(
        content=ClassNoticeResp(
            id=result.id,
            classId=result.class_id,
            message=result.message,
            createdAt=result.created_at,
            updatedAt=result.updated_at,
        )
    )


@router.delete("/notice/{class_id}/{notice_id}", response_model=ClassNoticeResp)
async def delete_class_notice(
    class_id: str, notice_id: int, responses={400: {"model": ErrorResponse}}
) -> ClassNoticeResp:
    async with AsyncScopedSession() as session:
        try:
            stmt = (
                delete(ClassNotice)
                .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
                .returning(ClassNotice)
            )
            result: ClassNotice = (await session.execute(stmt)).scalar()
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise error.ClassNoticeDeleteFailed()

    if result is None:
        raise error.ClassNoticeNotFound()

    return HttpResponse(
        content=ClassNoticeResp(
            id=result.id,
            classId=result.class_id,
            message=result.message,
            createdAt=result.created_at,
            updatedAt=result.updated_at,
        )
    )
