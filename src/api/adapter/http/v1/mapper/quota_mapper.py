from src.api.adapter.http.v1.payload.request.quota_request import (
    QuotaRequest,
    QuotaUpdateRequest,
)
from src.api.adapter.http.v1.payload.response.quota_response import (
    QuotaResponse,
    ProviderResponse,
    UseCaseResponse,
    ModelResponse,
)
from src.api.domain.quota import (
    Quota,
    QuotaUnit,
    UseCase,
    Provider,
    Model,
    QuotaUpdate,
)


class QuotaMapper:
    @staticmethod
    def to_quota(quota_request: QuotaRequest) -> Quota:
        return Quota(
            unit=QuotaUnit[quota_request.unit.name],
            limit=quota_request.limit,
            use_case=UseCase(
                id=quota_request.use_case.id, name=quota_request.use_case.name
            ),
            provider=Provider(
                name=quota_request.provider.name,
                model=Model(name=quota_request.provider.model.name),
            ),
        )

    @staticmethod
    def to_quota_update(quota_request: QuotaUpdateRequest) -> QuotaUpdate:
        return QuotaUpdate(
            enabled=quota_request.enabled,
        )

    @staticmethod
    def to_quota_from_dict(data: dict) -> Quota:
        return Quota(
            _id=data.get("_id", None),
            unit=data.get("unit", "tokens"),
            limit=data.get("limit", None),
            balance=data.get("balance", None),
            use_case=UseCase(
                id=data["use_case"].get("id", None),
                name=data["use_case"].get("name", None),
            ),
            provider=Provider(
                name=data["provider"].get("name", None),
                model=Model(name=data["provider"].get("model").get("name", None)),
            ),
            created_at=data.get("created_at", None),
            enabled=data.get("enabled", False),
        )

    @staticmethod
    def to_quota_response(quota: Quota) -> QuotaResponse:
        return QuotaResponse(
            id=quota._id if hasattr(quota, '_id') else quota.id,
            unit=quota.unit,
            limit=quota.limit,
            balance=quota.balance,
            use_case=UseCaseResponse(
                id=quota.use_case.id,
                name=quota.use_case.name,
            ),
            provider=ProviderResponse(
                name=quota.provider.name,
                model=ModelResponse(name=quota.provider.model.name),
            ),
            created_at=quota.created_at,
            enabled=quota.enabled,
        )


    @staticmethod
    def to_quota_response_from_dict(data: dict) -> QuotaResponse:
        return QuotaResponse(
            id=data["_id"],
            unit=data["unit"],
            limit=data["limit"],
            balance=data["balance"],
            use_case=UseCaseResponse(
                id=data["use_case"]["id"],
                name=data["use_case"]["name"]
            ),
            provider=ProviderResponse(
                name=data["provider"]["name"],
                model=ModelResponse(
                    name=data["provider"]["model"]["name"]
                )
            ),
            created_at=data["created_at"],
            enabled=data["enabled"]
        )