from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from app.models.urls import URLS
from app.utils.url_shortener_utils import _create_checksum
from app.log_base import get_logger

logger = get_logger(__name__)


async def _get_url_object(db_session: AsyncSession, url: str) -> Optional[URLS]:
    """
    Get the url object from db based on checksum.

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
        checksum = _create_checksum(url)

        result = await db_session.execute(select(URLS).where(URLS.checksum == checksum))

        url_object = result.scalar_one_or_none()

        return url_object

    except SQLAlchemyError as sqlerror:
        logger.error(f"Database error reason: {sqlerror}", exc_info=True)
        raise

    except Exception as ex:
        logger.error(f"Failed to get url from db reason: {ex}", exc_info=True)
        raise


async def _get_url_object_by_checksum(
    db_session: AsyncSession, checksum: str
) -> Optional[URLS]:
    """
    Get the url object from db based on checksum.

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
        result = await db_session.execute(select(URLS).where(URLS.checksum == checksum))

        url_object = result.scalar_one_or_none()

        return url_object

    except SQLAlchemyError as sqlerror:
        logger.error(f"Database error reason: {sqlerror}", exc_info=True)
        raise

    except Exception as ex:
        logger.error(f"Failed to get url from db reason: {ex}", exc_info=True)
        raise


async def _save_url_in_db(db_session: AsyncSession, url: str):
    """
    Save the url object in db based on checksum if url does not exist.

    Parameters
    ----------
    db_session: AsyncSession
       The async session object of database.
    url: str
       The url needed to be shortened.

    Returns
    -------
    checksum: str
       Checksum of original url in db.
    """

    try:
        url_object = await _get_url_object(db_session, url)

        if url_object:
            return url_object.checksum

        checksum = _create_checksum(url)
        db_session.add(URLS(original_url=url, checksum=checksum))
        await db_session.commit()
        return checksum
    except SQLAlchemyError as sqlerror:
        await db_session.rollback()
        logger.error(f"Database error : {sqlerror}", exc_info=True)
        raise
    except Exception as ex:
        await db_session.rollback()
        logger.error(f"Failed to add url in db reason: {ex}", exc_info=True)
        raise
