from redis.asyncio import Redis

def create_redis() -> Redis:
    return Redis(
        host="redis",   # Docker service name
        port=6379,
        decode_responses=True
    )