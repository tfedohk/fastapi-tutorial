from dependency_injector import providers, containers

from app.core.config import Config

from app import services  # 주입 대상
from app import repositories  # 주입 대상
from app.core.redis import RedisCache  # 주입 대상


class Container(containers.DeclarativeContainer):
    config: Config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=[  # 주입할 것들이 있는 곳
            "app.core",
            "app.routers",
        ]
    )

    # redis
    redis_cache = providers.Singleton(RedisCache)

    # repositories
    class_repository = providers.Factory(repositories.ClassRepository)
    user_repository = providers.Factory(repositories.UserRepository)

    # services
    class_service = providers.Factory(
        services.ClassService, class_repository=class_repository
    )
    user_service = providers.Factory(
        services.UserService, user_repository=user_repository
    )
