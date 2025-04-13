from .receipt import Receipt


# TODO: use enum and dispatcher to specify extractor?
def receipts_extract(receipt_input_filepaths: list[str]):
    receipts = [Receipt(filepath) for filepath in receipt_input_filepaths]
    b64s = [receipt.b64 for receipt in receipts]
