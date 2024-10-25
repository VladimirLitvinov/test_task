from pydantic import BaseModel, ConfigDict
from http import HTTPStatus


class ResponseSchema(BaseModel):
    result: bool = True
    model_config = ConfigDict(from_attributes=True)


class ConflictResponseSchema(ResponseSchema):
    result: bool = False
    error_type: str = HTTPStatus.CONFLICT  # 409
    error_message: str = "Пользователь с таким email уже существует"


class UnauthorizedResponseSchema(ResponseSchema):
    result: bool = False
    error_type: str = HTTPStatus.UNAUTHORIZED  # 401
    error_message: str = "Неверный email или пароль"


class IntegrityErrorResponseSchema(ResponseSchema):
    result: bool = False
    error_type: str = HTTPStatus.CONFLICT  # 409
    error_message: str = "У вас уже есть код"


class NotFoundReferralCodeSchema(ResponseSchema):
    result: bool = False
    error_type: str = HTTPStatus.NOT_FOUND  # 404
    error_message: str = "У пользователя ещё нет кода"
