from enum import Enum
from pydantic import BaseModel, ConfigDict

from src.api.domain.provider import Provider


class FileExtensionType(Enum):
    JSONL = "jsonl"


class FileExtension(BaseModel):
    name: FileExtensionType


class FilePurposeName(Enum):
    BATCH = "batch"


class FilePurpose(BaseModel):
    name: FilePurposeName


class File(BaseModel):
    file_path: str
    purpose: FilePurpose
    extension: FileExtension
    provider: Provider

    model_config = ConfigDict(arbitrary_types_allowed=True)
