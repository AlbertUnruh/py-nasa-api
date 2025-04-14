# third party
import pytest

# first party
from py_nasa_api.api.http import route


@pytest.mark.parametrize(
    "parameters",
    [
        {"foo": 1},
        {"foo": 1, "bar": "two"},
    ],
)
def test_base_route_parameters(parameters: dict[str, ...]):
    base_route = route.BaseRoute("GET", "/test/{foo}", **parameters)
    for k, v in parameters.items():
        assert str(v) in base_route.resolved_path, f"Value of parameter {k!r} not in resolved path!"


def test_base_route_quote():
    base_route = route.BaseRoute("GET", "/{foo}", foo=" ", bar="+")
    assert base_route.resolved_path == "/%20?bar=%2B"


def test_base_route_no_base():
    base_route = route.BaseRoute("GET", "/")
    with pytest.raises(AttributeError):
        _ = base_route.BASE
    with pytest.raises(AttributeError):
        _ = base_route.url


@pytest.mark.parametrize(
    ("path", "should_warn"),
    [
        ("/", False),
        ("", True),
    ],
)
def test_base_route_warn(path: str, should_warn: bool, recwarn: pytest.WarningsRecorder):
    route.BaseRoute("GET", path)
    assert len(recwarn) == should_warn


@pytest.mark.parametrize(
    ("base", "should_warn"),
    [
        ("", False),
        ("/", True),
        ("https://127.0.0.1", False),
        ("https://127.0.0.1/", True),
        ("https://127.0.0.1/api", False),
        ("https://127.0.0.1/api/", True),
    ],
)
def test_route_warn(base: str, should_warn: bool, recwarn: pytest.WarningsRecorder):
    class _Route(route.BaseRoute):
        BASE = base

    assert len(recwarn) == should_warn
