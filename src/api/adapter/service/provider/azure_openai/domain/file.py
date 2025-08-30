from enum import Enum
from pydantic import BaseModel, ConfigDict


class FilePurpose(Enum):
    BATCH = "batch"


class File(BaseModel):
    file: str
    purpose: FilePurpose
    model: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
