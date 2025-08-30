import os
from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html


swagger_router = APIRouter()


@swagger_router.get("/swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    path = os.getenv("AIGATEWAY_API_PATH", "/ai-gateway")
    return get_swagger_ui_html(openapi_url=f"{path}/swagger.json", title="Swagger UI")


@swagger_router.get("/swagger.json", include_in_schema=False)
async def get_open_api_endpoint(request: Request):
    return request.app.openapi()
