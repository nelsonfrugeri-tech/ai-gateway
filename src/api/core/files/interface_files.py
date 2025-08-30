from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.file_request import FileRequest


class InterfaceFiles(ABC):
    @abstractmethod
    def create(self, file_request: FileRequest):
        pass
