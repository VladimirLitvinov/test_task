from pydantic import BaseModel
from .schemas import UserCreate


class CreateReferralSchema(BaseModel):
    referral_code: str
    user: UserCreate
