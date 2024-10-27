from datetime import date

from fastapi import Form, Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from api_v1.exceptions import CustomApiException
from database import User, Referral
from auth.utils import validate_password
from database.base import get_async_session
from auth import utils
from database.crud import (
    get_user_by_id,
    get_referral_code,
    create_user,
    create_referral,
)
from schemas.referrals import CreateReferralSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api-v1/auth/token",
)


async def validate_user(
    session: AsyncSession = Depends(get_async_session),
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = CustomApiException(
        status_code=401, detail="Неверный username или пароль"
    )

    query = select(User).where(User.username == username)
    user = await session.execute(query)
    result = user.scalar_one_or_none()
    if not result:
        raise unauthed_exc
    b_password = result.password.encode()
    if not validate_password(password=password, hashed_password=b_password):
        raise unauthed_exc

    return result


async def get_current_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Ошибка недействительного токена")
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_payload),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    id: int = payload.get("sub")
    user = await get_user_by_id(session, id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user


async def create_referral_user(
    session: AsyncSession, new_referral: CreateReferralSchema
) -> Referral:
    ref_code = await get_referral_code(session, new_referral.referral_code)
    if ref_code.valid_until < date.today():
        raise CustomApiException(status_code=409, detail="Реферальный код просрочен")
    user = await create_user(session, new_referral.user)
    referral = await create_referral(session, user.id, ref_code.id)
    await session.refresh(referral)
    return referral
