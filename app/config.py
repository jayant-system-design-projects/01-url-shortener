from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # Database Configuration
    ASYNC_DATABASE_URL = f'postgresql+asyncpg://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOSTNAME")}:{os.getenv("DB_PORT_NUMBER")}/{os.getenv("DB_DATABASE_NAME")}'
    POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
    MAX_OVERFLOW_POOL = int(os.getenv("MAX_OVERFLOW_POOL", 5))
    DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", 15))
    DB_POOL_RECYCLE_TIME = int(os.getenv("DB_POOL_RECYCLE_TIME", 1800))
