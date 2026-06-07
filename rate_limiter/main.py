import asyncio
from services.rate_limiter import RateLimiter
from services.limiter_algorithms.token_bucket import TokenBucket
from services.limiter_algorithms.fixed_window_counter import FixedWindowCounter
from services.limiter_algorithms.sliding_window_counter import SlidingWindowCounter

async def _run_limiter(algorithm_name, limiter, user, iterations=180, sleep_time=0.2):
    true_count, false_count = 0, 0
    for i in range(iterations):
        print(algorithm_name)
        result = limiter.allow_request(user)
        print(i, result)
        if result:
            true_count += 1
        else:
            false_count += 1
        await asyncio.sleep(sleep_time)
    return algorithm_name, true_count, false_count

async def main():
    user = 'chris'

    task1 = _run_limiter(
        'TOKEN BUCKET',
        RateLimiter(lambda: TokenBucket(capacity=5, refill_rate=1)),
        user
    )
    task2 = _run_limiter(
        'FIXED WINDOW COUNTER',
        RateLimiter(lambda: FixedWindowCounter(capacity=5)),
        user
    )
    task3 = _run_limiter(
        'SLIDING WINDOW COUNTER',
        RateLimiter(lambda: SlidingWindowCounter(capacity=5)),
        user
    )

    results = await asyncio.gather(task1, task2, task3)

    for name, true_count, false_count in results:
        print(f"\n{name}")
        print(f"allowed: {true_count}")
        print(f"blocked: {false_count}")

if __name__ == "__main__":
    asyncio.run(main())
