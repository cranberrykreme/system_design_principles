class RateLimiter:
    def __init__(self, algorithm):
        self.users = {}
        self.algorithm = algorithm
    
    def allow_request(self, user_id) -> bool:
        if user_id not in self.users:
            self.users[user_id] = self.algorithm()
        return self.users[user_id].allow_request()
        