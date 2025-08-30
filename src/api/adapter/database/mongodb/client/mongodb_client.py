import inspect
import time
from typing import Any, Mapping

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import UpdateResult
from pymongo import ReturnDocument

from src.api.adapter.database.mongodb.log.mongodb_logger import MongoDbLogger
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.core.exception.not_found_exception import NotFoundException


class MongoDBClient:
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str) -> None:
        self.collection = database[collection_name]
        self._logger = MongoDbLogger()

    async def insert_one(self, document: dict) -> None:
        try:
            start_time = time.time()

            new_doc = await self.collection.insert_one(document)
            
            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                operation_documents=[document],
                response_documents=[new_doc],
            )

        except Exception as exception:
            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                operation_documents=[document],
                exception=exception,
            )
            raise InternalServerErrorException(
                exception=exception,
                message="Failed to insert document into the collection.",
            )

    async def find_one_and_update(self, filter: dict, update: dict) -> Mapping[str, Any] | None:
        try:
            start_time = time.time()
            updated_doc = await self.collection.find_one_and_update(
                filter, update, return_document=ReturnDocument.AFTER
            )


            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                update=update,
            )

            return updated_doc

        except Exception as exception:
            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                update=update,
                exception=exception,
            )
            raise InternalServerErrorException(
                exception=exception, message="Failed to update single document."
            )

    async def update_many(self, filter: dict, update: dict) -> None:
        try:
            start_time = time.time()

            updated_docs = await self.collection.update_many(filter, update)

            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                update=update,
                response_update=updated_docs,
            )

        except Exception as exception:
            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                update=update,
                exception=exception,
            )
            raise InternalServerErrorException(
                exception=exception, message="Failed to update multiple documents."
            )

    async def find(self, filter: dict = {}) -> list[dict]:
        try:
            start_time = time.time()
            docs = await self.collection.find(self.__filter_query(**filter)).to_list(
                length=None
            )

            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                operation_documents=docs,
            )
            return docs
        except Exception as error:
            self._logger.log(
                operation_name=inspect.currentframe().f_code.co_name,
                start_time=start_time,
                query=filter,
                exception=error,
            )
            raise InternalServerErrorException(
                exception=error, message="Failed to get documents."
            )

    def __filter_query(self, **kwargs) -> dict:
        query = {}
        for key, value in kwargs.items():
            if value is not None:
                query[key] = value
        return query
