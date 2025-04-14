from litellm.types.utils import ModelResponse

from .statement import (
    TranscribedStatements,
)
from .receipt import FileInput, TranscribedReceipts
import textwrap
import litellm


litellm.enable_json_schema_validation


# TODO: use enum and dispatcher to specify extractor?
async def receipts_extract(receipts: list[FileInput]):
    return await receipt_to_json(receipts)


async def receipt_to_json(receipts: list[FileInput]):
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
    assert isinstance(response, ModelResponse)
    assert isinstance(response.choices[0], litellm.Choices)
    assert response.choices[0].message.content is not None

    return TranscribedReceipts.model_validate_json(response.choices[0].message.content)


async def statements_extract(statements: list[FileInput]):
    return await statement_to_json(statements)


async def statement_to_json(statements: list[FileInput]):
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
    assert isinstance(response, ModelResponse)
    assert isinstance(response.choices[0], litellm.Choices)
    assert response.choices[0].message.content is not None

    return TranscribedStatements.model_validate_json(
        response.choices[0].message.content
    )
