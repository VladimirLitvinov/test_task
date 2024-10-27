from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from database.crud import create_user
from schemas.schemas import UserCreate
from schemas.exceptions import ConflictResponseSchema
from schemas.responses import UserResponseSchema

router = APIRouter(tags=["users"])


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=201,
    responses={409: {"model": ConflictResponseSchema}},
)
async def register(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    user = await create_user(session, new_user)
    return user
