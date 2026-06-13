from datetime import datetime
from core.storage.base import RateLimitStorage
from core.limiter_algorithms.base import RateLimitStrategy
from core.utils.get_storage_key import get_key

class LeakyBucket(RateLimitStrategy):
    def __init__(self, storage: RateLimitStorage, capacity: int, refill_rate: float):
        self.storage = storage
        self.capacity = capacity
        self.drain_rate = refill_rate

    async def allow_request(self, key: str) -> bool:
        bucket_key = get_key(key=key)
        bucket = await self._load(bucket_key)
        self._drain(bucket=bucket)
        allowed = self._consume(bucket=bucket)

        await self._save(bucket_key, bucket)

        return allowed
    
    # Helper methods

    async def _load(self, key: str) -> dict:
        data = await self.storage.get(key)

        if data is None:
            return {
                "requests": 0,
                "last": datetime.now().replace(microsecond=0).isoformat()
            }
        return data
    
    def _drain(self, bucket: dict) -> None:
        now = datetime.now().replace(microsecond=0).isoformat()
        delta = (datetime.fromisoformat(now) - datetime.fromisoformat(bucket['last'])).total_seconds()
        if delta != 0:
            bucket["requests"] = max(0, bucket["requests"] - delta * self.drain_rate)
            bucket["last"] = now

    def _consume(self, bucket: dict) -> bool:
        if bucket["requests"] >= self.capacity:
            return False
        
        bucket["requests"] += 1
        return True
    
    async def _save(self, key: str, bucket: dict) -> None:
        await self.storage.set(key, bucket, ttl=60)

        
