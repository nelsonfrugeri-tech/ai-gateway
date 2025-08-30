from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from pydantic import ValidationError


class BadRequestException(Exception):
    def __init__(self, params: list):
        self.params = params

    def __str__(self):
        return ", ".join(self.params)

    def get_params(self):
        return self.params


class ValidationBadRequestException(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ValidationError as exception:
            details = [
                {"loc": ex["loc"], "msg": ex["msg"]} for ex in exception.errors()
            ]
            raise BadRequestException(params=details) from exception
