from enum import Enum
from typing import List, Optional, Dict
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


class Severity(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Citation(BasePayload):
    url: str
    license: str


class Category(str, Enum):
    HATE = "hate"
    VIOLENCE = "violence"
    JAILBREAK = "jailbreak"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    PROFANITY = "profanity"
    PROTECTED_MATERIAL_CODE = "protected_material_code"
    PROTECTED_MATERIAL_TEXT = "protected_material_text"
    INDIRECT_ATTACK = "indirect_attack"
    CUSTOM_BLOCKLISTS = "custom_blocklists"
    ERROR = "error"


class Types(BasePayload):
    category: Category
    filtered: bool
    detected: Optional[bool] = None
    severity: Optional[Severity] = None
    citation: Optional[Citation] = None


class Completion(BasePayload):
    types: List[Types]


class Prompt(BasePayload):
    types: List[Types]


class ContentFilter(BasePayload):
    completion: Optional[Completion] = None
    prompt: Optional[Prompt] = None


class GuardrailResponse(BasePayload):
    content_filter: ContentFilter

    @classmethod
    def from_filter_results(
        cls,
        completion_filter_results: Optional[Dict] = None,
        prompt_filter_results: Optional[Dict] = None,
    ) -> "GuardrailResponse":
        return cls(
            content_filter=ContentFilter(
                prompt=(
                    Prompt(types=cls._set_types(prompt_filter_results))
                    if prompt_filter_results
                    else None
                ),
                completion=(
                    Completion(types=cls._set_types(completion_filter_results))
                    if completion_filter_results
                    else None
                ),
            )
        )

    @staticmethod
    def _set_types(filter_results: Dict) -> List[Types]:
        return (
            [
                Types(
                    category=category,
                    filtered=results.get("filtered"),
                    detected=results.get("detected", None),
                    severity=results.get("severity", None),
                    citation=results.get("citation", None),
                )
                for category, results in filter_results.items()
            ]
            if filter_results
            else []
        )
