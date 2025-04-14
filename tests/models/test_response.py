# third party
import pytest

# first party
from py_nasa_api.models import response


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ((_ := b""), _),
        ((_ := b"Hello, World!"), _),
        ((_ := "Do you feel the VÆB?".encode()), _),
    ],
)
def test_http_response_response(data: bytes, expected: bytes):
    assert response.HTTPResponse(data).response == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ((_ := b""), _.decode()),
        ((_ := b"Hello, World!"), _.decode()),
        ((_ := b"Do you feel the V\xc3\x86B?"), _.decode()),
    ],
)
def test_http_response_text(data: bytes, expected: str):
    assert response.HTTPResponse(data).text == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"[]", []),
        (b"[{}, {}]", [{}, {}]),
        (b'{"foo": "bar"}', {"foo": "bar"}),
        (b'{"V\xc3\x86B": true}', {"VÆB": True}),
    ],
)
def test_http_response_json(data: bytes, expected: dict | list):
    assert response.HTTPResponse(data).json == expected
