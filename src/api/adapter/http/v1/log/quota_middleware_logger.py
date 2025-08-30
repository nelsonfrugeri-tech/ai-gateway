import os
import traceback
import time
from datetime import datetime
from typing import Optional
from src.api.core.log.config.log_config import LogConfig
from src.api.adapter.http.v1.middleware.header_middleware import get_correlation_id
from src.api.core.log.domain.quota_middleware_log import (
    QuotaMiddlewareLog,
    ExceptionLogging,
    UsageLogging,
    LatencyLogging,
    RequestLogging,
    ResponseLogging,
    QuotaLogging,
    ProviderLogging,
    ModelLogging,
)


class QuotaMiddlewareLogger:
    def __init__(self):
        self._logconfig = LogConfig()
        self._log_level = os.getenv("LOG_LEVEL", "DEBUG")

    def log(
        self,
        start_time: time,
        path: Optional[str] = None,
        method: Optional[str] = None,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
        current_balance: Optional[int] = None,
        limit: Optional[int] = None,
        status_code: Optional[int] = None,
        new_balance: Optional[int] = None,
        exception: Optional[Exception] = None,
    ) -> None:
        quota_middleware_log = QuotaMiddlewareLog(
            level=self._log_level,
            correlation_id=get_correlation_id(),
            timestamp=datetime.now(),
            request=(
                RequestLogging(path=path, method=method) if path and method else None
            ),
            response=(
                ResponseLogging(
                    status_code=status_code,
                    latency=LatencyLogging(
                        time=(time.time() - start_time) * 1000,
                    ),
                )
                if status_code
                else None
            ),
            quota=(
                QuotaLogging(
                    usage=UsageLogging(
                        prompt_tokens=0,
                        total_tokens=0,
                    ),
                    provider=ProviderLogging(
                        name=provider_name,
                        model=ModelLogging(name=model_name),
                    ),
                    limit=limit,
                    balance=current_balance,
                    new_balance=new_balance,
                )
                if provider_name
                and model_name
                and current_balance
                and limit
                and new_balance
                else None
            ),
            exception=(
                ExceptionLogging(
                    type=exception.__class__.__name__,
                    message=str(exception),
                    stack_trace="".join(
                        traceback.format_exception(
                            type(exception), exception, exception.__traceback__
                        )
                    ),
                )
                if exception
                else None
            ),
        )

        self._logconfig.get_logger().info(
            "QUOTA MIDDLEWARE LOG",
            quota_middleware_log=quota_middleware_log.model_dump(exclude_none=True),
        )
