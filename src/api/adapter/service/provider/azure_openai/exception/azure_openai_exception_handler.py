import openai
from typing import Optional
from openai import AzureOpenAI
from src.api.adapter.service.provider.azure_openai.log.azure_openai_logger import (
    AzureOpenAILogger,
)
from src.api.core.exception.rate_limit_exeception import (
    RateLimitException,
)
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)


class AzureOpenAIExceptionHandler:
    def __init__(self, logger: AzureOpenAILogger) -> None:
        self._logger = logger

    def throw(
        self,
        exception: Exception,
        model_name: str,
        azure_openai: AzureOpenAI,
        status_code: int,
        start_time: float,
        message: Optional[str] = None,
    ) -> None:
        exception_mapping = {
            openai.RateLimitError: RateLimitException(exception=exception),
            openai.NotFoundError: NotFoundException(entity=message),
            openai.InternalServerError: InternalServerErrorException(
                exception=exception
            ),
        }

        self._logger.log(
            model_name=model_name,
            azure_openai=azure_openai,
            status_code=status_code,
            start_time=start_time,
            exception=exception,
        )

        raise exception_mapping.get(
            type(exception),
            InternalServerErrorException(
                message="Azure OpenAI error not mapped!", exception=exception
            ),
        )
