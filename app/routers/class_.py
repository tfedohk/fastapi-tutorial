from uuid import uuid4
from typing import List

from fastapi import APIRouter
from sqlalchemy import select, insert, update, delete

from app.core.db.session import AsyncScopedSession
from app.models.schemas.common import BaseResponse, HttpResponse  #
from app.models.schemas.class_ import (
    ClassReq,
    ClassResp,
    ClassNoticeReq,
    ClassNoticeResp,
)
from app.models.db.class_ import Class, ClassNotice

router = APIRouter()


@router.post(
    "", response_model=BaseResponse[ClassResp]
)  # /class/. class 생성 post. ClassResp: 넣고 싶은 타입 부분-> 제네릭 T 부분이 ClassResp로 치환됨. Validation, Swagger에 들어가게 됨
async def create_class(  # endpoint
    request_body: ClassReq,  # 클래스 생성 시 요청할 클래스
) -> BaseResponse[ClassResp]:
    class_id = (
        uuid4().hex
    )  # hexa decimal uuid 스트링 그냥 쓰기 보단, hexa decimal로 별도로 한 번 더 만들어서 쓴다. 스타일적인 부분.
    async with AsyncScopedSession() as session:
        stmt = (
            insert(Class)
            .values(
                class_id=class_id,
                class_name=request_body.className,
                teacher_id=request_body.teacherId,
            )
            .returning(Class)
        )

        result: Class = (await session.execute(stmt)).scalar()
        await session.commit()  # write 연산이기 때문에 반드시 커밋해야 함
        # try-except로 롤백 기능도 반드시 넣어야 함

    return HttpResponse(  # HttpResponse: ORJSONResponse를 상속받아 만들어짐
        content=ClassResp(
            classId=result.class_id,
            className=result.class_name,
            teacherId=result.teacher_id,
            createdAt=result.created_at,
        )
    )


@router.get(
    "/list", response_model=BaseResponse[List[ClassResp]]
)  # 전체 클래스 리스트를 가져오라: get("/list", List[ClassResp]].
async def read_class_list() -> BaseResponse[List[ClassResp]]:
    async with AsyncScopedSession() as session:
        stmt = select(Class)
        result = (
            (await session.execute(stmt)).scalars().all()
        )  # all select는 위험하긴 함. 그래서 페이지네이션이 필요->다음 시간.

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


@router.get(
    "/{class_id}", response_model=BaseResponse[ClassResp]
)  # 특정 class에 대한 정보만 리턴한다. List로 리턴안하고 있음.
async def read_class(
    class_id: str,
) -> BaseResponse[ClassResp]:
    async with AsyncScopedSession() as session:
        stmt = select(Class).where(Class.class_id == class_id)
        result = (await session.execute(stmt)).scalar()

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
) -> BaseResponse[ClassNoticeResp]:
    async with AsyncScopedSession() as session:
        stmt = (
            insert(ClassNotice)
            .values(class_id=class_id, message=request_body.message)
            .returning(ClassNotice)
        )

        result: ClassNotice = (await session.execute(stmt)).scalar()
        await session.commit()

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
    class_id: str,
) -> BaseResponse[List[ClassNoticeResp]]:
    async with AsyncScopedSession() as session:
        stmt = (
            select(ClassNotice)
            .where(ClassNotice.class_id == class_id)
            .order_by(ClassNotice.created_at.desc())
        )
        result = (await session.execute(stmt)).scalars().all()

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
) -> ClassNoticeResp:
    async with AsyncScopedSession() as session:
        stmt = (
            update(ClassNotice)
            .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
            .values(message=request_body.message)
            .returning(ClassNotice)
        )
        result: ClassNotice = (await session.execute(stmt)).scalar()
        await session.commit()

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
    class_id: str,
    notice_id: int,
) -> ClassNoticeResp:
    async with AsyncScopedSession() as session:
        stmt = (
            delete(ClassNotice)
            .where(ClassNotice.id == notice_id, ClassNotice.class_id == class_id)
            .returning(ClassNotice)
        )
        result: ClassNotice = (await session.execute(stmt)).scalar()
        await session.commit()

    return HttpResponse(
        content=ClassNoticeResp(
            id=result.id,
            classId=result.class_id,
            message=result.message,
            createdAt=result.created_at,
            updatedAt=result.updated_at,
        )
    )
