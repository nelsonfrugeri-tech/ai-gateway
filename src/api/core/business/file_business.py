import os


from src.api.adapter.http.v1.payload.request.file_request import FileRequest
from src.api.adapter.service.provider.port.file_port import FilePort
from src.api.adapter.service.provider.service_provider import ServiceProvider
from src.api.core.files.jsonl_files import JsonlFiles
from src.api.domain.file import File, FileExtension, FilePurpose
from src.api.domain.provider import (
    Provider,
    Model,
    Category,
)
from src.api.adapter.cache.simple.provider_cache import ProviderCache


from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)


class FileBusiness:

    def __init__(self):
        self.service_provider = ServiceProvider()
        self.extension = {
            "jsonl": JsonlFiles(),
        }

    def generate_file(self, file_request: FileRequest) -> FilePort:
        provider = next(
            provider
            for provider in ProviderCache.get_providers()
            if provider.name == file_request.provider.name
        )
        provider_model = next(
            model
            for model in provider.models
            if model.name == file_request.provider.model.name
        )
        file_path = self.extension[file_request.extension.name.value].create(
            file_request
        )
        new_file = self.service_provider.generate_file(
            provider_name=file_request.provider.name,
            file_object=File(
                file_path=file_path,
                purpose=FilePurpose(name=file_request.purpose.name.value),
                extension=FileExtension(name=file_request.extension.name.value),
                provider=Provider(
                    id=provider.id,
                    name=provider.name,
                    label=provider.label,
                    description=provider.description,
                    models=[
                        Model(
                            id=provider_model.id,
                            name=provider_model.name,
                            label=provider_model.label,
                            description=provider_model.description,
                            endpoints=provider_model.endpoints,
                            category=Category(
                                generation_type=provider_model.category.generation_type,
                                modal_type=provider_model.category.modal_type,
                            ),
                            enabled=provider_model.enabled,
                        )
                    ],
                ),
            ),
        )
        self.__delete(file_path)
        return new_file

    def get_file(self, provider_name, model_name, file_id: str):
        return self.service_provider.get_file(provider_name, model_name, file_id)

    def __delete(self, temp_file_path: str):
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            return
        raise BadRequestException(params=["Please provide a valid path!"])
