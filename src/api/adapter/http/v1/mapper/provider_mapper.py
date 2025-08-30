from typing import List, Optional

from src.api.adapter.http.v1.payload.response.provider_response import (
    ProviderResponse,
    Model,
    Pixel,
    Price,
    Token,
    CategoryResponse,
)

from src.api.domain.provider import Provider as ProviderDomain, Category


class ProviderMapper:

    def to_providers(self, providers: List[ProviderDomain]) -> List[ProviderResponse]:
        return [
            ProviderResponse(
                name=provider.name,
                label=provider.label,
                description=provider.description,
                models=[
                    Model(
                        name=model.name,
                        label=model.label,
                        description=model.description,
                        context_window=model.context_window,
                        training_data=model.training_data,
                        prices=self.get_price(model.prices),
                        endpoints=model.endpoints,
                        enabled=model.enabled,
                        category=self.get_category(model.category),
                        process_type=model.process_type,
                    )
                    for model in provider.models
                ],
            )
            for provider in providers
        ]

    def get_category(self, category: Category):
        return CategoryResponse(
            generation_type=category.generation_type, modal_type=category.modal_type
        )

    def get_token(self, token: Optional[Token]) -> Optional[Token]:
        if token:
            return Token(
                input_value=token.input_value,
                output_value=token.output_value,
                training_value=token.tranning_value,
            )
        return None

    def get_pixel(self, pixel: Optional[Pixel]) -> Optional[Pixel]:
        if pixel:
            return Pixel(
                width=pixel.width,
                height=pixel.height,
                quality=pixel.quality.value if pixel.quality else None,
                value=pixel.value,
            )
        return None

    def get_price(self, prices: List[Price]) -> Optional[List[Price]]:
        if prices:
            return [
                Price(
                    token=self.get_token(price.token),
                    pixel=self.get_pixel(price.pixel),
                    unit_of_measure=(
                        price.unit_of_measure.value if price.unit_of_measure else None
                    ),
                    currency=price.currency.value if price.currency else None,
                )
                for price in prices
            ]
        return None
