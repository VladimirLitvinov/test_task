import random
import string
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from api_v1.exceptions import CustomApiException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, ReferralCode, Referral
from schemas.schemas import UserCreate, UserSchema
from auth.utils import hash_password


def generate_code() -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(8))
    return random_string


async def create_user(session: AsyncSession, new_user: UserCreate) -> User:
    search_user = select(User).where(User.email == new_user.email)
    user = await session.execute(search_user)
    result = user.scalar_one_or_none()

    if result:
        raise CustomApiException(
            status_code=409, detail="Пользователь с таким email уже существует"
        )

    new_user.password = hash_password(new_user.password).decode()
    create_user = User(**new_user.dict())
    session.add(create_user)
    try:
        await session.commit()
    except IntegrityError:
        raise CustomApiException(
            status_code=409, detail="Пользователь с таким username уже существует"
        )
    return create_user


async def get_user_by_id(session: AsyncSession, id: int) -> User:
    query = select(User).where(User.id == id)
    user = await session.execute(query)
    result = user.scalar_one_or_none()
    return result


async def create_referral_code(
    session: AsyncSession, user: UserSchema, date: date
) -> ReferralCode:
    referral_code = ReferralCode(
        author_id=user.id, code=generate_code(), valid_until=date
    )
    session.add(referral_code)
    try:
        await session.commit()
    except IntegrityError:
        raise CustomApiException(status_code=409, detail="У вас уже есть промокод")
    return referral_code


async def get_referral_code_by_email(session: AsyncSession, email: str) -> ReferralCode:
    query = select(User).options(joinedload(User.code_value)).where(User.email == email)
    user = await session.execute(query)
    result = user.unique().scalar_one_or_none()
    if not result:
        raise CustomApiException(
            status_code=404, detail="Пользователь с таким email не найден"
        )
    if result.code_value is None:
        raise CustomApiException(status_code=404, detail="У пользователя ещё нет кода")

    return result.code_value


async def get_referral_code(session: AsyncSession, referral_code: str) -> ReferralCode:
    query = select(ReferralCode).where(ReferralCode.code == referral_code)
    referral_code = await session.execute(query)
    result = referral_code.scalar_one_or_none()
    if not result:
        raise CustomApiException(status_code=404, detail="Реферальный код не найден")
    return result


async def create_referral(
    session: AsyncSession, user_id: int, code_id: int
) -> Referral:
    referral = Referral(user_id=user_id, code_id=code_id)
    session.add(referral)
    await session.commit()
    await session.refresh(referral)
    return referral


async def delete_code(session: AsyncSession, user: UserSchema) -> bool:
    query = select(ReferralCode).where(ReferralCode.author_id == user.id)
    referral_code = await session.execute(query)
    result = referral_code.scalar_one_or_none()
    if not result:
        raise CustomApiException(status_code=404, detail="У вас ещё нет кода")
    await session.delete(result)
    await session.commit()
    return True


async def get_referrals(session: AsyncSession, user_id: int):
    query = (
        select(User)
        .options(
            joinedload(User.code_value)
            .joinedload(ReferralCode.referrals)
            .joinedload(Referral.user)
        )
        .where(User.id == user_id)
    )

    result = await session.execute(query)
    user = result.unique().scalar_one_or_none()

    if not user:
        raise CustomApiException(status_code=404, detail="Пользователь не найден")

    if not user.code_value:
        raise CustomApiException(
            status_code=404, detail="У пользователя нет реферального кода"
        )

    referrals = user.code_value.referrals
    if not referrals:
        raise CustomApiException(
            status_code=404, detail="У пользователя ещё нет рефералов"
        )

    referral_users = [ref.user for ref in referrals if ref.user]
    return {"users": referral_users}
