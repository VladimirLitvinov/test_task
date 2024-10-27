from typing import Optional
import json
from datetime import datetime

from redis import asyncio as aioredis

from config import REDIS_HOST, REDIS_PORT

redis = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


class RedisCache:
    @staticmethod
    async def set_referral_code(email: str, code_data: dict, expire: int = 3600):
        code_data["cached_at"] = datetime.now().isoformat()
        await redis.set(f"referral_code:{email}", json.dumps(code_data), ex=expire)

    @staticmethod
    async def get_referral_code(email: str) -> Optional[dict]:
        data = await redis.get(f"referral_code:{email}")
        if data:
            return json.loads(data)
        return None

    @staticmethod
    async def delete_referral_code(email: str):
        await redis.delete(f"referral_code:{email}")
