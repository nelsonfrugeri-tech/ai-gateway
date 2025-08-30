from fastapi import Query
from src.api.adapter.cache.simple.provider_cache import ProviderCache
from src.api.core.exception.not_found_exception import NotFoundException
from src.api.domain.provider import ProcessType
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)
from src.api.domain.provider import GenerationTypeFields


class ModelValidation:

    @staticmethod
    def validate_model_by_typel(
        model_name: str, generation_type: GenerationTypeFields
    ) -> bool:
        models = ProviderCache.get_model_by_type(generation_type)
        if model_name not in models:
            raise BadRequestException(
                params=[
                    f"Model name '{model_name}' is not a valid {generation_type.name} generation model type"
                ]
            )
        return model_name

    @staticmethod
    def validate_model_enable(model_name: str) -> bool:
        model = ProviderCache.get_provider_model(model_name)
        if model.enabled is False:
            raise BadRequestException(
                params=[
                    f"Model name '{model_name}' is not enable. Please use another one"
                ]
            )
        return model_name

    @staticmethod
    def validate_max_tokens(max_tokens: int, context_window: int, model_name: str):
        if max_tokens is not None and max_tokens > context_window:
            raise BadRequestException(
                params=[
                    f"maxTokens '{max_tokens}' exceeds the context window '{context_window}' for the model '{model_name}'"
                ]
            )

    @staticmethod
    def validate_model_existence(model_name: str = Query(..., alias="modelName")):
        if not model_name or model_name.strip() == "":
            raise BadRequestException(params=["Model name cannot be empty or blank."])
        model = ProviderCache.get_provider_model(model_name)
        if model is None:
            raise NotFoundException(f"Model {model_name}")

        return model_name

    @staticmethod
    def validate_batch_purpose(purpose_name: str, model_name: str):
        if purpose_name == "batch":
            model = ProviderCache.get_provider_model(model_name)
            if not any(pt == ProcessType.BATCH for pt in model.process_type):
                raise BadRequestException(
                    params=[
                        f"The model_name '{model_name}'does not support batch processing."
                    ]
                )

        return purpose_name
