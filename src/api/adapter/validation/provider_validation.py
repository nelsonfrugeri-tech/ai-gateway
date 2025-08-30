from fastapi import Query
from src.api.adapter.cache.simple.provider_cache import ProviderCache
from src.api.core.exception.bad_request_exception import BadRequestException
from src.api.core.exception.not_found_exception import NotFoundException


class ProviderValidation:

    @staticmethod
    def validate_provider_existence(
        provider_name: str = Query(..., alias="providerName")
    ):
        if not provider_name or provider_name.strip() == "":
            raise BadRequestException(
                params=["Provider name cannot be empty or blank."]
            )

        providers = ProviderCache.get_providers()
        if provider_name not in [provider.name for provider in providers]:
            raise NotFoundException(f"Provider {provider_name}")

        return provider_name
