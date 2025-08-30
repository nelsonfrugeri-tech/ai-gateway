from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.adapter.http.v1.payload.response.batch_response import (
    BatchStatusResponse,
)
from src.api.adapter.service.provider.port.batch_port import BatchPort
from src.api.adapter.service.provider.service_provider import ServiceProvider
from src.api.core.cost.cost_client import CostClient, CostType


class BatchBusiness:

    def __init__(self):
        self.service_provider = ServiceProvider()
        self.cost_client = CostClient()

    def generate_batch(self, batch_request: BatchRequest) -> BatchPort:
        return self.service_provider.generate_batch(
            provider_name=batch_request.provider.name,
            batch_request=batch_request,
        )

    def get_batch(self, provider_name, model_name, batch_id: str):
        batch_response = self.service_provider.get_batch(
            provider_name, model_name, batch_id
        )
        if batch_response.status == BatchStatusResponse.completed:
            batch_response.cost = self.cost_client.add(
                model_name=model_name,
                usage=batch_response.usage,
                cost_type=CostType.TEXT,
            )
        return batch_response
