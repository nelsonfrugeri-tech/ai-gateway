from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from src.api.adapter.http.v1.payload.response.error_response import (
    ErrorResponse,
    ErrorDetails,
)
from src.api.core.exception.quota_exceeded_exception import QuotaExceededException
from src.api.core.exception.not_found_exception import NotFoundException


class MiddlewareErrorHandle:

    @staticmethod
    def internal_error(request: Request, exception: Exception):

        # TODO: CRIAR O MÉTODO ESPECIFICO PARA OS LOGS DE ERRO DO QUOTA-MIDDLEWARE
        # LogErrorHandle.handler(
        #     request=request,
        #     message="Quota Middlware Internal Error",
        #     exception=exception,
        # )

        error_response = ErrorResponse(
            errorDetails=[
                ErrorDetails(
                    statusCode="ERR_MID_001",
                    message="An error occurred while processing the request",
                )
            ]
        )
        return JSONResponse(
            content=jsonable_encoder(error_response, exclude_none=True),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def exceeded_quota_error(request: Request, exception: QuotaExceededException):
        # TODO: CRIAR O MÉTODO ESPECIFICO PARA OS LOGS DE ERRO DO QUOTA-MIDDLEWARE
        # LogErrorHandle.handler(
        #     request=request, message="Exceeded Quota", exception=exception
        # )

        error_response = ErrorResponse(
            errorDetails=[
                ErrorDetails(
                    statusCode="ERR_MID_002",
                    message=f"Exceeded quota, balance is {exception.balance}",
                )
            ]
        )
        return JSONResponse(
            content=jsonable_encoder(error_response, exclude_none=True),
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    @staticmethod
    def not_found_error(request: Request, exception: NotFoundException):
        # TODO: CRIAR O MÉTODO ESPECIFICO PARA OS LOGS DE ERRO DO QUOTA-MIDDLEWARE
        # LogErrorHandle.handler(
        #     request=request, message="Exceeded Quota", exception=exception
        # )

        error_response = ErrorResponse(
            errorDetails=[
                ErrorDetails(
                    statusCode="ERR_MID_003",
                    message=f"{exception.get_entity()} not Found",
                )
            ]
        )
        return JSONResponse(
            content=jsonable_encoder(error_response, exclude_none=True),
            status_code=status.HTTP_404_NOT_FOUND,
        )
