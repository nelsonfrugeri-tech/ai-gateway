import ddtrace
import structlog
from ddtrace import tracer
from typing import Any, Dict, Optional


class LogConfig:

    def get_logger(self) -> structlog.BoundLogger:
        structlog.configure(
            processors=[
                self._tracer_injection,
                structlog.processors.JSONRenderer(),
            ]
        )

        return structlog.get_logger()

    def trace_datadog(
        self, data_dog_traces: Dict[str, str], operation_name: Optional[str] = None
    ):
        with tracer.trace(operation_name) as span:
            for key, value in data_dog_traces.items():
                span.set_tag(key, value)

    def _tracer_injection(
        self, logger: Any, log_method: str, event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:

        span = tracer.current_span()
        trace_id, span_id = (
            (str((1 << 64) - 1 & span.trace_id), span.span_id) if span else (None, None)
        )

        event_dict["dd.trace_id"] = str(trace_id or 0)
        event_dict["dd.span_id"] = str(span_id or 0)

        event_dict["dd.env"] = ddtrace.config.env or ""
        event_dict["dd.service"] = ddtrace.config.service or ""
        event_dict["dd.version"] = ddtrace.config.version or ""

        return event_dict
