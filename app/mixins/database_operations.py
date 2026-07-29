from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from app.models.urls import URLS
from app.utils.url_shortener_utils import _create_short_code
from app.log_base import get_logger

logger = get_logger(__name__)


async def _get_url_object(db_session: AsyncSession, url: str) -> Optional[URLS]:
    """
    Get the url object from db based on short_code.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The url needed to be shortened.

    Returns
    -------
    url_object: URLS
       The urls object from the database
    """
    try:
        short_code = _create_short_code(url)

        result = await db_session.execute(
            select(URLS).where(URLS.short_code == short_code)
        )

        url_object = result.scalar_one_or_none()

        if url_object:
            logger.info("Found existing URL object for short code %s", short_code)
        else:
            logger.info("No URL object found for short code %s", short_code)

        return url_object

    except SQLAlchemyError as sqlerror:
        logger.error(f"Database error reason: {sqlerror}", exc_info=True)
        raise

    except Exception as ex:
        logger.error(f"Failed to get url from db reason: {ex}", exc_info=True)
        raise


async def _get_url_object_by_short_code(
    db_session: AsyncSession, short_code: str
) -> Optional[URLS]:
    """
    Get the url object from db based on short_code.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The url needed to be shortened.

    Returns
    -------
    url_object: URLS
       The urls object from the database
    """
    try:
        result = await db_session.execute(
            select(URLS).where(URLS.short_code == short_code)
        )

        url_object = result.scalar_one_or_none()

        if url_object:
            logger.info("Found URL object for short code %s", short_code)
        else:
            logger.info("No URL object found for short code %s", short_code)

        return url_object

    except SQLAlchemyError as sqlerror:
        logger.error(f"Database error reason: {sqlerror}", exc_info=True)
        raise

    except Exception as ex:
        logger.error(f"Failed to get url from db reason: {ex}", exc_info=True)
        raise


async def _save_url_in_db(db_session: AsyncSession, url: str):
    """
    Save the url object in db based on short_code if url does not exist.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The url needed to be shortened.

    Returns
    -------
    short_code: str
       short_code of original url in db.
    """

    try:
        url_object = await _get_url_object(db_session, url)

        if url_object:
            logger.info("Using existing short code %s", url_object.short_code)
            return url_object.short_code

        short_code = _create_short_code(url)
        db_session.add(URLS(original_url=url, short_code=short_code))
        await db_session.commit()
        logger.info("Saved new URL with short code %s", short_code)
        return short_code
    except SQLAlchemyError as sqlerror:
        await db_session.rollback()
        logger.error(f"Database error : {sqlerror}", exc_info=True)
        raise
    except Exception as ex:
        await db_session.rollback()
        logger.error(f"Failed to add url in db reason: {ex}", exc_info=True)
        raise
