from src.api.domain.provider import (
    Provider,
    Endpoint,
    EndpointName,
    Model,
    Category,
    GenerationType,
    ModalType,
    ProcessType,
)

from src.api.domain.price import (
    Pixel,
    Price,
    UnitOfMeasure,
    Currency,
    Token,
    ImageQuality,
)


class ProviderBusiness:

    def find(self) -> list[Provider]:
        return [
            Provider(
                name="azure_openai",
                label="Azure OpenAI",
                description="Azure OpenAI provider",
                models=[
                    Model(
                        name="gpt-35-turbo",
                        label="GPT-3.5 Turbo",
                        description="GPT-3.5 Turbo model",
                        context_window=16385,
                        training_data="Sep 2021",
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.single,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME],
                    ),
                    Model(
                        name="gpt-4",
                        label="GPT-4",
                        description="GPT-4 model",
                        context_window=8192,
                        training_data="Sep 2021",
                        prices=[
                            Price(
                                token=Token(
                                    input_value=30.00,
                                    output_value=60.00,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            )
                        ],
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.single,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME],
                    ),
                    Model(
                        name="dall-e-2",
                        label="DALL·E-2",
                        description="DALL·E-2 model for image generation",
                        context_window=None,
                        training_data="Nov 2022",
                        prices=[
                            Price(
                                pixel=Pixel(
                                    width=1024,
                                    height=1024,
                                    value=0.020,
                                ),
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=512,
                                    height=512,
                                    value=0.018,
                                ),
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=256,
                                    height=256,
                                    value=0.016,
                                ),
                                currency=Currency.USD,
                            ),
                        ],
                        category=Category(
                            generation_type=GenerationType.image,
                            modal_type=ModalType.multi,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME],
                    ),
                    Model(
                        name="dall-e-3",
                        label="DALL·E-3",
                        description="DALL·E-3 model for advanced image generation",
                        context_window=None,
                        training_data="Nov 2023",
                        prices=[
                            Price(
                                pixel=Pixel(
                                    width=1024,
                                    height=1024,
                                    quality=ImageQuality.STANDARD,
                                    value=0.040,
                                ),
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=1792,
                                    height=1024,
                                    quality=ImageQuality.STANDARD,
                                    value=0.080,
                                ),
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=1024,
                                    height=1024,
                                    quality=ImageQuality.HD,
                                    value=0.080,
                                ),
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=1792,
                                    height=1024,
                                    quality=ImageQuality.HD,
                                    value=0.120,
                                ),
                                currency=Currency.USD,
                            ),
                        ],
                        category=Category(
                            generation_type=GenerationType.image,
                            modal_type=ModalType.multi,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME, ProcessType.STREAM],
                    ),
                    Model(
                        name="gpt-4o",
                        label="GPT-4o",
                        description="GPT-4 multimodal",
                        context_window=128000,
                        training_data="Oct 2023",
                        prices=[
                            Price(
                                token=Token(
                                    input_value=2.50,
                                    output_value=10.00,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=1024,
                                    height=1024,
                                    quality=ImageQuality.STANDARD,
                                    value=0.001913,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                        ],
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.multi,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME, ProcessType.STREAM],
                    ),
                    Model(
                        name="gpt-4o-mini",
                        label="GPT-4o Mini",
                        description="GPT-4o Smaller Variant",
                        context_window=64000,
                        training_data="Oct 2023",
                        prices=[
                            Price(
                                token=Token(
                                    input_value=0.15,
                                    output_value=0.60,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                            Price(
                                pixel=Pixel(
                                    width=1024,
                                    height=1024,
                                    quality=ImageQuality.STANDARD,
                                    value=0.003825,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                        ],
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.multi,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME],
                    ),
                    Model(
                        name="text-embedding-ada-002",
                        label="Text Embedding Ada 002",
                        description="Ada 002 for embedding",
                        prices=[
                            Price(
                                token=Token(
                                    input_value=0.10,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                        ],
                        category=Category(
                            generation_type=GenerationType.embedding,
                            modal_type=ModalType.single,
                        ),
                        enabled=True,
                        process_type=[ProcessType.REALTIME],
                    ),
                    Model(
                        name="gpt-4o-batch",
                        label="GPT-4o Batch",
                        description="GPT-4o for batch requests",
                        endpoint=[Endpoint(name=EndpointName.CHAT)],
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.single,
                        ),
                        prices=[
                            Price(
                                token=Token(
                                    input_value=2.50,
                                    output_value=7.50,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                        ],
                        enabled=True,
                        process_type=[ProcessType.BATCH],
                    ),
                    Model(
                        name="gpt-4o-mini-batch",
                        label="GPT-4o Mini Batch",
                        description="GPT-4o smaller variant for batch requests",
                        endpoint=[Endpoint(name=EndpointName.CHAT)],
                        category=Category(
                            generation_type=GenerationType.text,
                            modal_type=ModalType.single,
                        ),
                        prices=[
                            Price(
                                token=Token(
                                    input_value=0.075,
                                    output_value=0.30,
                                ),
                                unit_of_measure=UnitOfMeasure.MILLION,
                                currency=Currency.USD,
                            ),
                        ],
                        enabled=True,
                        process_type=[ProcessType.BATCH],
                    ),
                ],
            ),
        ]
