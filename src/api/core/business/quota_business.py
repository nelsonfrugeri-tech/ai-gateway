from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.adapter.database.mongodb.client.mongodb_client import MongoDBClient
from src.api.adapter.http.v1.mapper.quota_mapper import QuotaMapper
from src.api.adapter.http.v1.payload.request.quota_request import (
    QuotaRequest,
    QuotaUpdateRequest,
)
from src.api.adapter.http.v1.payload.response.quota_response import (
    QuotaResponse,
)
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.domain.quota import Quota, QuotaUpdate


class QuotaBusiness:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.mongo_client = MongoDBClient(database, "quotas")

    async def create(self, quota_request: QuotaRequest) -> QuotaResponse:
        quota = QuotaMapper.to_quota(quota_request=quota_request)
        await self.__disable(quota=quota)
        await self.mongo_client.insert_one(document=quota.to_dict())

        return QuotaMapper.to_quota_response(quota=quota)

    async def retrieve(
        self, use_case_id: str, provider_name: str, model_name: str, enabled: str = None
    ) -> list[QuotaResponse]:
        quotas_data = await self.mongo_client.find(
            filter={
                "use_case.id": use_case_id,
                "enabled": enabled,
                "provider.name": provider_name,
                "provider.model.name": model_name,
            }
        )

        if len(quotas_data) < 1:
            raise NotFoundException("quotas")

        return [
            QuotaMapper.to_quota_response(
                quota=QuotaMapper.to_quota_from_dict(data=quota_data)
            )
            for quota_data in quotas_data
        ]

    async def update_many(
        self,
        use_case_id: str,
        provider_name: str,
        model_name: str,
        update: dict,
    ) -> None:
        filter = {
            "use_case.id": use_case_id,
            "provider.name": provider_name,
            "provider.model.name": model_name,
            "enabled": True,
        }

        await self.mongo_client.update_many(filter=filter, update={"$set": update})

    async def update(
        self,
        use_case_id: str,
        provider_name: str,
        model_name: str,
        quota_request: QuotaUpdateRequest,
        enabled: bool,
    ) -> QuotaResponse:
        enabled = enabled if enabled is not None else True
        quota = QuotaMapper.to_quota_update(quota_request=quota_request)

        filter = {
            "use_case.id": use_case_id,
            "provider.name": provider_name,
            "provider.model.name": model_name,
            "enabled": enabled,
        }
        update = {"$set": {"enabled": quota.enabled}}

        result = await self.mongo_client.find_one_and_update(filter=filter, update=update)

        if result is None:
            raise NotFoundException("quota")

        return QuotaMapper.to_quota_response_from_dict(result)

    async def __disable(self, quota: Quota) -> None:
        filter = {
            "_id": {"$ne": quota.id},
            "use_case.id": quota.use_case.id,
            "provider.name": quota.provider.name,
            "provider.model.name": quota.provider.model.name,
        }
        update = {"$set": {"enabled": False}}

        await self.mongo_client.update_many(filter=filter, update=update)
