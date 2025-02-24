from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.core.config import settings
from sqlalchemy import create_engine

engine = create_async_engine(settings.DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql"), echo=True)
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
