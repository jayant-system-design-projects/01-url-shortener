import redis.asyncio as aioredis
from app.config import Config
from app.redis_connector import get_redis_async_connection


async def _redis_prune_schedule_task() -> bool:
    """
    This function do get prune all invalid or unpopular url
    from the actual redis cache that are not used frequently after certain time.

    Parameters
    ----------
    None

    Returns
    -------
    bool:
        True if pipeline is successfully removed as the are unpopular.
    """
    redis_connect: aioredis.Redis = get_redis_async_connection()

    async with redis_connect.pipeline() as r_p:
        valid_short_code = await r_p.zrange(Config.REDIS_URL_CLICK_TRACK_KEY, 0, -1)

        all_short_codes = await r_p.zrange(Config.REDIS_URL_TRACK_KEY, 0, -1)

        to_prune_short_code = set(all_short_codes) - set(valid_short_code)

        if to_prune_short_code:
            r_p.hdel(Config.REDIS_URL_TRACK_KEY, *to_prune_short_code)
    return True
