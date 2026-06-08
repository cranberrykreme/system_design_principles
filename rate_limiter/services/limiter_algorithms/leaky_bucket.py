from datetime import datetime

class LeakyBucket:
    def __init__(self, capacity, drain_rate):
        self.capacity = capacity
        self.drain_rate = drain_rate
        self.prev_request_time = datetime.now().replace(microsecond=0)
        self.request_counter = 0

    def allow_request(self) -> bool:
        self._drain()
        if self.request_counter < self.capacity:
            self.request_counter += 1
            return True
        return False
    
    def _drain(self) -> None:
        now = datetime.now().replace(microsecond=0)
        delta = (now - self.prev_request_time).total_seconds()
        if delta != 0:
            self.request_counter = max(0, self.request_counter - delta * self.drain_rate)
            self.prev_request_time = now

        
