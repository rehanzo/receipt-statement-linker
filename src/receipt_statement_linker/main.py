import argparse
import json
import asyncio
from .extract import merge_statements_receipts, receipts_extract, statements_extract
from .receipt import FileInput


async def main():
    parser = argparse.ArgumentParser(
        description="Parse receipt images and output data."
    )
    parser.add_argument(
        "--receipt-input", nargs="+", required=True, help="Receipt images to parse"
    )
    parser.add_argument(
        "--statement-input", nargs="+", required=True, help="Statement images to parse"
    )
    parser.add_argument(
        "--receipt-output", required=True, help="Filepath to output receipt data"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        required=False,
        help="List of categories",
    )
    args = parser.parse_args()

    receipt_input_filepaths: list[str] = args.receipt_input
    statement_input_filepaths: list[str] = args.statement_input

    receipts = [FileInput(filepath) for filepath in receipt_input_filepaths]
    receipt_extracts = await receipts_extract(receipts, args.categories)

    statements = [FileInput(filepath) for filepath in statement_input_filepaths]
    statement_extracts = await statements_extract(statements, args.categories)

    # merge
    pairs = await merge_statements_receipts(statement_extracts, receipt_extracts)

    pairs_json = [json.loads(pair.model_dump_json()) for pair in pairs]

    with open(args.receipt_output, "w") as f:
        json.dump(pairs_json, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
