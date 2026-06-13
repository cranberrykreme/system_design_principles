import json
from redis.asyncio import Redis
from .base import RateLimitStorage


class RedisStorage(RateLimitStorage):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        value = await self.redis.get(key)   # ✅ await FIRST

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        return json.loads(value)            # ✅ THEN parse JSON

    async def set(self, key: str, value, ttl: int):
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl
        )

    async def incr(self, key: str):
        return await self.redis.incr(key)