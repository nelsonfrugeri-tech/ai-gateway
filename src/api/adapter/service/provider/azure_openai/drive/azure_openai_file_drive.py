from src.api.adapter.service.provider.azure_openai.domain.file import File as AzureFile
from src.api.adapter.service.provider.port.file_port import FilePort
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)


from src.api.adapter.http.v1.payload.response.file_response import (
    FileResponse,
    ExtensionResponse as FileExtensionResponse,
    PurposeResponse as FilePurposeResponse,
    StatusResponse as FileStatusResponse,
)

from src.api.domain.file import File


class AzureOpenAIFileDrive(FilePort):

    def __init__(self, client: "AzureOpenAIClient"):
        self.client = client

    def generate(self, file_object: File) -> FileResponse:
        new_file = AzureFile(
            file=file_object.file_path,
            purpose=file_object.purpose.name.value,
            model=file_object.provider.models[0].name,
        )
        return self.__build_file_response(self.client.create_file(new_file))

    def get(self, model_name: str, file_id: str) -> FileResponse:
        return self.__build_file_response(
            response=self.client.get_file(model_name, file_id)
        )

    def __build_file_response(self, response) -> FileResponse:
        return FileResponse(
            id=response.id,
            name=response.filename,
            extension=FileExtensionResponse[
                FileResponse.get_file_extension(response.filename)
            ],
            purpose=FilePurposeResponse[response.purpose],
            status=FileStatusResponse[response.status],
            bytes=response.bytes,
            created_at=response.created_at,
        )
