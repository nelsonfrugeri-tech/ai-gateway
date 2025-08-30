from enum import Enum
from src.api.adapter.cache.simple.provider_cache import ProviderCache
from src.api.core.cost.calculation.text_cost import TextCost
from src.api.core.cost.calculation.image_cost import ImageCost
from src.api.adapter.http.v1.payload.response.cost_response import Usage, Cost


class CostType(Enum):
    IMAGE = "image"
    TEXT = "text"


class CostClient:
    def __init__(self):
        self.calculators = {
            CostType.TEXT: TextCost(),
            CostType.IMAGE: ImageCost(),
        }

    def add(
        self,
        model_name: str,
        usage: Usage,
        cost_type: CostType,
    ) -> Cost | None:
        model = ProviderCache.get_provider_model(model_name)
        if model.prices:
            for price in model.prices:
                if cost_type in self.calculators:
                    return self.calculators[cost_type].calculate_cost(price, usage)
        return None
