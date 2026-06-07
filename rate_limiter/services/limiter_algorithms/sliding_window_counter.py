from datetime import datetime

class SlidingWindowCounter:
    WINDOW_SIZE = 60

    def __init__(self, capacity):
        self.capacity = capacity
        self.curr_window_tokens_used = 0
        self.prev_window_tokens_used = 0
        self.curr_window_start = datetime.now().replace(second=0, microsecond=0)

    def allow_request(self) -> bool:
        avail_tokens = self._get_available_tokens()
        if avail_tokens >= 1:
            self.curr_window_tokens_used += 1
            return True
        return False
    
    def _get_available_tokens(self):
        self._refill()
        elapsed_seconds = (datetime.now() - self.curr_window_start).total_seconds()
        perc_from_prev_window = 1 - (elapsed_seconds / self.WINDOW_SIZE)

        weight_prev = max(0.0, min(1.0, perc_from_prev_window))

        used = weight_prev*self.prev_window_tokens_used + self.curr_window_tokens_used

        return self.capacity - used
    
    def _refill(self):
        now = datetime.now().replace(second=0, microsecond=0)
        if now != self.curr_window_start:
            self.curr_window_start = now
            self.prev_window_tokens_used = self.curr_window_tokens_used
            self.curr_window_tokens_used = 0