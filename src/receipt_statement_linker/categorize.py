from enum import Enum, StrEnum, auto
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, model_serializer

from .receipt import Receipt, ReceiptEntry, TranscribedReceipt
from .statement import Transaction
from .pair import TransactionReceiptPair

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


T = TypeVar("T", bound=BaseModel)


class Categorized(BaseModel, Generic[T]):
    content: T
    category: Enum

    # NOTE(Rehan): keep category on same level as content basemodel when dumping
    @model_serializer(mode="plain")
    def _flatten(self) -> dict[str, Any]:
        if isinstance(self.content, BaseModel):
            data: dict[str, Any] = self.content.model_dump()
        else:
            data: dict[str, Any] = {"content": self.content}

        data["category"] = self.category
        return data


class CategorizedReceipt(Receipt):
    items: list[Categorized[ReceiptEntry]]

    @classmethod
    def from_transcribed_receipt(
        cls,
        transcribed_receipt: TranscribedReceipt,
        categorized_entries: list[Categorized[ReceiptEntry]],
    ):
        return cls(
            vendor=transcribed_receipt.vendor,
            datetime=transcribed_receipt.datetime,
            subtotal=transcribed_receipt.subtotal,
            grand_total=transcribed_receipt.grand_total,
            items=categorized_entries,
        )


# TODO(Rehan): wanted to subclass TransactionReceiptPair, but idk it is messy, maybe revisit later
class CategorizedTransactionReceiptPair(BaseModel):
    transaction: Categorized[Transaction]
    receipt: CategorizedReceipt | None

    @classmethod
    def from_transaction_receipt_pair(
        cls,
        transaction: Categorized[Transaction],
        receipt: CategorizedReceipt | None,
    ):
        return cls(transaction=transaction, receipt=receipt)


def categorize_pairs(
    pairs: list[TransactionReceiptPair], categories_enum: type[Enum]
) -> list[CategorizedTransactionReceiptPair]:
    transactions, receipts = (
        TransactionReceiptPair.extract_transactions(pairs),
        TransactionReceiptPair.extract_receipts(pairs),
    )
    categorized_transactions = categorize_transactions(transactions, categories_enum)
    categorized_receipts = categorize_receipts(receipts, categories_enum)

    return [
        CategorizedTransactionReceiptPair.from_transaction_receipt_pair(
            transaction, receipt
        )
        for transaction, receipt in zip(categorized_transactions, categorized_receipts)
    ]


class PlaceholderEnum(StrEnum):
    TEST = auto()


def categorize_transactions(
    # NOTE(Rehan): skeleton, need to set up proper categorization
    # plan:
    # - send in with indicies
    # - structured output with list of basemodel that has index and categorization fields to fill
    # - might have to do that thing I did before with creating new base model on the fly to use dynamic enum
    transactions: list[Transaction],
    categories_enum: type[Enum],
) -> list[Categorized[Transaction]]:
    return [
        Categorized(content=transaction, category=PlaceholderEnum.TEST)
        for transaction in transactions
    ]


def categorize_receipts(
    receipts: list[TranscribedReceipt | None], categories_enum: type[Enum]
) -> list[CategorizedReceipt | None]:
    # NOTE(Rehan): skeleton, need to set up proper categorization
    # plan:
    # - send in with indicies
    # - structured output with list of basemodel that has index and categorization fields to fill
    # - might have to do that thing I did before with creating new base model on the fly to use dynamic enum
    categorized_receipts = []
    for receipt in receipts:
        if receipt is None:
            categorized_receipts.append(receipt)
            continue

        categorized_entries = [
            Categorized(content=item, category=PlaceholderEnum.TEST)
            for item in receipt.items
        ]

        categorized_receipts.append(
            CategorizedReceipt.from_transcribed_receipt(receipt, categorized_entries)
        )
    return categorized_receipts
