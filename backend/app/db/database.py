from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

# For SQLite, use aiosqlite
if settings.database_url.startswith("sqlite"):
    engine = create_async_engine(settings.database_url.replace("sqlite://", "sqlite+aiosqlite://"), echo=True)
else:
    # For PostgreSQL, ensure we use asyncpg
    if settings.database_url.startswith("postgresql://"):
        db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    else:
        db_url = settings.database_url
    engine = create_async_engine(db_url, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
