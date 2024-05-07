import pytest
from unittest.mock import AsyncMock

from httpx import AsyncClient

from app.main import create_app
from app.core.container import Container
from app.services import UserService, ClassService
from app.repositories import UserRepository, ClassRepository


@pytest.fixture
def container() -> Container:
    # app/main.py에서 빼놓은 container다.
    # 생성 후 리턴
    return Container()


@pytest.fixture
def async_client(container) -> AsyncClient:  # 컨테이너를 실제로 가져다 쓰는 부분
    # fastAPI앱을 테스트하기 위한 하나의 객체로 만들어준다.
    # 서비스를 실제로 띄우지 않은 채로 객체로 만들어서 호출을 받을 수 있는 상태로 만든다.
    # httpx를 쓴다.
    app = create_app(container)  # app/main.py의 create_app.
    return AsyncClient(app=app, base_url="http://test")
    # 통합 테스트 시에 async_client를 이용해서 엔드포인트별로 콜을 날린다.


@pytest.fixture
def user_repository_mock():
    # 모킹. 유저 레포 외 클래스 레포 등을 흉내내는 목 객체를 정의한 것.
    # 비동기 함수를 쓸 것이기 때문에 에이싱크목을 쓴다.
    # 그냥 def를 쓴다면 asyncmock이 아니라 그냥 mock을 쓴다.
    return AsyncMock(spec=UserRepository)
    # 테스트 할 때 직접 DB에 접근하지 않고, 이 모킹된 객체를 사용한다.
    # 특정 값이 나오도록 주입하고서 실제로 처리되는지를 살펴볼 목적이다.


@pytest.fixture
def class_repository_mock():
    return AsyncMock(spec=ClassRepository)


@pytest.fixture
def user_service_mock(user_repository_mock):
    # 얘는 모킹할 게 없다. 이미 user_repository_mock에서 하고 있기 때문.
    return UserService(user_repository=user_repository_mock)


@pytest.fixture
def class_service_mock(class_repository_mock):
    return ClassService(class_repository=class_repository_mock)
