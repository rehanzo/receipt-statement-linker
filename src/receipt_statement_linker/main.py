import argparse
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
    # parser.add_argument(
    #     "--receipt-output", required=True, help="Filepath to output receipt data"
    # )
    args = parser.parse_args()

    receipt_input_filepaths: list[str] = args.receipt_input
    statement_input_filepaths: list[str] = args.statement_input

    receipts = [FileInput(filepath) for filepath in receipt_input_filepaths]
    receipt_extracts = await receipts_extract(receipts)

    statements = [FileInput(filepath) for filepath in statement_input_filepaths]
    statement_extracts = await statements_extract(statements)

    # merge
    merged = await merge_statements_receipts(statement_extracts, receipt_extracts)


if __name__ == "__main__":
    asyncio.run(main())
