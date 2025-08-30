from pydantic import BaseModel, field_validator, ConfigDict
from src.api.core.exception.bad_request_exception import BadRequestException
from src.api.adapter.cache.simple.provider_cache import ProviderCache


class Model(BaseModel):
    name: str

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={"examples": [{"name": "gpt-4o"}]},
    )


class Provider(BaseModel):
    name: str
    model: Model

    @field_validator("name")
    def validate_provider_name(cls, value):
        valid_names = ProviderCache.get_valid_provider_names()
        if value not in valid_names:
            raise BadRequestException(
                params=[
                    f"Provider name '{value}' is not valid. Valid names are {valid_names}"
                ]
            )
        return value

    @field_validator("model")
    def validate_model_name(cls, value):
        model = ProviderCache.get_provider_model(value.name)
        if model is None:
            raise BadRequestException(
                params=[f"Model name '{value.name}' is not valid."]
            )
        return value
