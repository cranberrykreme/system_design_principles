import time
from services.rate_limiter import RateLimiter

if __name__ == "__main__":
    rl = RateLimiter(capacity=5, refill_rate=1)
    user = 'chris'
    for i in range(15):
        print(i, rl.allow_request(user))
        time.sleep(0.2)