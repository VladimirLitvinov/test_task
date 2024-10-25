from pydantic import BaseModel
from datetime import date


class CreateCode(BaseModel):
    valid_until: date


class ReferralCodeSchema(BaseModel):
    id: int
    valid_until: date
    code: str
    author_id: int
