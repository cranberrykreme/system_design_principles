from datetime import datetime

class FixedWindowCounter:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tokens = capacity
        self.window_start = datetime.now().replace(second=0, microsecond=0)

    def allow_request(self) -> bool:
        self._refill()

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
    
    def _refill(self) -> None:
        now = datetime.now().replace(second=0, microsecond=0)
        if now != self.window_start:
            self.tokens = self.capacity
            self.window_start = now
