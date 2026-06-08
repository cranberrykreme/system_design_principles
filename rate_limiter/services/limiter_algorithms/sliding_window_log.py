from datetime import datetime, timedelta
from collections import deque

class SlidingWindowLog:
    def __init__(self, capacity):
        self.capacity = capacity
        self.request_times = deque()

    def allow_request(self) -> bool:
        self._drain()
        now = datetime.now()
        if len(self.request_times) < self.capacity:
            self.request_times.append(now)
            return True
        return False
    
    def _drain(self) -> None:
        cutoff = datetime.now() - timedelta(minutes=1)
        while self.request_times and self.request_times[0] < cutoff:
            self.request_times.popleft()
