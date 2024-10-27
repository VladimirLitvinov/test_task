from fastapi import APIRouter, Depends

from api_v1.utils import validate_user
from auth import utils as auth_utils
from schemas.schemas import UserSchema
from schemas.token import Token
from schemas.exceptions import UnauthorizedResponseSchema


router = APIRouter(tags=["auth"])


@router.post(
    "/token",
    response_model=Token,
    responses={401: {"model": UnauthorizedResponseSchema}},
)
async def get_token(user: UserSchema = Depends(validate_user)):
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
    }

    access_token = auth_utils.encode_jwt(jwt_payload)
    return Token(access_token=access_token, token_type="Bearer")
