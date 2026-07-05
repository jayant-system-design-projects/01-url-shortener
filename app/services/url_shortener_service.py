from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.mixins.database_operations import (
    _get_url_object_by_short_code,
    _save_url_in_db,
    _get_url_object,
)
from app.schemas.urls_response_schemas import CreateShortenURLResponse, Data


async def create_shorten_url_handler(
    db_session: AsyncSession, url: str, base_api_url: str
) -> CreateShortenURLResponse:
    """
    Create a shortened url for original url.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The original longer url.
    base_api_url: str
       The base url of route.

    Returns
    -------
    shortened_url: CreateShortenURLResponse
      Return a shortened url.
    """
    short_code = await _save_url_in_db(db_session, url)
    shortened_url = f"{base_api_url}shortenURL/{short_code}"
    return CreateShortenURLResponse(
        statusCode="20001", data=Data(shortened_url=shortened_url)
    )


async def create_redirect_url_handler(db_session: AsyncSession, short_code: str) -> str:
    """
    Create a shortened url for original url.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The original longer url.
    base_api_url: str
       The base url of route.

    Returns
    -------
    shortened_url: CreateShortenURLResponse
      Return a shortened url.
    """
    url_object = await _get_url_object_by_short_code(db_session, short_code)
    if not url_object:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return url_object.original_url
