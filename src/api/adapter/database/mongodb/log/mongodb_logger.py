import os
import time
import traceback
from typing import Optional, List
from datetime import datetime

from pymongo.results import UpdateResult, InsertManyResult, InsertOneResult

from src.api.core.log.config.log_config import LogConfig
from src.api.adapter.http.v1.middleware.header_middleware import get_correlation_id

from src.api.core.log.domain.database_log import (
    LatencyLogging,
    ExceptionLogging,
    ResponseLogging,
    UseCaseLogging,
    ModelLogging,
    ProviderLogging,
    QueryLogging,
    DocumentLogging,
    DocumentResponseLogging,
    DatabaseLog,
    VendorLogging,
    OperationLogging,
    UpdateLogging,
    OperatorUpdateValueLogging,
    UpdateResponseLogging,
)


class MongoDbLogger:
    def __init__(self):
        self._logconfig = LogConfig()
        self._log_level = os.getenv("LOG_LEVEL", "DEBUG")

    def log(
        self,
        operation_name: str,
        start_time: time,
        operation_documents: list = None,
        response_documents: List[InsertOneResult | InsertManyResult] = None,
        query: dict = None,
        update: dict = None,
        response_update: UpdateResult = None,
        exception: Optional[Exception] = None,
    ) -> None:
        mongodb_log = DatabaseLog(
            level=self._log_level,
            correlation_id=get_correlation_id(),
            timestamp=datetime.now(),
            vendor=VendorLogging(
                name="MongoDB",
                version="6.0.19",
            ),
            operation=OperationLogging(
                name=operation_name,
                documents=(
                    [DocumentLogging(**document) for document in operation_documents]
                    if operation_documents
                    else None
                ),
                query=(
                    QueryLogging(
                        provider=ProviderLogging(
                            name=query.get("provider.name", None),
                            model=ModelLogging(
                                name=query.get("provider.model.name", None),
                            ),
                        ),
                        use_case=UseCaseLogging(
                            id=query.get("use_case.id", None),
                            name=query.get("use_case.name", None),
                        ),
                        enabled=query.get("enabled", None),
                    )
                    if query
                    else None
                ),
                updates=(
                    [
                        UpdateLogging(
                            operator=operator,
                            update_values=[
                                OperatorUpdateValueLogging(key=key, value=value)
                                for key, value in operator_values.items()
                            ],
                        )
                        for operator, operator_values in update.items()
                    ]
                    if update
                    else None
                ),
                response=ResponseLogging(
                    documents=(
                        [
                            DocumentResponseLogging(
                                id=document.inserted_id,
                            )
                            for document in response_documents
                        ]
                        if response_documents
                        else None
                    ),
                    update=(
                        UpdateResponseLogging(
                            matched_count=response_update.matched_count,
                        )
                        if response_update
                        else None
                    ),
                    latency=LatencyLogging(
                        time=(time.time() - start_time) * 1000,
                    ),
                ),
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
            "DATABASE LOG: MongoDB",
            database_log=mongodb_log.model_dump(exclude_none=True),
        )
