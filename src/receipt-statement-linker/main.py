import argparse


def main():
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

    print(f"receipt_input={args.receipt_input}, receipt_output={args.receipt_output}")


if __name__ == "__main__":
    main()
