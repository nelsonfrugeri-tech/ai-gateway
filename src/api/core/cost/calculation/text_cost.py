from src.api.adapter.http.v1.payload.response.cost_response import (
    Price as PriceResponse,
    Token,
    Cost,
    Usage,
)
from src.api.core.cost.calculation.base_cost import BaseCost
from src.api.domain.price import Price


class TextCost(BaseCost):
    def calculate_cost(self, price: Price, usage: Usage) -> Cost:
        prompt_cost = self._calculate_cost(
            tokens=usage.prompt_tokens,
            unit_of_measure=price.unit_of_measure.value,
            value=price.token.input_value,
        )

        if usage.completion_tokens:
            completion_cost = self._calculate_cost(
                tokens=usage.completion_tokens,
                unit_of_measure=price.unit_of_measure.value,
                value=price.token.output_value,
            )
            total_cost = self._calculate_total_cost(completion_cost, prompt_cost)

            price_response = self.__build_price_response(price, True)

            return Cost(
                token=Token(
                    price=price_response,
                    prompt=prompt_cost,
                    completion=completion_cost,
                    total=total_cost,
                )
            )

        total_cost = self._calculate_total_cost(0.0, prompt_cost)

        price_response = self.__build_price_response(price, False)

        return Cost(
            token=Token(
                price=price_response,
                total=total_cost,
            )
        )

    def __build_price_response(
        self, price, has_completion_tokens: bool
    ) -> PriceResponse:
        if has_completion_tokens:
            return PriceResponse(
                unit_of_measure=price.unit_of_measure.value,
                currency=price.currency.value,
                input_value=price.token.input_value,
                output_value=price.token.output_value,
            )
        return PriceResponse(
            unit_of_measure=price.unit_of_measure.value,
            currency=price.currency.value,
            input_value=price.token.input_value,
        )
