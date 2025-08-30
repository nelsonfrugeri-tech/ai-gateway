import base64
import json
from typing import List, Dict
from src.api.adapter.service.provider.azure_openai.domain.batch import Batch
from src.api.adapter.service.provider.port.batch_port import BatchPort
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)


from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.adapter.http.v1.payload.response.batch_response import (
    BatchMessageResponse,
    BatchUsageResponse,
    BatchErrorResponse,
    BatchDataItemResponse,
    BatchResponse,
    BatchFileResponse,
    BatchRequestCountsResponse,
    BatchStatusResponse,
    BatchCompletionWindowResponse,
    BatchEndpointResponse,
    BatchResultResponse,
)

from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)


class AzureOpenAIBatchDrive(BatchPort):

    def __init__(self, client: "AzureOpenAIClient"):
        self.client = client

    def generate(self, batch_request: BatchRequest) -> BatchResponse:
        batch = Batch(
            input_file_id=batch_request.file.id,
            endpoint=batch_request.endpoint.name,
            model=batch_request.provider.model.name,
            completion_window=batch_request.completion_window.name.value,
        )
        return self.__build_batch_response(
            model_name=batch.model, response=self.client.batch(batch)
        )

    def get(self, model_name: str, batch_id: str) -> BatchResponse:
        return self.__build_batch_response(
            model_name=model_name,
            response=self.client.get_batch(model_name=model_name, batch_id=batch_id),
        )

    def __build_batch_result_response(self, file: str):
        try:
            responses = self.__parse_and_sort_responses(file=file)
            data_items = []

            data_items, total_usage_tokens = self.__build_data_items(
                file_items=responses
            )

            return BatchResultResponse(
                type="base64",
                content=base64.b64encode(
                    json.dumps(
                        {"data": [item.dict() for item in data_items]},
                        indent=4,
                        ensure_ascii=False,
                    ).encode("utf-8")
                ).decode("utf-8"),
            ), BatchUsageResponse(**total_usage_tokens)
        except Exception as error:
            raise InternalServerErrorException(
                exception=error, message="Error serializing the file result."
            )

    def __get_content(self, model_name: str, file_id: str) -> str:
        return self.client.get_file_content(model_name, file_id).text

    def __parse_and_sort_responses(self, file: str) -> List[Dict]:
        return sorted(
            [json.loads(obj) for obj in file.strip().split("\n") if obj.strip()],
            key=lambda x: int(x["custom_id"]),
        )

    def __build_data_items(self, file_items):
        data_items = []
        total_usage_tokens = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "total_tokens": 0,
        }

        for response in file_items:

            choices = response["response"]["body"].get("choices", [])
            request_error = None

            if response["error"] is not None:
                request_error = BatchErrorResponse(
                    code=response.error.code, message=response.error.message
                )

            if not choices:
                continue

            message_data = choices[0].get("message", {})
            usage_data = response["response"]["body"].get("usage", {})

            total_usage_tokens["completion_tokens"] += usage_data.get(
                "completion_tokens", 0
            )
            total_usage_tokens["prompt_tokens"] += usage_data.get("prompt_tokens", 0)
            total_usage_tokens["total_tokens"] += usage_data.get("total_tokens", 0)

            message = BatchMessageResponse(
                role=message_data["role"], content=message_data["content"]
            )
            usage = BatchUsageResponse(
                completion_tokens=usage_data["completion_tokens"],
                prompt_tokens=usage_data["prompt_tokens"],
                total_tokens=usage_data["total_tokens"],
            )

            data_items.append(
                BatchDataItemResponse(message=message, usage=usage, error=request_error)
            )
        return data_items, total_usage_tokens

    def __build_batch_errors(self, errors) -> List[BatchErrorResponse]:
        return [
            BatchErrorResponse(code=err.code, message=err.message, line=err.line)
            for err in errors.data
        ]

    def __build_batch_response(self, model_name: str, response) -> BatchResponse:

        result, usage_tokens = (
            self.__build_batch_result_response(
                self.__get_content(model_name, response.output_file_id)
            )
            if response.status == "completed"
            else (None, None)
        )

        batch_errors = (
            self.__build_batch_errors(response.errors)
            if response.errors is not None
            else None
        )

        return BatchResponse(
            id=response.id,
            file=BatchFileResponse(id=response.input_file_id),
            status=BatchStatusResponse[response.status],
            completion_window=BatchCompletionWindowResponse(
                name=response.completion_window
            ),
            errors=batch_errors,
            usage=usage_tokens,
            endpoint=BatchEndpointResponse.from_endpoint(response.endpoint),
            result=result,
            request_counts=BatchRequestCountsResponse(
                completed=response.request_counts.completed,
                failed=response.request_counts.failed,
                total=response.request_counts.total,
            ),
            created_at=response.created_at,
            in_progress_at=response.in_progress_at,
            completed_at=response.completed_at,
            failed_at=response.failed_at,
            expired_at=response.expired_at,
            cancelled_at=response.cancelled_at,
        )
