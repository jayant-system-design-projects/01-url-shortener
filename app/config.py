from dotenv import load_dotenv
import os

load_dotenv()


def _get_bool_env(name: str, default: bool = False) -> bool:
    """
    Get a boolean value from environment variables.

    Parameters
    ----------
    name : str
        The environment variable name.
    default : bool, optional
        The fallback value when the variable is missing.

    Returns
    -------
    bool
        The parsed boolean value.
    """
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes"}


class Config:
    # Database Configuration
    ASYNC_DATABASE_URL = f'postgresql+asyncpg://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOSTNAME")}:{os.getenv("DB_PORT_NUMBER")}/{os.getenv("DB_DATABASE_NAME")}'
    POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
    MAX_OVERFLOW_POOL = int(os.getenv("MAX_OVERFLOW_POOL", 5))
    DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", 15))
    DB_POOL_RECYCLE_TIME = int(os.getenv("DB_POOL_RECYCLE_TIME", 1800))

    # Redis Information
    REDIS_HOST_NAME = os.getenv("REDIS_HOST_NAME")
    REDIS_USER_NAME = os.getenv("REDIS_USER_NAME")
    REDIS_PASS_WORD = os.getenv("REDIS_PASS_WORD")
    REDIS_SSL_ENABLED = _get_bool_env("REDIS_SSL_ENABLED")
    REDIS_SSL_CERTFILE = os.getenv("REDIS_SSL_CERTFILE")
    REDIS_SSL_KEYFILE = os.getenv("REDIS_SSL_KEYFILE")
    REDIS_SSL_CA_CERTS = os.getenv("REDIS_SSL_CA_CERTS")
    REDIS_MAX_CONNECTION = int(os.getenv("REDIS_POOL_SIZE", 10))
    REDIS_URL_TRACK_KEY = os.getenv("REDIS_URL_TRACK_KEY", "global:site_clicks")
    REDIS_URL_CLICK_TRACK_KEY = os.getenv(
        "REDIS_URL_CLICK_TRACK_KEY", "global:site_track"
    )
    REDIS_TOP_MAX_URL_CAPACITY = int(os.getenv("REDIS_TOP_MAX_URL_CAPACITY", 10000))
    REDIS_UNPOPULAR_URL_PRUNE_TASK_TIME_IN_SECONDS = int(
        os.getenv("REDIS_UNPOPULAR_URL_PRUNE_TASK_TIME_IN_SECONDS", 3600)
    )
