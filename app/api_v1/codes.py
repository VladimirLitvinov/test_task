from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.utils import get_current_auth_user
from database.base import get_async_session
from database.crud import create_referral_code, delete_code
from schemas.codes import CreateCode
from schemas.schemas import UserSchema
from schemas.exceptions import IntegrityErrorResponseSchema, NotFoundReferralCodeSchema
from schemas.responses import ReferralCodeResponseSchema

router = APIRouter(tags=["codes"])


@router.post(
    "/register",
    response_model=ReferralCodeResponseSchema,
    status_code=201,
    responses={409: {"model": IntegrityErrorResponseSchema}},
)
async def create_code(
    date: CreateCode,
    user: UserSchema = Depends(get_current_auth_user),
    session: AsyncSession = Depends(get_async_session),
):
    code = await create_referral_code(session, user, date.valid_until)
    return code


@router.delete(
    "delete", status_code=204, responses={404: {"model": NotFoundReferralCodeSchema}}
)
async def delete_referral_code(
    user: UserSchema = Depends(get_current_auth_user),
    session: AsyncSession = Depends(get_async_session),
):
    del_code = await delete_code(session, user)
    return del_code
