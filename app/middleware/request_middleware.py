from fastapi import Request, Response
from app.utils.filters import RequestIDFilter
from uuid import uuid4
from app.log_base import get_logger


async def request_middleware(request: Request, call_next) -> Response:
    """
    This is a custom middleware that handles incoming request
    and add correct request id var for that task and return same in response.

    Parameters
    -----------
    request: Request
        This is the fastapi request parameter.
    call_next: any
        This is call next param to call route.

    response: Response
        This is http or https api call response.
    """
    headers = request.headers

    # Set request id and security token
    request_id = headers.get("requestId", False) or str(uuid4())
    RequestIDFilter.set_request_id(request_id)

    logger = get_logger("shorten url service")

    logger.info(f"Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    # Return the request ID back to the client
    response.headers["requestId"] = request_id

    return response
