from datetime import datetime, timedelta
from collections import deque
from core.storage.base import RateLimitStorage
from core.limiter_algorithms.base import RateLimitStrategy
from core.utils.get_storage_key import get_key

class SlidingWindowLog(RateLimitStrategy):
    def __init__(self, storage: RateLimitStorage, capacity: int, refill_rate: float):
        self.storage = storage
        self.capacity = capacity
        _ = refill_rate

    async def allow_request(self, key: str) -> bool:
        window_key = key
        window = await self._load(window_key)
        self._drain(window=window)

        allow = self._consume(window=window)

        window["list"] = list(window["list"])
        await self._save(window_key, window)

        return allow
    
    # Helper methods

    async def _load(self, key: str) -> dict:
        data = await self.storage.get(key)

        if data is None:
            return {
                "requests": 0,
                "list": deque()
            }
        return {
            "requests": data["requests"],
            "list": deque(data["list"])
        }
    
    def _drain(self, window: dict) -> None:
        cutoff = datetime.now() - timedelta(minutes=1)
        while window["list"] and datetime.fromisoformat(window["list"][0]) < cutoff:
            window["requests"] -= 1
            window["list"].popleft()

    def _consume(self, window: dict) -> bool:
        now = datetime.now().isoformat()
        if window["requests"] < self.capacity:
            window["requests"] += 1
            window["list"].append(now)
            return True
        return False
    
    async def _save(self, key: str, window: dict) -> None:
        await self.storage.set(key, window, ttl=60)
