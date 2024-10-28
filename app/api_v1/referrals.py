from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from schemas.schemas import UserSearchSchema
from database.crud import get_referral_code_by_email, get_referrals
from schemas.exceptions import NotFoundReferralCodeSchema
from schemas.referrals import CreateReferralSchema
from .utils import create_referral_user
from schemas.responses import (
    ReferralResponseSchema,
    CodeForUserResponseSchema,
    ReferralListResponseSchema,
)

router = APIRouter(tags=["referrals"])


@router.get("/{user_id}", response_model=ReferralListResponseSchema)
async def get_user_referrals(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    referrals = await get_referrals(session, user_id)
    return referrals


@router.post(
    "/referral_code",
    status_code=200,
    response_model=CodeForUserResponseSchema,
    responses={404: {"model": NotFoundReferralCodeSchema}},
)
async def get_referral_code(
    email: UserSearchSchema, session: AsyncSession = Depends(get_async_session)
):
    code = await get_referral_code_by_email(session, email.email)
    return code


@router.post("/register", status_code=201, response_model=ReferralResponseSchema)
async def register_referral(
    referral: CreateReferralSchema, session: AsyncSession = Depends(get_async_session)
):
    new_referral = await create_referral_user(session, referral)
    return new_referral
