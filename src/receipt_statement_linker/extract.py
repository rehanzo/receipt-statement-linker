from litellm.types.utils import ModelResponse
from .receipt import Receipt, TranscribedReceipts
import textwrap
import litellm


litellm.enable_json_schema_validation


# TODO: use enum and dispatcher to specify extractor?
async def receipts_extract(receipts: list[Receipt]):
    return await receipt_to_json(receipts)


async def receipt_to_json(receipts: list[Receipt]):
    system_prompt = textwrap.dedent(
        """
        You are an accurate receipt transcriber. You will be given image(s) of receipt(s). You will convert it to JSON output based on the schema provided.

        NOTES:
            - Ensure your datetime value is correct and in ISO 8601 format (YYYY-MM-DD HH:MM:SS.sssZ)
            - Item name is to be just the name. Do not include quantity in the name. Quantity has its own field.
        """
    ).strip()
    # user_message = "Here are images of the receipts. Output JSON in order as one contiguous output."
    messages: list[dict] = [
        {"content": system_prompt, "role": "system"},
    ]

    receipts_content = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpg;base64,{receipt.b64}"},
        }
        for receipt in receipts
    ]
    messages.append({"role": "user", "content": receipts_content})
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
