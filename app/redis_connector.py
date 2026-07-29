from typing import AsyncGenerator
import redis.asyncio as aioredis
from app.config import Config

__pool_configuration = {
    "host": Config.REDIS_HOST_NAME,
    "max_connections": Config.REDIS_MAX_CONNECTION,
    "decode_responses": True,
}

if Config.REDIS_USER_NAME:
    __pool_configuration["username"] = Config.REDIS_USER_NAME

if Config.REDIS_PASS_WORD:
    __pool_configuration["password"] = Config.REDIS_PASS_WORD

if Config.REDIS_SSL_ENABLED:
    __pool_configuration.update(
        {
            "ssl": True,
            "ssl_certfile": Config.REDIS_SSL_CERTFILE,
            "ssl_keyfile": Config.REDIS_SSL_KEYFILE,
            "ssl_ca_certs": Config.REDIS_SSL_CA_CERTS,
            "ssl_cert_reqs": "required" if Config.REDIS_SSL_CA_CERTS else "none",
        }
    )

__redis_pool = aioredis.ConnectionPool(**__pool_configuration)


def get_redis_async_connection() -> aioredis.Redis:
    """
    Create a Redis async connection.

    Returns
    -------
    aioredis.Redis
        The Redis async connection.
    """
    return aioredis.Redis(connection_pool=__redis_pool)


async def _get_redis_async_connection() -> AsyncGenerator[aioredis.Redis]:
    """
    Yield a Redis async connection for FastAPI dependency injection.

    Parameters
    ----------
    None

    Yields
    ------
    aioredis.Redis
        The Redis async connection.
    """
    async with get_redis_async_connection() as r:
        try:
            yield r
        finally:
            pass
