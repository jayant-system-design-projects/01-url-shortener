import redis.asyncio as aioredis
from app.config import Config
from app.log_base import get_logger

logger = get_logger(__name__)


async def _add_url_in_redis(
    redis_connection: aioredis.Redis,
    short_code: str,
    url: str,
) -> bool:
    """
    This function does three things:
    1. Add short code and url in url track sorted set in redis.
    2. Add short code and url in url click track sorted set in redis.
    3. Removes extra urls that are clicked less and maintain top max popular url.

    Parameters
    ----------
    redis_connection: aioredis.Redis
        This the async redis connection.
    short_code: str
        This the short code for a given url.
    url: str
        Actual url that points to given short code.

    Returns
    -------
    bool:
        True if was able to perform operation else False
    """
    try:
        redis_click_track_key = Config.REDIS_URL_CLICK_TRACK_KEY
        logger.info("Adding short code %s in Redis", short_code)

        async with redis_connection.pipeline(transaction=True) as r_p:
            r_p.hset(Config.REDIS_URL_TRACK_KEY, short_code, url)

            r_p.zincrby(redis_click_track_key, 1, short_code)

            r_p.zremrangebyrank(
                redis_click_track_key, 0, -(Config.REDIS_TOP_MAX_URL_CAPACITY + 1)
            )

            await r_p.execute()

        logger.info("Added short code %s in Redis", short_code)
        return True

    except Exception as ex:
        logger.error("Failed to add URL in Redis: %s", ex, exc_info=True)
        raise


async def _get_url_and_add_click_in_redis(
    redis_connection: aioredis.Redis, short_code: str
) -> str | None:
    """
    This function does two things.
    1. Get the url used in redis cache.
    2. Add a click count to url added to increases it's popularity.

    Parameters
    ----------
    redis_connection: aioredis.Redis
        This the async redis connection.
    short_code: str
        This the short code for a given url.

    Returns
    -------
    url: str | None
        Actual url that points to given short code if present in redis cache else None.
    """
    try:
        logger.info("Checking Redis for short code %s", short_code)
        url = await redis_connection.hget(Config.REDIS_URL_TRACK_KEY, short_code)

        if url:
            await redis_connection.zincrby(
                Config.REDIS_URL_CLICK_TRACK_KEY, 1, short_code
            )
            logger.info("Redis cache hit for short code %s", short_code)
        else:
            logger.info("Redis cache miss for short code %s", short_code)

        return url
    except Exception as ex:
        logger.error("Failed to get URL from Redis: %s", ex, exc_info=True)
        raise
