# standard library
from collections.abc import Iterable

# third party
import pytest

# first party
from py_nasa_api.client.utils import misc


@pytest.mark.parametrize(
    "path",
    ["/", "/{foo}", "/?foo={foo}", "/?mystery={foo}"],
)
@pytest.mark.parametrize(
    "parameters",
    [
        {},
        {"foo": ...},
        {"foo": ..., "bar": ...},
        (),
        ("foo",),
        ("foo", "bar"),
    ],
)
def test_add_missing_parameters(path: str, parameters: Iterable[str]):
    corrected_path = misc.add_missing_parameters(path, parameters)
    for parameter in parameters:
        assert f"{{{parameter}}}" in corrected_path
    assert corrected_path.count("?") == bool(parameters) or path == corrected_path
    assert corrected_path.count("&") <= len(list(parameters))
