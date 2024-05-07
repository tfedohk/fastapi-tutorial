import pytest
from datetime import datetime

from httpx import AsyncClient

from app.core.container import Container
from app.core.errors import error
from app.models.dtos.user import UserDTO
from app.models.constants import UserRole
from app.models.schemas.user import UserReq
from app.services import UserService

# 모든 엔드포인트에 대한 테스트 코드는 STATUS CODE에 맞게 테스트 코드를 작성해야 한다.


@pytest.mark.parametrize(
    "user_name,user_role",
    [
        ("test_username", UserRole.TEACHER),
    ],
)
async def test_create_user_teacher_200(  # 선생님 계정 생성 테스트. 200이 나오면 성공 케이스다.
    container: Container,
    async_client: AsyncClient,
    user_service_mock: UserService,
    # 위의 세 개는 fixture로 정의된 것
    user_name: str,
    user_role: UserRole,
    # 입력받을 인자들을 정의한 것
):
    # Setup
    # Request
    data = UserReq(
        userName=user_name,
    )
    # Repository
    user_dto = UserDTO(
        user_id="-",  # 내부적으로 랜덤하게 유효하게 만들어놔서 이렇게 넣는다.
        user_name=user_name,
        user_role=user_role,
        created_at=datetime.now(),  # 검사만 하면 되는 것이기 때문에 이렇게 넣어도 된다.
    )
    user_service_mock.user_repository.create_teacher_user.return_value = (
        user_dto  # 모킹된 객체에 리턴값을 명시적으로 넣어준다.
    )
    container.user_service.override(
        user_service_mock
    )  # 컨테이너에 모킹된 객체를 넣어준다.
    # override는 컨테이너에 있는 객체를 덮어쓰는 것이다. 이렇게 함으로써 container가 생성된 이후에도 모킹된 객체를 사용할 수 있다.

    # Run
    headers = {"x-api-key": "test_api_key"}
    url = "/v1/user/teacher"
    response = await async_client.post(  # async_client는 conftest.py에 정의되어 있는 것
        # create_teacher를 위해 post
        url,
        headers=headers,
        data=data.model_dump_json(),  # data는 UserReq의 인스턴스
    )
    json_response = response.json()  # response를 json으로 변환
    # app 서버를 따로 띄우지 않은 채, async_client를 통해 테스트를 진행한다.
    # async_client의 base url은 http://test로 설정되어 있다.
    # async_client에 API call 때리듯이, post를 날려서 response를 받아온다.

    # Assert
    # json_response 결과를 검사한다.
    assert response.status_code == 200  # response의 status code가 200이어야 한다.
    # user_id는 랜덤하게 생성되기 때문에 검사하지 않는다.
    assert (
        json_response["data"]["userName"] == user_dto.user_name
    )  # response의 data의 userName이 user_dto의 user_name과 같아야 한다.
    assert (
        json_response["data"]["userRole"] == user_dto.user_role.value
    )  # response의 data의 userRole이 user_dto의 user_role과 같아야 한다.


@pytest.mark.parametrize(  # 파라미터라이즈를 통해 여러 케이스를 한 번에 테스트할 수 있다.
    "user_name,user_role",
    [
        ("test_username", UserRole.STUDENT),
    ],
)
async def test_create_user_student_200(
    container: Container,
    async_client: AsyncClient,
    user_service_mock: UserService,
    user_name: str,
    user_role: UserRole,
):
    # Setup
    # Request
    data = UserReq(
        userName=user_name,
    )
    # Repository
    user_dto = UserDTO(
        user_id="-",
        user_name=user_name,
        user_role=user_role,
        created_at=datetime.now(),
    )
    user_service_mock.user_repository.create_student_user.return_value = user_dto
    container.user_service.override(user_service_mock)

    # Run
    headers = {"x-api-key": "test_api_key"}
    url = "/v1/user/student"
    response = await async_client.post(
        url, headers=headers, data=data.model_dump_json()
    )
    json_response = response.json()

    # Assert
    assert response.status_code == 200
    assert json_response["data"]["userName"] == user_dto.user_name
    assert json_response["data"]["userRole"] == user_dto.user_role.value


@pytest.mark.parametrize(
    "user_name,expected_error",
    [
        ("test_username", error.ERROR_400_USER_CREATION_FAILED),
    ],
)
async def test_create_user_teacher_400(  # 선생님 계정 생성 테스트. 400이 나오면 실패 케이스다.
    async_client: AsyncClient,
    user_name: str,
    expected_error: Exception,
):
    # Setup
    data = UserReq(
        userName=user_name,
    )

    # Run
    headers = {"x-api-key": "test_api_key"}
    url = "/v1/user/teacher"
    response = await async_client.post(
        url, headers=headers, data=data.model_dump_json()
    )
    json_response = response.json()

    # Assert
    assert response.status_code == 400
    assert json_response["statusCode"] == expected_error


@pytest.mark.parametrize(
    "user_name,expected_error",
    [
        ("test_username", error.ERROR_400_USER_CREATION_FAILED),
        # error.ERROR_400_USER_CREATION_FAILED에 대해 정의되어 있어야 한다.
        # repository 레벨에서 에러가 뜨도록 설정되어 있어야 한다.
    ],
)
async def test_create_user_student_400(
    async_client: AsyncClient,
    user_name: str,
    expected_error: Exception,
):
    # Setup
    data = UserReq(
        userName=user_name,
    )
    # 실제로 DB로 접속하려고 한다. 그러나 모킹된 객체가 없다. 그래서 실패한다.
    # 이 테스트를 위해서는 docker stop postgres로 DB를 꺼야 함
    # docker restart postgres로 다시 킬 수 있음

    # Run
    # mocking 부분이 없다. 왜냐하면 이 테스트는 실패 케이스를 테스트하는 것이기 때문이다.
    headers = {"x-api-key": "test_api_key"}
    url = "/v1/user/student"
    response = await async_client.post(
        url, headers=headers, data=data.model_dump_json()
    )
    json_response = response.json()

    # Assert
    assert response.status_code == 400
    assert json_response["statusCode"] == expected_error
