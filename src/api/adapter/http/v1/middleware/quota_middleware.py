import asyncio
import os
import json
import time
from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, List, Union
from src.api.domain.quota import Provider
from src.api.core.business.quota_business import QuotaBusiness
from src.api.adapter.http.v1.payload.response.quota_response import QuotaResponse
from src.api.adapter.http.v1.payload.response.cost_response import Usage
from src.api.adapter.http.v1.handle.middleware_error_handle import (
    MiddlewareErrorHandle,
)

# from src.api.core.exception.internal_server_error_exception import InternalServerErrorException
from src.api.core.exception.quota_exceeded_exception import QuotaExceededException
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.adapter.http.v1.log.quota_middleware_logger import QuotaMiddlewareLogger


class QuotaMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        prefix = os.getenv("AIGATEWAY_API_PATH", "/ai-gateway")
        self.ENDPOINT_ENABLED = {
            f"{prefix}/v1/chat": {"POST"},
            f"{prefix}/v1/embeddings": {"POST"},
            f"{prefix}/v1/similarity": {"POST"},
        }
        self._logger = QuotaMiddlewareLogger()
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            start_time = time.time()
            path = request.url.path
            method = request.method

            if path in self.ENDPOINT_ENABLED and method in self.ENDPOINT_ENABLED[path]:
                quota_business = QuotaBusiness(request.app.state.db)

                client_id = request.headers.get("client_id")
                provider = await self.__get_provider(request)
                balance, limit = await self.__validate_balance(
                    quota_business=quota_business,
                    provider=provider,
                    client_id=client_id,
                )
                response_stream = await call_next(request)
                response = await self.__get_response(response_stream=response_stream)

                if (
                    response.status_code != status.HTTP_200_OK
                    and response.status_code != status.HTTP_201_CREATED
                ):
                    return response

                usage = await self.__get_usage(response=response)

                new_balance = await self.__calculate_new_balance(
                    usage=usage,
                    balance=balance,
                )

                await self.__update_balance(
                    quota_business=quota_business,
                    provider=provider,
                    client_id=client_id,
                    new_balance=new_balance,
                )

                self._logger.log(
                    start_time=start_time,
                    path=path,
                    method=method,
                    provider_name=provider.name,
                    model_name=provider.model.name,
                    current_balance=balance,
                    limit=limit,
                    status_code=response.status_code,
                    new_balance=new_balance,
                )
                return response

            return await call_next(request)
        except QuotaExceededException as exception:
            self._logger.log(start_time=start_time, exception=exception)
            return MiddlewareErrorHandle.exceeded_quota_error(
                request=request,
                exception=exception,
            )
        except NotFoundException as exception:
            self._logger.log(start_time=start_time, exception=exception)
            return MiddlewareErrorHandle.not_found_error(
                request=request,
                exception=exception,
            )

    async def __update_balance(
        self,
        quota_business: QuotaBusiness,
        provider: Provider,
        client_id: str,
        new_balance: int,
    ) -> None:
        asyncio.create_task(
            quota_business.update_many(
                use_case_id=client_id,
                provider_name=provider.name,
                model_name=provider.model.name,
                update={"balance": new_balance},
            )
        )

    async def __calculate_new_balance(self, usage: Usage, balance: int) -> int:
        return balance - usage.total_tokens

    async def __get_usage(self, response: Response) -> Usage:
        return Usage(**json.loads(response.body.decode("utf-8"))["usage"])

    async def __get_response(self, response_stream: Response) -> Response:
        response_body_chunks = []

        async for chunk in response_stream.body_iterator:
            response_body_chunks.append(chunk)

        return Response(
            content=b"".join(response_body_chunks),
            status_code=response_stream.status_code,
            headers=response_stream.headers,
        )

    async def __validate_balance(
        self, quota_business: QuotaBusiness, provider: Provider, client_id: str
    ) -> Union[int, int]:
        start_time = time.time()
        quotas_response: List[QuotaResponse] = await quota_business.retrieve(
            use_case_id=client_id,
            provider_name=provider.name,
            model_name=provider.model.name,
            enabled=True,
        )

        if not quotas_response:
            not_found_exception = NotFoundException(entity="Quota")
            self._logger.log(start_time=start_time, exception=not_found_exception)
            raise not_found_exception

        balance = quotas_response[0].balance

        if balance < 1:
            quota_exceeded_exception = QuotaExceededException(balance=balance)
            self._logger.log(start_time=start_time, exception=quota_exceeded_exception)
            raise quota_exceeded_exception

        return balance, quotas_response[0].limit

    async def __get_provider(self, request: Request) -> Provider:
        body = await request.body()
        return Provider(**json.loads(body.decode("utf-8"))["provider"])
