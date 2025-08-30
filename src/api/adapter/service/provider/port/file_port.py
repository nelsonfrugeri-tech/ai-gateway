from abc import ABC, abstractmethod
from src.api.domain.file import File
from src.api.adapter.http.v1.payload.response.file_response import FileResponse


class FilePort(ABC):
    @abstractmethod
    def generate(self, file: File) -> FileResponse:
        pass

    @abstractmethod
    def get(self, model_name: str, file_id: str) -> FileResponse:
        pass
