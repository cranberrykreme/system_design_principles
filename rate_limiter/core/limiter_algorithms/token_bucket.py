import time
from core.storage.base import RateLimitStorage
from core.limiter_algorithms.base import RateLimitStrategy
from rate_limiter.core.utils.get_storage_key import get_key


class TokenBucket(RateLimitStrategy):

    def __init__(self, storage: RateLimitStorage, capacity: int, refill_rate: float):
        self.storage = storage
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second

    async def allow_request(self, key: str) -> bool:
        bucket_key = get_key(key)

        bucket = await self._load(bucket_key)

        now = time.time()

        self._refill(bucket, now)

        allowed = self._consume(bucket)

        await self._save(bucket_key, bucket)

        return allowed

    # -----------------------
    # internal helpers
    # -----------------------

    def _refill(self, bucket: dict, now: float) -> None:
        elapsed = now - bucket["last"]

        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + elapsed * self.refill_rate
        )

        bucket["last"] = now

    def _consume(self, bucket: dict) -> bool:
        if bucket["tokens"] < 1:
            return False

        bucket["tokens"] -= 1
        return True

    async def _load(self, key: str) -> dict:
        data = await self.storage.get(key)

        if data is None:
            return {
                "tokens": self.capacity,
                "last": time.time()
            }

        return data

    async def _save(self, key: str, bucket: dict) -> None:
        # TTL keeps stale buckets from accumulating forever
        await self.storage.set(key, bucket, ttl=60)