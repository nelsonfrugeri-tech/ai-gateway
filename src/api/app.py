import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.api.adapter.database.mongodb.client.mongodb import MongoDB
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.core.exception.unauthorized_exception import UnauthorizedException
from src.api.adapter.http.v1.handle.route_handle import router
from src.api.adapter.http.v1.handle.exception_handle import (
    bad_request_exception,
    request_validation_exception,
    internal_server_error_exception,
    rate_limit_exception,
    not_found_exception,
    unauthorized_exception,
)
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
    ValidationBadRequestException,
)
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.core.exception.rate_limit_exeception import (
    RateLimitException,
)
from src.api.adapter.http.v1.middleware.log_middleware import LogMiddleware
from src.api.adapter.http.v1.middleware.header_middleware import HeaderMiddleware
from src.api.adapter.http.v1.middleware.quota_middleware import QuotaMiddleware

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = MongoDB.initialize_mongo()
    app.state.db = MongoDB.get_database(app.state.mongo_client)
    yield
    app.state.mongo_client.close()


def api():
    app = FastAPI(
        title=os.getenv("AIGATEWAY_API_TITLE", "AIGATEWAY"),
        description=os.getenv(
            "AIGATEWAY_API_DESCRIPTION",
            "Responsible for being the application integration with GenAI models",
        ),
        lifespan=lifespan,
    )
    app.include_router(router())
    app.add_exception_handler(RequestValidationError, request_validation_exception)
    app.add_exception_handler(BadRequestException, bad_request_exception)
    app.add_exception_handler(
        InternalServerErrorException, internal_server_error_exception
    )
    app.add_exception_handler(RateLimitException, rate_limit_exception)
    app.add_exception_handler(NotFoundException, not_found_exception)
    app.add_exception_handler(UnauthorizedException, unauthorized_exception)

    if os.getenv("TOGGLE_QUOTA_MIDDLEWARE", "false").lower() == "true":
        app.add_middleware(QuotaMiddleware)

    app.add_middleware(HeaderMiddleware)
    app.add_middleware(LogMiddleware)
    app.add_middleware(ValidationBadRequestException)

    return app


if __name__ == "__main__":
    uvicorn.run(
        api,
        factory=True,
        host=os.getenv("AIGATEWAY_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("AIGATEWAY_SERVER_PORT", "8080")),
    )
