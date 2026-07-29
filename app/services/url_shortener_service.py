from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis
from app.mixins.database_operations import (
    _get_url_object_by_short_code,
    _save_url_in_db,
)
from app.mixins.redis_operations import (
    _add_url_in_redis,
    _get_url_and_add_click_in_redis,
)
from app.schemas.urls_response_schemas import CreateShortenURLResponse, Data
from app.log_base import get_logger

logger = get_logger(__name__)


async def create_shorten_url_handler(
    db_session: AsyncSession, redis_session: aioredis.Redis, url: str, base_api_url: str
) -> CreateShortenURLResponse:
    """
    Create a shortened url for original url.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    redis_session: aioredis.Redis
      The async session object of redis.
    url: str
       The original longer url.
    base_api_url: str
       The base url of route.

    Returns
    -------
    shortened_url: CreateShortenURLResponse
      Return a shortened url.
    """
    try:
        logger.info("Creating shortened URL")
        short_code = await _save_url_in_db(db_session, url)
        await _add_url_in_redis(redis_session, short_code, url)
        shortened_url = f"{base_api_url}shortenURL/{short_code}"
        logger.info("Created shortened URL for short code %s", short_code)
        return CreateShortenURLResponse(
            statusCode="20001", data=Data(shortened_url=shortened_url)
        )
    except HTTPException:
        raise
    except Exception as ex:
        logger.error("Failed to create shortened URL: %s", ex, exc_info=True)
        raise


async def create_redirect_url_handler(
    db_session: AsyncSession, redis_session: aioredis.Redis, short_code: str
) -> str:
    """
    Create a shortened url for original url.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    redis_session: aioredis.Redis
       The async session object of redis.
    short_code: str
       The generated short code.

    Returns
    -------
    original_url: str
      Return the original url.
    """
    try:
        logger.info("Resolving short code %s", short_code)
        redis_cached_url = await _get_url_and_add_click_in_redis(
            redis_session, short_code
        )
        if redis_cached_url:
            logger.info("Resolved short code %s from Redis cache", short_code)
            return redis_cached_url
        url_object = await _get_url_object_by_short_code(db_session, short_code)
        if not url_object:
            logger.warning("Short code %s was not found", short_code)
            raise HTTPException(status_code=404, detail="Short URL not found")
        logger.info("Resolved short code %s from database", short_code)
        return url_object.original_url
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(
            "Failed to get original URL for short code %s: %s",
            short_code,
            ex,
            exc_info=True,
        )
        raise
