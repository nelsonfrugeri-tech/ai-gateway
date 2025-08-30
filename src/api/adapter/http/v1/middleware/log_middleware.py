import os
import json
import socket
import platform
import datetime
import time
from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.concurrency import iterate_in_threadpool

from typing import Callable, Tuple

from src.api.adapter.http.v1.log.http_log import (
    HTTPLog,
    Application,
    Environment,
    Request as RequestLogging,
    Response as ResponseLogging,
)

from src.api.core.log.config.log_config import LogConfig


class LogMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

        self._logconfig = LogConfig()
        self._log_level_info = "INFO"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if (
            request.url.path == f'{os.getenv("AIGATEWAY_API_PATH")}/health'
            or request.url.path.startswith(f'{os.getenv("AIGATEWAY_API_PATH")}/swagger')
        ):
            return await call_next(request)

        start_time = time.time()

        http_log = await self._set_request(request)

        if request.url.path == f'{os.getenv("AIGATEWAY_API_PATH")}/v1/chat/stream':
            return await self._handle_streaming_response(
                http_log, start_time, call_next, request
            )
        else:
            http_log, response = await self._set_response(
                http_log=http_log,
                start_time=start_time,
                request=request,
                call_next=call_next,
            )

            self._logconfig.get_logger().info(
                f"HTTP LOG: {http_log.request.method} {http_log.request.url} {http_log.response.status_code} {http_log.response.latency}ms",
                access_log=http_log.model_dump(exclude_none=True),
            )

            return response

    async def _set_request(self, request: Request) -> HTTPLog:
        body = {}
        request_headers = dict(request.headers)
        request_headers.pop('x-admin-auth', None)

        log_level = os.getenv("LOG_LEVEL", self._log_level_info)

        try:
            body = await request.json() if request.method in ["POST", "PUT"] else {}
        except json.JSONDecodeError:
            body = {}

        if log_level.upper() != "DEBUG":
            if "prompt" in body and "messages" in body["prompt"]:
                for message in body["prompt"]["messages"]:
                    message["content"] = "***"

        http_log = HTTPLog(
            correlation_id=request.headers.get("X-Correlation-ID", str(uuid4())),
            timestamp=datetime.datetime.now(),
            level=log_level,
            message="Request Successfully",
            application=Application(name="AIGateway", version="1.0.0"),
            environment=Environment(
                hostname=socket.gethostname(),
                ip=socket.gethostbyname(socket.gethostname()),
                runtime=f"{platform.python_implementation()} {platform.python_version()}",
                platform=platform.system(),
            ),
            request=RequestLogging(
                method=request.method,
                url=str(request.url),
                headers=request_headers,
                body=body,
            ),
        )
        request.state.http_log = http_log
        return http_log

    async def _set_response(
        self,
        http_log: HTTPLog,
        start_time: float,
        request: Request,
        call_next: Callable,
    ) -> Tuple[HTTPLog, Response]:
        data = {}
        response: Response = await call_next(request)

        body = b""
        async for body_iterator in response.body_iterator:
            body += body_iterator

        response.body_iterator = iterate_in_threadpool(iter([body]))

        try:
            data = json.loads(body.decode())
        except json.JSONDecodeError:
            data = {}

        if os.getenv("LOG_LEVEL", self._log_level_info).upper() != "DEBUG":
            if data.get("messages", None) is not None:
                for message in data["messages"]:
                    message["content"] = "***"

        end_time = time.time()
        http_log.response = ResponseLogging(
            status_code=response.status_code,
            body=data,
            latency=round((end_time - start_time) * 1000, 2),
        )

        return http_log, response

    async def _handle_streaming_response(
        self,
        http_log: HTTPLog,
        start_time: float,
        call_next: Callable,
        request: Request,
    ) -> StreamingResponse:
        response: Response = await call_next(request)

        original_body_iterator = response.body_iterator

        async def log_and_stream():
            nonlocal http_log
            nonlocal start_time
            try:
                async for chunk in original_body_iterator:
                    yield chunk
            finally:
                end_time = time.time()
                http_log.response = ResponseLogging(
                    status_code=response.status_code,
                    body={},
                    latency=round((end_time - start_time) * 1000, 2),
                )
                self._logconfig.get_logger().info(
                    f"HTTP LOG: {http_log.request.method} {http_log.request.url} {http_log.response.status_code} {http_log.response.latency}ms",
                    access_log=http_log.model_dump(exclude_none=True),
                )

        return StreamingResponse(log_and_stream(), media_type=response.media_type)
