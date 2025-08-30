import os
from collections import namedtuple
from datetime import datetime
from enum import Enum
from pydantic import field_serializer
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload

EnumFields = namedtuple("EnumFields", ["id", "name", "description"])


def serialize_enum(value: Enum):
    return {"id": value.id, "name": value.name, "description": value.description}


class ExtensionResponse(Enum):
    jsonl = EnumFields(1, "jsonl", "JSON Lines")


class PurposeResponse(Enum):
    batch = EnumFields(1, "batch", "Batch processing")


class StatusResponse(Enum):
    pending = EnumFields(1, "pending", "Pending")
    completed = EnumFields(2, "completed", "Completed")
    failed = EnumFields(3, "failed", "Failed")
    processed = EnumFields(4, "processed", "Processed")


class FileResponse(BasePayload):
    id: str
    name: str
    extension: ExtensionResponse
    purpose: PurposeResponse
    status: StatusResponse
    bytes: int
    created_at: int

    @field_serializer("extension")
    def serialize_extension(self, value: ExtensionResponse):
        return serialize_enum(value.value)

    @field_serializer("purpose")
    def serialize_purpose(self, value: PurposeResponse):
        return serialize_enum(value.value)

    @field_serializer("status")
    def serialize_status(self, value: StatusResponse):
        return serialize_enum(value.value)

    @field_serializer("created_at")
    def serialize_dt(self, value: int):
        return datetime.fromtimestamp(value).isoformat()

    @staticmethod
    def get_file_extension(filename: str) -> str:
        _, extension = os.path.splitext(filename)
        return extension[1:] if extension else ""
