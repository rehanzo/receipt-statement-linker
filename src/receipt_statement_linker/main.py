import argparse
import asyncio
from .extract import receipts_extract
from .receipt import ImageInput


async def main():
    parser = argparse.ArgumentParser(
        description="Parse receipt images and output data."
    )
    parser.add_argument(
        "--receipt-input", nargs="+", required=True, help="Receipt images to parse"
    )
    parser.add_argument(
        "--receipt-output", required=True, help="Filepath to output receipt data"
    )
    args = parser.parse_args()

    receipt_input_filepaths: list[str] = args.receipt_input
    receipt_output_filepath: str = args.receipt_output

    receipts = [ImageInput(filepath) for filepath in receipt_input_filepaths]
    receipt_extracts = await receipts_extract(receipts)


if __name__ == "__main__":
    asyncio.run(main())
