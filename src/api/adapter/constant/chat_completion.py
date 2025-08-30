from enum import Enum


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

    @classmethod
    def is_valid(cls, value) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_roles(cls) -> list:
        return [role.value for role in cls]
