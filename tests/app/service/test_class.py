import pytest
from unittest.mock import AsyncMock

from app.models.dtos.common import PageDTO
from app.models.dtos.class_ import ClassDTO, ClassListDTO
from app.services.class_service import ClassService


@pytest.mark.asyncio
async def test_create_class(
    class_repository_mock: AsyncMock,
    class_service_mock: ClassService,
):  # 위 두 개는 conftest.py에 정의되어 있는 것.
    # Setup
    class_dto = ClassDTO(
        class_id="class_id",
        class_name="class_name",
        teacher_id="teacher_id",
    )  # 리턴해야 할 value를 정의한 것
    class_repository_mock.create_class.return_value = class_dto

    # Run
    result = await class_service_mock.create_class(class_dto=class_dto)
    # mock 클래스가 class_dto를 리턴하도록 설정하는 부분

    # Assert
    assert result != None
    assert result.class_id == class_dto.class_id
    assert result.class_name == class_dto.class_name
    assert result.teacher_id == class_dto.teacher_id

    class_service_mock.class_repository.create_class.assert_called_once_with(
        class_id=class_dto.class_id,
        class_name=class_dto.class_name,
        teacher_id=class_dto.teacher_id,
    )


@pytest.mark.asyncio
async def test_read_class_list(
    class_repository_mock: AsyncMock,
    class_service_mock: ClassService,
):
    # Setup
    page = 1  # 페이지네이션을 위한 변수
    limit = 10
    total = 1
    class_dto = ClassDTO(
        class_id="class_id",
        class_name="class_name",
        teacher_id="teacher_id",
    )
    page_dto = PageDTO(page=page, limit=limit, total=total)

    class_list_dto = ClassListDTO(page=page_dto, data=[class_dto])
    class_repository_mock.read_class_list.return_value = class_list_dto

    # Run
    results = await class_service_mock.read_class_list(page=page, limit=limit)

    # Assert
    assert results != None

    # page 검사
    result_page = results.page
    assert result_page.page == page_dto.page
    assert result_page.limit == page_dto.limit
    assert result_page.total == page_dto.total

    result_data = results.data
    assert len(result_data) == 1
    result = result_data[0]
    assert result.class_id == class_dto.class_id
    assert result.class_name == class_dto.class_name
    assert result.teacher_id == class_dto.teacher_id

    class_service_mock.class_repository.read_class_list.assert_called_once_with(
        page=page, limit=limit
    )


@pytest.mark.asyncio
async def test_read_class(
    class_repository_mock: AsyncMock,
    class_service_mock: ClassService,
):
    # Setup
    class_id = "class_id"
    class_dto = ClassDTO(
        class_id=class_id,
        class_name="class_name",
        teacher_id="teacher_id",
    )
    class_repository_mock.read_class.return_value = class_dto

    # Run
    result = await class_service_mock.read_class(class_id=class_id)

    # Assert
    assert result != None
    assert result.class_id == class_dto.class_id
    assert result.class_name == class_dto.class_name
    assert result.teacher_id == class_dto.teacher_id

    class_service_mock.class_repository.read_class.assert_called_once_with(
        class_id=class_id
    )
