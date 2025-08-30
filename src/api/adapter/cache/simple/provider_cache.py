from typing import List, Optional

from src.api.domain.provider import Provider, GenerationTypeFields
from src.api.core.business.provider_business import ProviderBusiness


class ProviderCache:
    _providers: List[Provider] = None

    @classmethod
    def get_valid_provider_names(cls) -> List[str]:
        providers: List[Provider] = cls.get_providers()
        return [provider.name for provider in providers]

    @classmethod
    def get_context_window_for_model(cls, model_name: str) -> Optional[int]:
        providers: List[Provider] = cls.get_providers()
        for provider in providers:
            for model in provider.models:
                if model.name == model_name:
                    return model.context_window
        return 0

    @classmethod
    def get_providers(cls) -> List[Provider]:
        if cls._providers is None:
            cls._providers = ProviderBusiness().find()
        return cls._providers

    @classmethod
    def get_provider_model(cls, model_name: str):
        providers: List[Provider] = cls.get_providers()
        for provider in providers:
            for model in provider.models:
                if model.name == model_name:
                    return model
        return None

    @classmethod
    def get_model_by_type(cls, model_type: GenerationTypeFields) -> List[str]:
        providers: List[Provider] = cls.get_providers()
        model_names: List[str] = [
            model.name
            for provider in providers
            for model in provider.models
            if model.category.generation_type.value.id == model_type.value.id
        ]
        return model_names
