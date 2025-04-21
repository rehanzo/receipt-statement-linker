from dataclasses import dataclass
from litellm.types.utils import ModelResponse

from .statement import (
    Transaction,
    TranscribedStatements,
)
from .receipt import FileInput, ReceiptEntry, TranscribedReceipt, TranscribedReceipts
import textwrap
import litellm


litellm.enable_json_schema_validation


# TODO: use enum and dispatcher to specify extractor?
async def receipts_extract(receipts: list[FileInput]) -> TranscribedReceipts:
    return await receipt_to_json(receipts)


async def receipt_to_json(receipts: list[FileInput]) -> TranscribedReceipts:
    system_prompt = textwrap.dedent(
        """
        You are an accurate receipt transcriber. You will be given image(s) of receipt(s). You will convert it to JSON output based on the schema provided.

        NOTES:
            - Ensure your datetime value is correct and in ISO 8601 format (YYYY-MM-DD HH:MM:SS.sssZ)
            - Item name is to be just the name. Do not include quantity in the name. Quantity has its own field.
        """
    ).strip()
    receipts_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpg;base64,{receipt.b64}"
            },  # TODO: not always jpeg
        }
        for receipt in receipts
    ]

    messages: list[dict] = [
        {"content": system_prompt, "role": "system"},
        {"role": "user", "content": receipts_content},
    ]
    response = await litellm.acompletion(
        model="gemini/gemini-2.0-flash",
        messages=messages,
        response_format=TranscribedReceipts,
        temperature=0,
    )

    # TODO: Better way to work around this for type checking? or is this just an unfortunate design decision by litellm??
    # response can be ModelResponse or CustomStreamWrapper, latter doesn't have `choices` field...
    assert isinstance(response, ModelResponse)
    assert isinstance(response.choices[0], litellm.Choices)
    assert response.choices[0].message.content is not None

    return TranscribedReceipts.model_validate_json(response.choices[0].message.content)


async def statements_extract(statements: list[FileInput]) -> TranscribedStatements:
    return await statement_to_json(statements)


async def statement_to_json(statements: list[FileInput]) -> TranscribedStatements:
    system_prompt = textwrap.dedent(
        """
        You are an accurate bank statement transcriber. You will be given bank statement(s). You will convert it to JSON output based on the schema provided.

        NOTES:
            - Ensure your datetime value is correct and in ISO 8601 format (YYYY-MM-DD HH:MM:SS.sssZ).
            - Do not include opening and closing balances in transactions. They belong in their respective fields.
        """
    ).strip()
    statement_content = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:application/pdf;base64,{statement.b64}"},
        }
        for statement in statements
    ]

    messages: list[dict] = [
        {"content": system_prompt, "role": "system"},
        {"role": "user", "content": statement_content},
    ]
    response = await litellm.acompletion(
        model="gemini/gemini-2.0-flash",
        messages=messages,
        response_format=TranscribedStatements,
        temperature=0,
    )

    # COPYPASTA: receipt_to_json
    # TODO: Better way to work around this for type checking? or is this just an unfortunate design decision by litellm??
    # response can be ModelResponse or CustomStreamWrapper, latter doesn't have `choices` field...
    assert isinstance(response, ModelResponse)
    assert isinstance(response.choices[0], litellm.Choices)
    assert response.choices[0].message.content is not None

    return TranscribedStatements.model_validate_json(
        response.choices[0].message.content
    )


@dataclass
class TransactionReceiptPair:
    transaction: Transaction
    receipt: TranscribedReceipt


async def merge_statements_receipts(
    statements: TranscribedStatements, receipts: TranscribedReceipts
) -> list[TransactionReceiptPair]:
    # plan:
    # - match on price since likelihood of price matching exactly is low
    # - check if vendor match
    #   - we can do this the dumb way first (receipt vendor in )
    pairs: list[TransactionReceiptPair] = []

    for statement in statements.transcribed_statements:
        for transaction in statement.transactions:
            price_match_receipts = [
                receipt
                for receipt in receipts.transcribed_receipts
                if receipt.grand_total == transaction.withdrawl_amount
            ]

            if not price_match_receipts:
                # TODO(Rehan): Handle case where no price match
                pass

            elif len(price_match_receipts) == 1:
                pairs.append(
                    TransactionReceiptPair(transaction, price_match_receipts[0])
                )

            else:
                name_match_receipts = [
                    receipt
                    for receipt in price_match_receipts
                    if await receipt.vendor_match_transaction_name(transaction)
                ]

                if len(name_match_receipts) == 1:
                    pairs.append(
                        TransactionReceiptPair(transaction, name_match_receipts[0])
                    )
                else:
                    # TODO(Rehan): Handle cases where no name match or multiple name matches
                    pass

    return pairs
