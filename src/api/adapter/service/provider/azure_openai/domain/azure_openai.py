import httpx
from pydantic import BaseModel, ConfigDict


class AzureOpenAIConnection(BaseModel):
    azure_endpoint: str
    api_key: str
    api_version: str
    azure_deployment: str
    http_client: httpx.Client

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )
