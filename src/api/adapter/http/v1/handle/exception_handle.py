from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from src.api.adapter.http.v1.payload.response.error_response import (
    ErrorResponse,
    ErrorDetails,
)
from src.api.adapter.http.v1.log.error_log import ErrorLog
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.core.exception.rate_limit_exeception import (
    RateLimitException,
)
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.core.exception.unauthorized_exception import UnauthorizedException


async def bad_request_exception(request: Request, exception: BadRequestException):

    ErrorLog.handler(request, "Bad Request")

    return _response_bad_request_exception(exception.get_params())


async def request_validation_exception(
    request: Request, exception: RequestValidationError
):

    ErrorLog.handler(request, "Request Validation Error")

    errors = []
    for error in exception.errors():
        field_path = error["loc"][1:]
        detailed_path = ".".join(str(x) for x in field_path if isinstance(x, str))
        message = error["msg"]
        formatted_error = f"{message} in {detailed_path}"
        errors.append(formatted_error)

    return _response_bad_request_exception(errors)


def _response_bad_request_exception(params: list):
    error_response = ErrorResponse(
        errorDetails=[
            ErrorDetails(statusCode="ERROR_001", message=f"Bad Request", details=params)
        ]
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error_response),
    )


async def internal_server_error_exception(
    request: Request, exception: InternalServerErrorException
):
    ErrorLog.handler(
        request,
        (
            exception.message
            if exception.message
            else "An unexpected server error occurred"
        ),
        exception=exception.exception,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            ErrorResponse(
                errorDetails=[
                    ErrorDetails(
                        statusCode="ERROR_002", message="Internal Server Error"
                    )
                ]
            )
        ),
    )


async def rate_limit_exception(request: Request, exception: RateLimitException):
    ErrorLog.handler(request, "Exceeded rate limit", exception=exception.exception)

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=jsonable_encoder(
            ErrorResponse(
                errorDetails=[
                    ErrorDetails(
                        statusCode="ERROR_003",
                        message="Exceeded rate limit, please retry later",
                    )
                ]
            )
        ),
    )


async def not_found_exception(request: Request, exception: NotFoundException):
    ErrorLog.handler(request, "Not Found")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(
            ErrorResponse(
                errorDetails=[
                    ErrorDetails(
                        statusCode="ERROR_004",
                        message=f"{exception.get_entity()} not found",
                    )
                ]
            ),
            exclude_none=True,
        ),
    )


async def unauthorized_exception(request: Request, exception: UnauthorizedException):
    ErrorLog.handler(
        request,
        (exception.message if exception.message else "Unauthorized access"),
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            ErrorResponse(
                errorDetails=[
                    ErrorDetails(
                        statusCode="ERROR_401",
                        message="Unauthorized access",
                    )
                ]
            ),
            exclude_none=True,
        ),
    )
