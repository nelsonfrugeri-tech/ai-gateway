import os

from motor.motor_asyncio import AsyncIOMotorClient

from src.api.core.exception.startup_error_exception import StartupErrorException


class MongoDB:
    @staticmethod
    def initialize_mongo():
        mongodb_user = os.getenv("MONGODB_USER")
        mongodb_password = os.getenv("MONGODB_PASSWORD")
        mongodb_connection = os.getenv("MONGODB_CONNECTION")

        if not all([mongodb_user, mongodb_password, mongodb_connection]):
            raise StartupErrorException(
                "MongoDB environment variables are not configured correctly."
            )

        connection_uri = mongodb_connection.replace("{USER}", mongodb_user).replace(
            "{PASSWORD}", mongodb_password
        )
        return AsyncIOMotorClient(connection_uri)

    @staticmethod
    def get_database(motor_client: AsyncIOMotorClient):
        mongodb_database = os.getenv("MONGODB_DATABASE")

        if not mongodb_database:
            raise StartupErrorException(
                message="The environment variable 'MONGODB_DATABASE' is not set or is empty. Please check the MongoDB configuration."
            )

        return motor_client[mongodb_database]
