import redis.asyncio as redis
from app.core.config import settings

redis_client = None

async def init_redis():
    global redis_client
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

async def close_redis():
    if redis_client:
        await redis_client.close()
