import base64
from pydantic import BaseModel
from datetime import datetime


class ReceiptEntry(BaseModel):
    quantity: int
    name: str
    price: float


# TODO: deal with discrepancies between subtotal and sum of items
# need to think about if we should error, or warn, or something else??
class TranscribedReceipt(BaseModel):
    vendor: str
    datetime: datetime
    items: list[ReceiptEntry]
    subtotal: float
    grand_total: float


class TranscribedReceipts(BaseModel):
    transcribed_receipts: list[TranscribedReceipt]


class Receipt:
    def __init__(self, filepath):
        self._filepath: str = filepath
        self._b64: str | None = None

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def b64(self) -> str:
        if not self._b64:
            with open(self._filepath, "rb") as image_file:
                self._b64 = base64.b64encode(image_file.read()).decode()

        return self._b64
