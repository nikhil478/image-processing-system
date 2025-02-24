import asyncio
import signal
import logging
from fastapi import FastAPI
from app.core import engine
from app.models import Base
from app.api import router
from app.core.redis import init_redis, close_redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

shutdown_called = False

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_redis()
    logger.info("Redis connection established.")

@app.on_event("shutdown")
async def shutdown():
    global shutdown_called
    if not shutdown_called:
        shutdown_called = True
        logger.info("Disposing database engine...")
        try:
            await engine.dispose()
            logger.info("Database engine disposed successfully.")
        except Exception as e:
            logger.error(f"Error disposing database engine: {e}")
        await close_redis()
        logger.info("Redis connection closed.")

def handle_exit(*args):
    logger.info("Received termination signal. Shutting down gracefully...")
    
    async def shutdown():
        await engine.dispose()
        sys.exit(0)

    asyncio.run(shutdown())

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)