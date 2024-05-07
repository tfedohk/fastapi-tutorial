ERROR_400_CLASS_NOT_FOUND = "40000"
ERROR_400_CLASS_NOTICE_NOT_FOUND = "40001"
ERROR_400_CLASS_CREATION_FAILED = "40002"
ERROR_400_CLASS_NOTICE_CREATION_FAILED = "40003"
ERROR_400_CLASS_NOTICE_UPDATE_FAILED = "40004"
ERROR_400_CLASS_NOTICE_DELETE_FAILED = "40005"
ERROR_400_USER_CREATION_FAILED = "40006"

ERROR_401_INVALID_API_KEY = "40100"


class BaseAPIException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        """
            Exception: 최상위 파이썬 기본 Exception
            코드랑 메세지를 받아서 API에서 발생시킬 에러 객체를 만든다.
        """


class BaseAuthException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class ClassNotFoundException(BaseAPIException):
    def __init__(self):
        # super().__init__(code="40000", message="Class not found")
        """
        40000: 400에러.
        status코드는 400다.
        "우리가 어떤 엔드포인트를 찔렀는데 400에러가 났습니다." vs "400005 에러가 났습니다."="40005에러는 클래스 에러다."
        -> 커뮤니케이션시에 편하다.
        이렇게 하드 코딩하지 말고, 아래와 같이 한다.
        """
        super().__init__(code=ERROR_400_CLASS_NOT_FOUND, message="Class not found")


class ClassCreationFailed(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_CLASS_CREATION_FAILED, message="Class creation failed"
        )


class ClassNoticeNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_CLASS_NOTICE_NOT_FOUND, message="Class Notice not found"
        )


class ClassNoticeCreationFailed(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_CLASS_NOTICE_CREATION_FAILED,
            message="Class Notice creation failed",
        )


class ClassNoticeUpdateFailed(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_CLASS_NOTICE_UPDATE_FAILED,
            message="Class Notice update failed",
        )


class ClassNoticeDeleteFailed(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_CLASS_NOTICE_DELETE_FAILED,
            message="Class Notice delete failed",
        )


class InvalidAPIKey(BaseAuthException):
    def __init__(self):
        super().__init__(code=ERROR_401_INVALID_API_KEY, message="Invalid API Key")


class UserCreationFailed(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=ERROR_400_USER_CREATION_FAILED, message="User creation failed"
        )
