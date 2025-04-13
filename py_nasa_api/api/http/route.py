__all__ = ("BaseRoute",)


# standard library
from typing import ClassVar
from urllib.parse import quote as _uri_quote

# first party
from py_nasa_api.client.utils.misc import add_missing_parameters
from py_nasa_api.client.utils.warning import warn_if_path_is_incorrect


class BaseRoute:
    """Base for every API route."""

    BASE: ClassVar[str]  # not static; different between APIs

    path: str
    method: str
    params: dict[str, ...]

    def __init__(self, method: str, path: str, **parameters: ...):
        if warn_if_path_is_incorrect(path):
            # now the search begins...
            if not path.startswith("/"):
                path = f"/{path}"
            path = path.removesuffix("&").removesuffix("?")

        path = add_missing_parameters(path, parameters)

        self.path = path
        self.method = method
        self.params = parameters

    @property
    def resolved_path(self) -> str:
        """The endpoint for this route, with all parameters resolved."""
        return self.path.format_map({k: _uri_quote(v) if isinstance(v, str) else v for k, v in self.params.items()})

    @property
    def url(self) -> str:
        """The full url for this route."""
        return f"{self.BASE}{self.resolved_path}"
