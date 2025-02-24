from logging.config import fileConfig
import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

from app.models.base import Base
from app.models.processed_image import ProcessedImage
from app.models.processing_request import ProcessingRequest
from app.core.config import settings

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

connectable = create_async_engine(settings.DATABASE_URL, echo=True)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async support."""
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())