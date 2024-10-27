from datetime import datetime, timedelta

import jwt
import bcrypt

from config import (
    ALGORITHM,
    PUBLIC_KEY_PATH,
    PRIVATE_KEY_PATH,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def encode_jwt(
    payload: dict,
    private_key: str = PRIVATE_KEY_PATH.read_text(),
    algorithm: str = ALGORITHM,
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm)
    return encoded_jwt


def decode_jwt(
    token: str,
    public_key: str = PUBLIC_KEY_PATH.read_text(),
    algorithm: str = ALGORITHM,
):
    decoded_jwt = jwt.decode(token, public_key, algorithm)
    return decoded_jwt


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
