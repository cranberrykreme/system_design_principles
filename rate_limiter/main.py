from fastapi import FastAPI
from contextlib import asynccontextmanager

from infra.redis_client import create_redis
from core.storage.redis import RedisStorage
from core.limiter_algorithms.token_bucket import TokenBucket
from core.rate_limiter import RateLimiter
from api.rate_limit_controller import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --------------------
    # Startup
    # --------------------
  
    redis = create_redis()

    storage = RedisStorage(redis)

    strategy = TokenBucket(
        storage=storage,
        capacity=5,
        refill_rate=0.2
    )

    app.state.rate_limiter = RateLimiter(strategy)

    yield

    # --------------------
    # Shutdown
    # --------------------
    await redis.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router)