# third party
import pytest
from pytest_httpserver import HTTPServer

# first party
from py_nasa_api.api.http import http_client
from py_nasa_api.api.http.route import BaseRoute
from py_nasa_api.client.const import __py_version__, __repository__, __version__


@pytest.mark.parametrize(
    "client",
    [
        http_client.HTTPClient,
        http_client.HTTPClient("Hello, World!"),
    ],
)
def test_http_client_user_agent_class(client: type[http_client.HTTPClient] | http_client.HTTPClient):
    assert client.user_agent
    assert __version__ in client.user_agent
    assert __repository__ in client.user_agent
    assert "python" in client.user_agent.lower()
    assert __py_version__ in client.user_agent


@pytest.mark.asyncio
async def test_http_client_session():
    client = http_client.HTTPClient("Hello, World!")
    assert client._session is None, "Session should not be present!"
    async with client:
        assert client._session is not None, "No session present!"
    assert client._session is None, "Session should not be present after context!"


def test_http_client_headers():
    client = http_client.HTTPClient("Hello, World!")
    assert isinstance(client.headers, dict)
    assert "User-Agent" in client.headers, "No user-agent in headers present!"
    assert http_client.HTTPClient.user_agent in client.headers.values(), "Pre-defined user-agent is missing!"
    assert client.headers["User-Agent"] == http_client.HTTPClient.user_agent, "Invalid user-agent header!"


class Route(BaseRoute):
    BASE = "localhost"

    def __init__(self, base: str, method: str, path: str, **parameters: ...):
        self.BASE = base
        super().__init__(method, path, **parameters)


@pytest.mark.parametrize(
    ("endpoint", "parameters"),
    [
        ("/test", {}),
        ("/test", {"foo": "bar"}),
        ("/{foo}", {"foo": "bar"}),
        ("/{foo}?egg={spam}", {"foo": "bar", "spam": True}),
    ],
)
@pytest.mark.asyncio
async def test_http_client_request_with_context(endpoint: str, parameters: dict[str, ...], httpserver: HTTPServer):
    client = http_client.HTTPClient("Hello, World!")
    route = Route(httpserver.url_for("/").removesuffix("/"), "GET", endpoint, **parameters)
    httpserver.expect_request(endpoint.format_map(parameters), route.method)
    async with client:
        assert await client.request(route)


@pytest.mark.parametrize(
    ("endpoint", "parameters"),
    [
        ("/test", {}),
        ("/test", {"foo": "bar"}),
        ("/{foo}", {"foo": "bar"}),
        ("/{foo}?egg={spam}", {"foo": "bar", "spam": True}),
    ],
)
@pytest.mark.asyncio
async def test_http_client_request_no_context(endpoint: str, parameters: dict[str, ...], httpserver: HTTPServer):
    client = http_client.HTTPClient("Hello, World!")
    route = Route(httpserver.url_for("/").removesuffix("/"), "GET", endpoint, **parameters)
    httpserver.expect_request(endpoint.format_map(parameters), route.method)
    assert await client.request(route)
