from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base
from app.api import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
