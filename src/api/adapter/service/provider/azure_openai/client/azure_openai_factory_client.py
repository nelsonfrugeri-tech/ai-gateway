import os
import httpx
from openai import AzureOpenAI
from src.api.adapter.service.provider.azure_openai.constant.api_version import (
    APIVersion,
)
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)


class AzureOpenAIFactoryClient:

    def __init__(self) -> None:
        self._api_key_west_us = os.getenv("AZURE_OPENAI_WEST_US_API_KEY")
        self._endpoint_west_us = os.getenv("AZURE_OPENAI_WEST_US_ENDPOINT")
        self._api_key_east_us = os.getenv("AZURE_OPENAI_EAST_US_API_KEY")
        self._endpoint_east_us = os.getenv("AZURE_OPENAI_EAST_US_ENDPOINT")
        self._http_client = httpx.Client(
            verify=os.getenv("HTTPX_CLIENT_VERIFY", "False") == "True"
        )

        self._clients = {
            "gpt-4o": self._get_gpt_4o_pg_client(),
            "text-embedding-ada-002": self._get_text_embedding_ada_002_client(),
            "gpt-4o-batch": self._get_gpt_4o_batch_client(),
            "gpt-4o-mini-batch": self._get_gpt_4o_batch_client(),
            "gpt-4o-mini": self._get_gpt_4o_mini_client(),
            "dall-e-2": self.get_dall_e_2_client(),
            "dall-e-3": self.get_dall_e_3_client(),
        }

    def get_client(self, model_name: str):
        try:
            return self._clients[model_name]
        except KeyError as exception:
            raise InternalServerErrorException(
                message="Invalid model type",
                exception=exception,
            )
        except Exception as exception:
            raise InternalServerErrorException(
                exception=exception,
            )

    def _get_gpt_4o_pg_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_west_us,
            azure_endpoint=self._endpoint_west_us,
            api_version=APIVersion.VERSION_2024_10_21.value,
            azure_deployment="gpt-4o-pg",
            http_client=httpx.Client(
                verify=os.getenv("HTTPX_CLIENT_VERIFY", "False") == "True"
            ),
        )

    def _get_text_embedding_ada_002_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_west_us,
            azure_endpoint=self._endpoint_west_us,
            api_version=APIVersion.VERSION_2023_03_15_PREVIEW.value,
            azure_deployment="text-embedding-ada-002",
            http_client=self._http_client,
        )

    def _get_gpt_4o_batch_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_west_us,
            azure_endpoint=self._endpoint_west_us,
            api_version=APIVersion.VERSION_2024_07_01_PREVIEW.value,
            http_client=self._http_client,
        )

    def _get_gpt_4o_mini_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_east_us,
            azure_endpoint=self._endpoint_east_us,
            api_version="2024-10-01-preview",
            azure_deployment="gpt-4o-mini",
            http_client=self._http_client,
        )

    def get_dall_e_2_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_east_us,
            azure_endpoint=self._endpoint_east_us,
            api_version=APIVersion.VERSION_2024_05_01_PREVIEW.value,
            azure_deployment="dalle2",
            http_client=self._http_client,
        )

    def get_dall_e_3_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self._api_key_east_us,
            azure_endpoint=self._endpoint_east_us,
            api_version=APIVersion.VERSION_2024_02_01.value,
            azure_deployment="dalle3",
            http_client=self._http_client,
        )
