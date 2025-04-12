__all__ = ("HTTPClient",)


# standard library
from typing import ClassVar

# third party
from aiohttp.client import ClientSession

# first party
from py_nasa_api.client.const import DEFAULT_API_KEY, __py_version__, __repository__, __version__
from py_nasa_api.models.response import HTTPResponse

# local
from .route import BaseRoute


class HTTPClient:
    """An http client for sending requests to the NASA API."""

    api_key: str
    user_agent: ClassVar[str] = f"py-nasa-api/{__version__} ({__repository__}) Python/{__py_version__}"

    _session: ClientSession

    def __init__(self, api_key: str = DEFAULT_API_KEY):
        self.api_key = api_key
        self._session = ClientSession()

    def __del__(self):
        """Close session when instance gets deleted."""
        self._session.close()

    @property
    def headers(self) -> dict[str, str]:
        """Headers for http requests."""
        return {"User-Agent": self.user_agent}

    async def request(self, route: BaseRoute) -> HTTPResponse:
        """Make a request to NASA."""
        url = route.url + ("&" if "?" in route.url else "?") + f"api_key={self.api_key}"
        async with self._session.request(route.method, url, headers=self.headers) as response:
            return HTTPResponse(await response.read(), encoding=response.get_encoding())
