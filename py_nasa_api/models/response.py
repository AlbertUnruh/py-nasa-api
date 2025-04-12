# third party
import orjson


class HTTPResponse:
    """Container for http responses."""

    _data: bytes
    encoding: str

    def __init__(self, response: bytes, /, *, encoding: str = "utf-8"):
        self._data = response
        self.encoding = encoding

    @property
    def response(self) -> bytes:
        """Raw response data."""
        return self._data

    @property
    def text(self) -> str:
        """Response as text."""
        return self._data.decode(self.encoding)

    @property
    def json(self) -> dict:
        """Response as json."""
        return orjson.loads(self._data)
