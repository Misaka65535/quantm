from typing import Generic, TypeVar, Optional, Any
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponseModel(BaseModel):
    """
    Base info response model
    """
    code: int
    message: str


class ResponseModel(BaseResponseModel, Generic[T]):
    """
    General response model
    """
    data: Optional[T] = None


def resp_success(data: Any = None, message: str = "OK") -> ORJSONResponse:
    """
    Response success
    """
    return ORJSONResponse(
        status_code=200,
        content=ResponseModel(code=0, message=message, data=data).dict()
    )


def resp_error(data: Any = None, code: int = 1, message: str = "Error") -> ORJSONResponse:
    """
    Response error
    """
    return ORJSONResponse(
        status_code=200,
        content=ResponseModel(code=code, message=message, data=data).dict()
    )


def server_error(data: Any = None, status_code=500, code: int = 1, message: str = "Error") -> ORJSONResponse:
    """
    Server response error
    """
    return ORJSONResponse(
        status_code=status_code,
        content=ResponseModel(code=code, message=message, data=data).dict()
    )
