from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi.routing import Request, APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis
from app.services.url_shortener_service import (
    create_redirect_url_handler,
    create_shorten_url_handler,
)
from app.database import _get_async_db_session
from app.redis_connector import _get_redis_async_connection
from app.schemas.urls_request_schemas import CreateShortenURLRequest
from app.schemas.urls_response_schemas import CreateShortenURLResponse

shorten_url_router = APIRouter()


@shorten_url_router.post("/shortenURL", response_model=CreateShortenURLResponse)
async def create_shorten_url(
    shorten_url_request: CreateShortenURLRequest,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(_get_async_db_session)],
    redis_session: Annotated[aioredis.Redis, Depends(_get_redis_async_connection)],
):
    """
    Create a shortened URL.

    Parameters
    ----------
    shorten_url_request : CreateShortenURLRequest
        The request body containing the original URL.
    request : Request
        The incoming FastAPI request.
    db_session : AsyncSession
        The async database session.
    redis_session : aioredis.Redis
        The async Redis session.

    Returns
    -------
    CreateShortenURLResponse
        The shortened URL response.
    """
    base_api_url = str(request.base_url)
    return await create_shorten_url_handler(
        db_session, redis_session, str(shorten_url_request.url), base_api_url
    )


@shorten_url_router.get("/shortenURL/{short_code}")
async def redirect_url(
    short_code: str,
    db_session: Annotated[AsyncSession, Depends(_get_async_db_session)],
    redis_session: Annotated[aioredis.Redis, Depends(_get_redis_async_connection)],
):
    """
    Redirect a short code to its original URL.

    Parameters
    ----------
    short_code : str
        The generated short code.
    db_session : AsyncSession
        The async database session.
    redis_session : aioredis.Redis
        The async Redis session.

    Returns
    -------
    RedirectResponse
        The redirect response for the original URL.
    """
    original_url = await create_redirect_url_handler(
        db_session, redis_session, short_code
    )

    return RedirectResponse(url=original_url, status_code=302)
