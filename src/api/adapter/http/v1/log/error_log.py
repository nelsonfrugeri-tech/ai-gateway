from src.api.adapter.http.v1.log.http_log import ExceptionDetail, HTTPLog
from fastapi import Request
import traceback


class ErrorLog:

    # TODO: criar o método handler do middlware

    @staticmethod
    def handler(request: Request, message: str, exception: Exception = None) -> None:
        http_log: HTTPLog = request.state.http_log
        http_log.level = "ERROR"
        http_log.message = message

        if exception:
            exception_type = exception.__class__.__name__
            exception_message = str(exception)
            stack_trace = traceback.format_exc()

            http_log.exception = ExceptionDetail(
                type=exception_type, message=exception_message, stack_trace=stack_trace
            )
