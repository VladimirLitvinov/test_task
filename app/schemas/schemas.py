from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    model_config = ConfigDict(strict=True)
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    password: str
    email: EmailStr


class UserSearchSchema(BaseModel):
    email: EmailStr
