import os
import time
from typing import Optional
from datetime import datetime
from openai import AzureOpenAI
from src.api.core.log.config.log_config import LogConfig
from src.api.adapter.http.v1.middleware.header_middleware import (
    get_correlation_id,
)
from src.api.core.log.domain.llm_log import (
    LLMLog,
    LatencyLogging,
    ResponseLogging,
    CallLogging,
    ExceptionDetailLogging,
    AzureOpenAIClientLogging,
    ProviderLogging,
)


class AzureOpenAILogger:
    def __init__(self):
        self._logconfig = LogConfig()
        self._log_level = os.getenv("LOG_LEVEL", "DEBUG")

    def log(
        self,
        model_name: str,
        azure_openai: AzureOpenAI,
        status_code: int,
        start_time: time,
        exception: Optional[Exception] = None,
    ) -> None:
        llm_log = LLMLog(
            level=self._log_level,
            correlation_id=get_correlation_id(),
            timestamp=datetime.now(),
            provider=ProviderLogging(
                name="azure_openai",
                model=model_name,
                client=AzureOpenAIClientLogging(
                    base_url=str(azure_openai._base_url),
                    api_version=str(azure_openai._api_version),
                ),
                call=CallLogging(
                    response=ResponseLogging(
                        status_code=status_code,
                        latency=LatencyLogging(
                            time=round((time.time() - start_time) * 1000, 2)
                        ),
                        exception=(
                            ExceptionDetailLogging(
                                type=exception.__class__.__name__,
                                message=str(exception),
                            )
                            if exception
                            else None
                        ),
                    )
                ),
            ),
        )

        self._logconfig.get_logger().info(
            "LLM LOG: Azure OpenAI",
            llm_log=llm_log.model_dump(exclude_none=True),
        )
