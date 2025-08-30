import base64
import json
import os
import tempfile
import re


from binascii import Error as BinasciiError

from src.api.adapter.http.v1.payload.request.file_request import FileRequest
from src.api.adapter.http.v1.mapper.batch_file_mapper import BatchFileMapper
from src.api.core.files.interface_files import InterfaceFiles

from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)


class JsonlFiles(InterfaceFiles):

    def __init__(self) -> None:
        self.batch_file_mapper = BatchFileMapper()

    def create(self, file_request: FileRequest):
        content_file = self.__generate_content_file(file_request)
        temp_file_path = self.__generate_temp_file(
            name=file_request.name,
            content=content_file,
        )

        return temp_file_path

    def __generate_temp_file(self, name: str, content: str):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".jsonl", mode="w"
        ) as temp_file:
            for data in content:
                temp_file.write(json.dumps(data) + "\n")

        new_file_name = re.sub(
            r"(tmp)(\w+)(\.jsonl)$", rf"{name}_\1\2\3", temp_file.name
        )
        os.rename(temp_file.name, new_file_name)

        return new_file_name

    def __generate_content_file(self, file_request: FileRequest):
        formatted_data = self.__format_content(file_request.content)
        yield from self.batch_file_mapper.build_batch_file_content(
            file_request.provider.model.name,
            formatted_data["data"],
            file_request.endpoint.name,
        )

    def __format_content(self, content: str) -> dict:
        try:
            decoded_data = base64.b64decode(content).decode("utf-8").strip()
            return json.loads(decoded_data)
        except (ValueError, BinasciiError):
            raise BadRequestException(params=["Please provide a valid content"])
