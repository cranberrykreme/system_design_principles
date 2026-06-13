from core.limiter_algorithms.base import RateLimitStrategy


class RateLimiter:

    def __init__(self, strategy: RateLimitStrategy):
        self.strategy = strategy

    async def allow_request(self, key: str) -> bool:
        return await self.strategy.allow_request(key)