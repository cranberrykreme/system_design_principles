from services.token_bucket import TokenBucket

class RateLimiter:
    def __init__(self, capacity, refill_rate):
        self.users = {}
        self.capacity = capacity
        self.refill_rate = refill_rate
    
    def allow_request(self, user_id) -> bool:
        if user_id not in self.users:
            self.users[user_id] = TokenBucket(self.capacity, self.refill_rate)
        return self.users[user_id].allow_request()