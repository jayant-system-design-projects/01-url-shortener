from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import Config

async_engine = create_async_engine(
    Config.ASYNC_DATABASE_URL,
    pool_size=Config.POOL_SIZE,
    max_overflow=Config.MAX_OVERFLOW_POOL,
    pool_timeout=Config.DB_POOL_TIMEOUT,
    pool_recycle=Config.DB_POOL_RECYCLE_TIME,
    pool_pre_ping=True,
    echo=False,
)
async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_async_db_session():
    async with async_session() as async_db_session:
        yield async_db_session
