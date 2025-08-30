import os
from fastapi import APIRouter
from dotenv import load_dotenv
from src.api.adapter.http.v1.endpoint.health_endpoint import health_router
from src.api.adapter.http.v1.endpoint.batch_endpoint import batch_router
from src.api.adapter.http.v1.endpoint.chat_endpoint import chat_router
from src.api.adapter.http.v1.endpoint.embedding_endpoint import embedding_router
from src.api.adapter.http.v1.endpoint.file_endpoint import file_router
from src.api.adapter.http.v1.endpoint.similarity_endpoint import similarity_router
from src.api.adapter.http.v1.endpoint.image_endpoint import image_router
from src.api.adapter.http.v1.endpoint.provider_endpoint import provider_router
from src.api.adapter.http.v1.endpoint.quota_endpoint import quota_router
from src.api.adapter.http.v1.endpoint.swagger_endpoint import swagger_router


def router():
    load_dotenv()

    api_router = APIRouter()
    path = os.getenv("AIGATEWAY_API_PATH")

    api_router.include_router(health_router, prefix=path, tags=["health-router"])

    api_router.include_router(
        batch_router,
        prefix=path,
        tags=["batch"],
    )

    api_router.include_router(
        chat_router,
        prefix=path,
        tags=["chat"],
    )

    api_router.include_router(
        embedding_router,
        prefix=path,
        tags=["embedding"],
    )

    api_router.include_router(
        file_router,
        prefix=path,
        tags=["files"],
    )

    api_router.include_router(
        similarity_router,
        prefix=path,
        tags=["similarity"],
    )

    api_router.include_router(
        image_router,
        prefix=path,
        tags=["images"],
    )

    api_router.include_router(
        provider_router,
        prefix=path,
        tags=["provider"],
    )

    api_router.include_router(
        quota_router,
        prefix=path,
        tags=["quotas"],
    )

    api_router.include_router(
        swagger_router,
        prefix=path,
        tags=["swagger"],
    )

    return api_router
