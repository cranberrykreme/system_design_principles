from abc import ABC, abstractmethod

class RateLimitStrategy(ABC):

    @abstractmethod
    async def allow_request(self, key: str) -> bool:
        pass