import logging
from typing import Optional
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="N/A")
security_token_var: ContextVar[Optional[str]] = ContextVar(
    "security_token", default=None
)


class SecurityTokenFilter(logging.Filter):
    """
    Custom logging filter to append request_id to each log entry.
    """

    @staticmethod
    def set_security_token(security_token: Optional[str]):
        security_token_var.set(security_token)


class RequestIDFilter(logging.Filter):
    """
    Custom logging filter to append request_id to each log entry.
    """

    @staticmethod
    def set_request_id(request_id: str):
        request_id_var.set(request_id)

    def filter(self, record):
        record.request_id = request_id_var.get()
        return True
