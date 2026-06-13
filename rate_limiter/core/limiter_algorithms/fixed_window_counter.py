from datetime import datetime
from core.storage.base import RateLimitStorage
from core.limiter_algorithms.base import RateLimitStrategy
from core.utils.get_storage_key import get_key

class FixedWindowCounter(RateLimitStrategy):
    def __init__(self, storage: RateLimitStorage, capacity: int, refill_rate: float):
        self.storage = storage
        self.capacity = capacity
        _ = refill_rate

    async def allow_request(self, key: str) -> bool:
        window_key = get_key(key=key)
        window = await self._load(window_key)
        self._refill(window=window)
        allowed = self._consume(window=window)

        await self._save(window_key, window)

        return allowed
    
    # Helper methods

    async def _load(self, key: str) -> dict:
        data = await self.storage.get(key)

        if data is None:
            return {
                "tokens": self.capacity,
                "last": datetime.now().replace(second=0, microsecond=0).isoformat()
            }

        return data

    def _refill(self, window: dict) -> None:
        now = datetime.now().replace(second=0, microsecond=0).isoformat()
        if now != window["last"]:
            window["tokens"] = self.capacity
            window["last"] = now

    def _consume(self, window: dict) -> bool:
        if window["tokens"] < 1:
            return False
        
        window["tokens"] -= 1
        return True
    
    async def _save(self, key: str, window: dict) -> None:
        await self.storage.set(key, window, ttl=60)
