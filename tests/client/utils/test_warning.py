# third party
import pytest

# first party
from py_nasa_api.client.const import DEFAULT_API_KEY
from py_nasa_api.client.utils import warning


@pytest.mark.parametrize(
    ("api_key", "should_warn"),
    [
        ("Hello, World!", False),
        (DEFAULT_API_KEY, True),
    ],
)
def test_warn_if_is_default_api_key(api_key: str, should_warn: bool, recwarn: pytest.WarningsRecorder):
    warning.warn_if_is_default_api_key(api_key)
    assert len(recwarn) == should_warn


@pytest.mark.parametrize(
    ("path", "n_warnings"),
    [
        ("", 1),  # no `/`
        ("?", 2),  # no `/`; ends with `?`
        ("&", 2),  # no `/`; ends with `&`
        ("??", 3),  # no `/`; multiple `?`; ends with `?`
        ("/?", 1),  # ends with `?`
        ("/&", 1),  # ends with `&`
        ("/??", 2),  # multiple `?`; ends with `?`
        ("/?&", 1),  # ends with `&`
    ],
)
def test_warn_if_path_is_incorrect(path: str, n_warnings: int, recwarn: pytest.WarningsRecorder):
    warning.warn_if_path_is_incorrect(path)
    assert len(recwarn) == n_warnings
