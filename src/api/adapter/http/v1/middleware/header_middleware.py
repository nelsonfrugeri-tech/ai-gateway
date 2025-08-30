import contextvars
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Callable
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)

correlation_id_var = contextvars.ContextVar("correlation_id", default=None)


class HeaderMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        correlation_id = request.headers.get("X-Correlation-ID")
        correlation_id_var.set(correlation_id)
        return await call_next(request)


def get_correlation_id():
    try:
        correlation_id = correlation_id_var.get()
        return correlation_id
    except AttributeError as error:
        raise InternalServerErrorException(
            exception=error, message="Unable to get the correlation id"
        )
