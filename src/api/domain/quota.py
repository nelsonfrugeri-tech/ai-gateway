from uuid import uuid4
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class QuotaUnit(Enum):
    TOKENS = "tokens"


class Model(BaseModel):
    name: str


class Provider(BaseModel):
    name: str
    model: Model


class UseCase(BaseModel):
    id: str
    name: str


class Quota(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    unit: QuotaUnit
    limit: int
    balance: Optional[int] = Field(default=None)
    use_case: UseCase
    provider: Provider
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    enabled: bool = Field(True)

    model_config = ConfigDict(use_enum_values=True)

    def __init__(self, **data):
        super().__init__(**data)
        if self.balance is None:
            self.balance = self.limit

    def to_dict(self):
        return self.model_dump(by_alias=True)


class QuotaUpdate(BaseModel):
    enabled: bool = Field(default=False)
    model_config = ConfigDict(use_enum_values=True)
