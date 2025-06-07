from enum import Enum, StrEnum
from typing import Generic, TypeVar

from pydantic import BaseModel
from .extract import TransactionReceiptPair

DEFAULT_CATEGORIES = [
    "GROCERIES",
    "EATING_OUT",
    "TRANSPORTATION",
    "HOUSING",
    "HEALTHCARE",
    "PERSONAL_CARE",
    "ENTERTAINMENT",
    "SAVINGS_AND_INVESTMENTS",
    "DEBT_PAYMENT",
    "MISC",
]


def set_categories_enum(
    classifications_list: list[str] | None = None,
) -> type[StrEnum]:
    return StrEnum("Classifications", classifications_list or DEFAULT_CATEGORIES)


def categorize_pairs(pairs: list[TransactionReceiptPair]):
    pass


T = TypeVar("T", bound=BaseModel)


class Categorized(BaseModel, Generic[T]):
    content: T
    category: Enum

    def __init__(self, content: T):
        self.content = content
