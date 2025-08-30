from src.api.adapter.service.provider.azure_openai.domain.image_generate import (
    ImageGenerate,
)

from src.api.adapter.service.provider.port.image_port import ImagePort
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse, Image
from src.api.adapter.http.v1.payload.response.guardrail_response import (
    GuardrailResponse,
)
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)


class AzureOpenAIImageDrive(ImagePort):

    def __init__(self, client: AzureOpenAIClient):
        self.client = client

    def generate(self, image_request: ImageRequest) -> ImageResponse:
        image_generate = ImageGenerate(
            prompt=image_request.prompt.message,
            model=image_request.provider.model.name,
            n=image_request.prompt.parameter.n,
            quality=image_request.prompt.parameter.quality,
            response_format=image_request.prompt.parameter.response_format,
            size=image_request.prompt.parameter.size,
            style=image_request.prompt.parameter.style,
        )

        response = self.client.image_generate(image_generate)

        images = []

        for item in response.data:
            image = Image(
                b64_json=item.b64_json,
                revised_prompt=item.revised_prompt,
                url=item.url,
                guardrail=GuardrailResponse.from_filter_results(
                    completion_filter_results=getattr(
                        item, "content_filter_results", None
                    ),
                    prompt_filter_results=getattr(item, "prompt_filter_results", None),
                ),
            )
            images.append(image)

        return ImageResponse(data=images)
