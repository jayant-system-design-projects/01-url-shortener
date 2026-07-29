from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.log_base import get_logger

logger = get_logger(__name__)


def _build_error_response(
    http_status_code: int,
    error_code: str,
    details: str,
) -> JSONResponse:
    """
    Build a standard API error response.

    Parameters
    ----------
    http_status_code : int
        The HTTP status code for the response.
    error_code : str
        The application error code.
    details : str
        The error message returned to the client.

    Returns
    -------
    JSONResponse
        The formatted error response.
    """
    return JSONResponse(
        status_code=http_status_code,
        content={
            "statusCode": error_code,
            "errorDetails": {
                "errorCode": error_code,
                "details": details,
            },
        },
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """
    Handle expected HTTP exceptions.

    Parameters
    ----------
    request : Request
        The incoming FastAPI request.
    exc : HTTPException
        The HTTP exception raised by the application.

    Returns
    -------
    JSONResponse
        The formatted error response.
    """
    logger.warning(
        "HTTP exception for %s %s: %s",
        request.method,
        request.url.path,
        exc.detail,
    )
    return _build_error_response(
        http_status_code=exc.status_code,
        error_code=f"{exc.status_code}01",
        details=str(exc.detail),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle request validation exceptions.

    Parameters
    ----------
    request : Request
        The incoming FastAPI request.
    exc : RequestValidationError
        The validation exception raised by FastAPI.

    Returns
    -------
    JSONResponse
        The formatted error response.
    """
    logger.warning(
        "Validation exception for %s %s: %s",
        request.method,
        request.url.path,
        exc.errors(),
    )
    return _build_error_response(
        http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="42201",
        details="Invalid request payload.",
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected application exceptions.

    Parameters
    ----------
    request : Request
        The incoming FastAPI request.
    exc : Exception
        The unexpected exception raised by the application.

    Returns
    -------
    JSONResponse
        The formatted error response.
    """
    logger.error(
        "Unhandled exception for %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return _build_error_response(
        http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="50001",
        details="Internal server error.",
    )


def setup_global_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers on the FastAPI app.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Returns
    -------
    None
        This function only registers handlers on the app.
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
