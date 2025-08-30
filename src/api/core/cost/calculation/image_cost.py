from src.api.core.cost.calculation.base_cost import BaseCost
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse
from src.api.domain.price import Price


class ImageCost(BaseCost):
    def calculate_cost(self, price: Price, response: ImageResponse) -> ImageResponse:
        # Implementar lógica de cálculo de custo para imagens
        pass
