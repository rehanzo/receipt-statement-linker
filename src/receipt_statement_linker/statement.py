from pydantic import BaseModel, Field, create_model
from datetime import datetime

from .categories import set_categories_enum


class Transaction(BaseModel):
    name: str
    datetime: datetime
    withdrawl_amount: float | None
    deposit_amount: float | None


class TranscribedStatement(BaseModel):
    opening_balance: float | None
    transactions: list[Transaction]
    closing_balance: float | None


class TranscribedStatements(BaseModel):
    transcribed_statements: list[TranscribedStatement]


def get_transcribed_statements_class(
    categories_list: list[str] | None,
) -> type[TranscribedStatements]:
    transaction_class = create_model(
        "Transaction",
        category=(
            set_categories_enum(categories_list),
            Field(...),
        ),
        __base__=Transaction,
    )

    transcribed_statement_class = create_model(
        "TranscribedStatement",
        transactions=(list[transaction_class], Field(...)),
        __base__=TranscribedStatement,
    )

    transcribed_statements_class = create_model(
        "TranscribedStatements",
        transcribed_statements=(list[transcribed_statement_class], Field(...)),
        __base__=TranscribedStatements,
    )
    return transcribed_statements_class
