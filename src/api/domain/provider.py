from collections import namedtuple
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from src.api.domain.price import Price


class EndpointName(str, Enum):
    CHAT: str = "/chat/completions"


class Endpoint(BaseModel):
    name: EndpointName = EndpointName.CHAT

    model_config = ConfigDict(use_enum_values=True)


GenerationTypeFields = namedtuple("GenerationTypeFields", ["id", "name", "description"])
ModalTypeFields = namedtuple("ModalTypeFields", ["id", "name", "description"])


class GenerationType(Enum):
    text = GenerationTypeFields(1, "text", "Text generation")
    image = GenerationTypeFields(2, "image", "Image generation")
    embedding = GenerationTypeFields(3, "embedding", "Embedding generation")


class ModalType(Enum):
    single = ModalTypeFields(1, "uni_modal", "Single modality")
    multi = ModalTypeFields(2, "multi_modal", "Multi modality")


class Category(BaseModel):
    generation_type: GenerationType
    modal_type: ModalType


class ProcessType(str, Enum):
    REALTIME = "real_time"
    BATCH = "batch"
    STREAM = "stream"


class Model(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    label: str
    description: str
    context_window: Optional[int] = None
    training_data: Optional[str] = None
    prices: Optional[List[Price]] = None
    max_input: int = 8191
    category: Category
    enabled: bool
    endpoints: Optional[List[Endpoint]] = None
    process_type: Optional[List[ProcessType]] = None


class Provider(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    label: str
    description: str
    models: List[Model]
