import base64


class Receipt:
    _filepath: str

    def __init__(self, filepath):
        self._filepath = filepath
        self._b64 = None

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def b64(self) -> bytes:
        if not self._b64:
            with open(self._filepath, "rb") as image_file:
                self._b64 = base64.b64encode(image_file.read())

        return self._b64
