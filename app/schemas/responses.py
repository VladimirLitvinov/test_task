from typing import List

from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from schemas.schemas import UserBase


class BaseResponse(BaseModel):
    result: bool = True
    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(BaseResponse):
    id: int = Field(..., alias="id")
    email: str = Field(..., alias="email")


class ReferralResponseSchema(BaseResponse):
    id: int = Field(..., alias="id")
    user_id: int = Field(..., alias="user_id")
    code_id: int = Field(..., alias="code_id")


class ReferralCodeResponseSchema(BaseResponse):
    id: int = Field(..., alias="id")
    author_id: int = Field(..., alias="author_id")
    code: str = Field(..., alias="code")
    valid_until: date = Field(..., alias="valid_until")


class CodeForUserResponseSchema(BaseResponse):
    code: str = Field(..., alias="code")
    valid_until: date = Field(..., alias="valid_until")


class ReferralListResponseSchema(BaseResponse):
    users: List[UserBase]
