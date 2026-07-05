from typing import Annotated
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import Request, APIRouter
from fastapi import Depends
from app.services.url_shortener_service import (
    create_redirect_url_handler,
    create_shorten_url_handler,
)
from app.database import get_async_db_session
from app.schemas.urls_request_schemas import CreateShortenURLRequest
from app.schemas.urls_response_schemas import CreateShortenURLResponse

shorten_url_router = APIRouter()


@shorten_url_router.post("/shortenURL", response_model=CreateShortenURLResponse)
async def create_shorten_url(
    shorten_url_request: CreateShortenURLRequest,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
):
    base_api_url = str(request.base_url)
    return await create_shorten_url_handler(
        db_session, str(shorten_url_request.url), base_api_url
    )


@shorten_url_router.get("/shortenURL/{checksum}")
async def redirect_url(
    checksum: str, db_session: AsyncSession = Depends(get_async_db_session)
):
    original_url = await create_redirect_url_handler(db_session, checksum)

    return RedirectResponse(url=original_url, status_code=302)
