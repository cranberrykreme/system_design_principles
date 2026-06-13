from datetime import datetime
from core.storage.base import RateLimitStorage
from core.limiter_algorithms.base import RateLimitStrategy
from core.utils.get_storage_key import get_key

class SlidingWindowCounter(RateLimitStrategy):
    WINDOW_SIZE = 60

    def __init__(self, storage: RateLimitStorage, capacity: int, refill_rate: float):
        self.storage = storage
        self.capacity = capacity
        _ = refill_rate

    async def allow_request(self, key: str) -> bool:
        window_key = get_key(key=key)
        window = await self._load(window_key)

        avail_tokens = self._get_available_tokens(window=window)
        allowed = self._consume(window=window, avail_tokens=avail_tokens)
        
        await self._save(window_key, window)

        return allowed
    
    # Helper methods

    async def _load(self, key: str) -> dict:
        data = await self.storage.get(key)

        if data is None:
            return {
                "prev_count": 0,
                "curr_count": 0,
                "curr_start": datetime.now().replace(second=0, microsecond=0).isoformat()
            }

        return data

    def _get_available_tokens(self, window: dict):
        self._refill(window=window)
        elapsed_seconds = (datetime.now() - datetime.fromisoformat(window["curr_start"])).total_seconds()
        perc_from_prev_window = 1 - (elapsed_seconds / self.WINDOW_SIZE)

        weight_prev = max(0.0, min(1.0, perc_from_prev_window))

        used = weight_prev*window["prev_count"] + window["curr_count"]

        return self.capacity - used
    
    def _refill(self, window: dict):
        now = datetime.now().replace(second=0, microsecond=0)
        windows_elapsed = (now - datetime.fromisoformat(window["curr_start"])).total_seconds() // self.WINDOW_SIZE

        if windows_elapsed == 0:
            return
        elif windows_elapsed == 1:
            window["prev_count"] = window["curr_count"]
        else:
            window["prev_count"] = 0
        
        window["curr_start"] = now.isoformat()
        window["curr_count"] = 0
        
    def _consume(self, window: dict, avail_tokens: int) -> bool:
        if avail_tokens < 1:
            return False
        
        window["curr_count"] += 1
        return True
    
    async def _save(self, key: str, window: dict) -> None:
        await self.storage.set(key, window, ttl=60)