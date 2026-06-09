from fastapi import FastAPI, Depends
from services.rate_limiter import RateLimiter
from services.limiter_algorithms.token_bucket import TokenBucket

app = FastAPI()
rate_limiter = RateLimiter(lambda: TokenBucket(capacity=5, refill_rate=0.2))

def get_rate_limiter() -> RateLimiter:
    return rate_limiter

@app.get('/make-request')
async def make_request(rate_limiter: RateLimiter = Depends(get_rate_limiter)) -> bool:
    response = rate_limiter.allow_request("chris")

    return response