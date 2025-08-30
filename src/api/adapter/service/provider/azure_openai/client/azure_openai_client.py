import time
import openai
from fastapi import status
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv
from src.api.adapter.service.provider.azure_openai.domain.chat_completion import (
    ChatCompletion,
)
from src.api.adapter.service.provider.azure_openai.domain.batch import Batch
from src.api.adapter.service.provider.azure_openai.domain.embedding import Embedding
from src.api.adapter.service.provider.azure_openai.domain.file import File
from src.api.adapter.service.provider.azure_openai.domain.image_generate import (
    ImageGenerate,
)

from src.api.adapter.service.provider.azure_openai.client.azure_openai_factory_client import (
    AzureOpenAIFactoryClient,
)
from src.api.adapter.service.provider.azure_openai.log.azure_openai_logger import (
    AzureOpenAILogger,
)
from src.api.core.log.config.log_config import LogConfig
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.adapter.service.provider.azure_openai.exception.azure_openai_exception_handler import (
    AzureOpenAIExceptionHandler,
)


class AzureOpenAIClient:

    def __init__(self):
        load_dotenv()

        self.client = OpenAI()
        # self.client = AzureOpenAIFactoryClient()
        self._logger = AzureOpenAILogger()
        self._exception_handler = AzureOpenAIExceptionHandler(self._logger)
        self._logconfig = LogConfig()

    def trace_operation(
        self, model_name: str, elapsed_time_ms: float, operation_desc: str
    ):
        self._logconfig.trace_datadog(
            {"model": model_name, "latency-ms": str(int(elapsed_time_ms))},
            f"AzureOpenAIAdapter.{operation_desc}",
        )

    def image_generate(self, image_generate: ImageGenerate):
        try:
            start_time = time.time()
            # azure_openai: AzureOpenAI = self.client.get_client(image_generate.model)

            result = self.client.images.generate(
                **image_generate.model_dump(exclude_none=True)
            )

            self.trace_operation(
                image_generate.model,
                (time.time() - start_time) * 1000,
                "image_generate",
            )

            # self._logger.log(
            #     model_name=image_generate.model,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_201_CREATED,
            #     start_time=start_time,
            # )

            return result
        except (openai.RateLimitError, InternalServerErrorException) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=image_generate.model,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,                
            # )

    def chat_completion(self, chat_completion: ChatCompletion):
        try:
            start_time = time.time()
            # azure_openai: AzureOpenAI = self.client.get_client(chat_completion.model)

            result = self.client.chat.completions.create(
                **chat_completion.model_dump(exclude_none=True)
            )

            self.trace_operation(
                chat_completion.model,
                (time.time() - start_time) * 1000,
                "chat_completion",
            )

            # self._logger.log(
            #     model_name=chat_completion.model,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_200_OK,
            #     start_time=start_time,
            # )

            return result
        except (openai.RateLimitError, InternalServerErrorException) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=chat_completion.model,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,                
            # )

    def embedding(self, embedding: Embedding):
        try:
            start_time = time.time()
            # azure_openai: AzureOpenAI = self.client.get_client(embedding.model)

            result = self.client.embeddings.create(
                **embedding.model_dump(exclude_none=True)
            )

            self.trace_operation(
                embedding.model,
                (time.time() - start_time) * 1000,
                "create_embedding",
            )

            # self._logger.log(
            #     model_name=embedding.model,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_200_OK,
            #     start_time=start_time,
            # )

            return result
        except (openai.RateLimitError, InternalServerErrorException) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=embedding.model,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,                
            # )

    def create_file(self, new_file: File):
        try:
            start_time = time.time()
            # azure_openai: AzureOpenAI = self.client.get_client(new_file.model)

            result = self.client.files.create(
                file=open(new_file.file, "rb"), purpose=new_file.purpose.value
            )

            self.trace_operation(
                new_file.model,
                (time.time() - start_time) * 1000,
                "create_file",
            )

            # self._logger.log(
            #     model_name=new_file.model,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_201_CREATED,
            #     start_time=start_time,
            # )

            return result
        except (openai.RateLimitError, InternalServerErrorException) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=new_file.model,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,                
            # )

    def batch(self, batch: Batch):
        try:
            start_time = time.time()
            # azure_openai: AzureOpenAI = self.client.get_client(batch.model)

            result = self.client.batches.create(
                **batch.model_dump(exclude_none=True, exclude={"model"})
            )

            self.trace_operation(
                batch.model,
                (time.time() - start_time) * 1000,
                "create_batch",
            )

            # self._logger.log(
            #     model_name=batch.model,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_201_CREATED,
            #     start_time=start_time,
            # )

            return result
        except (
            openai.RateLimitError,
            openai.NotFoundError,
            InternalServerErrorException,
        ) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=batch.model,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,
            #     message=f"File: {batch.input_file_id}",
            # )

    def get_file(self, model_name: str, file_id: str):
        try:
            start_time = time.time()

            # azure_openai: AzureOpenAI = self.client.get_client(model_name)
            retrieved_file = self.client.files.retrieve(file_id=file_id)

            # self._logger.log(
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_200_OK,
            #     start_time=start_time,
            # )

            return retrieved_file
        except (
            openai.RateLimitError,
            openai.NotFoundError,
            InternalServerErrorException,
        ) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,
            #     message=f"File: {file_id}",
            # )

    def get_file_content(self, model_name: str, file_id: str):
        try:
            start_time = time.time()

            # azure_openai: AzureOpenAI = self.client.get_client(model_name)
            file_content = self.client.files.content(file_id)

            # self._logger.log(
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_200_OK,
            #     start_time=start_time,
            # )

            return file_content
        except (
            openai.RateLimitError,
            openai.NotFoundError,
            InternalServerErrorException,
        ) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,
            #     message=f"File: {file_id}",
            # )

    def get_batch(self, model_name: str, batch_id: str):
        try:
            start_time = time.time()

            # azure_openai: AzureOpenAI = self.client.get_client(model_name)
            batch = self.client.batches.retrieve(batch_id=batch_id)

            # self._logger.log(
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=status.HTTP_200_OK,
            #     start_time=start_time,
            # )

            return batch
        except (
            openai.RateLimitError,
            openai.NotFoundError,
            InternalServerErrorException,
        ) as exception:
            raise exception
            # self._exception_handler.throw(
            #     exception=exception,
            #     model_name=model_name,
            #     azure_openai=azure_openai,
            #     status_code=exception.status_code,
            #     start_time=start_time,
            #     message=f"Batch: {batch_id}",
            # )

