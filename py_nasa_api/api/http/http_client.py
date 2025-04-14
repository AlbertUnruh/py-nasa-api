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

    _session: ClientSession | None

    def __init__(self, api_key: str = DEFAULT_API_KEY):
        self.api_key = api_key
        self._session = None

    async def __aenter__(self) -> ClientSession:
        """Create a session."""
        self._session = ClientSession()
        await self._session.__aenter__()
        return self._session

    async def __aexit__(self, *exc: ...) -> None:
        """Close the session."""
        await self._session.__aexit__(*exc)
        self._session = None

    @property
    def headers(self) -> dict[str, str]:
        """Headers for http requests."""
        return {"User-Agent": self.user_agent}

    async def request(self, route: BaseRoute) -> HTTPResponse:
        """Make a request to NASA."""
        session = self._session

        if new_session_needed := session is None:  # create session if none is present
            session = await self.__aenter__()

        url = route.url + ("&" if "?" in route.url else "?") + f"api_key={self.api_key}"

        async with session.request(route.method, url, headers=self.headers) as response:
            http_response = HTTPResponse(await response.read(), encoding=response.get_encoding())

        if new_session_needed:  # close session if session was just created
            await self.__aexit__(None, None, None)

        return http_response
