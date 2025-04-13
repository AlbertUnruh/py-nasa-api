__all__ = (
    "warn_if_is_default_api_key",
    "warn_if_path_is_incorrect",
)


# standard library
from warnings import warn

# first party
from py_nasa_api.client.const import DEFAULT_API_KEY


def warn_if_is_default_api_key(api_key: str) -> bool:
    """Warn if the default API key is used.

    Parameters
    ----------
    api_key : str
        The API key to check.

    Returns
    -------
    bool
        True if warning was issued.
    """
    if api_key == DEFAULT_API_KEY:
        warn(
            f"You are using the default API key ({api_key}). "
            f"This will greatly impact call limits! "
            f"Please consider generating a personal API key over at https://api.nasa.gov/#signUp",
            category=RuntimeWarning,
            stacklevel=3,
        )
        return True
    return False


def warn_if_path_is_incorrect(path: str) -> bool:
    """Warn if the path is incomplete.

    Parameters
    ----------
    path : str
        The path to check.

    Returns
    -------
    bool
        True if warning was issued.
    """
    warned = False
    if not path.startswith("/"):
        warn(
            f"Path {path!r} is missing a leading `/`!",
            category=UserWarning,
            stacklevel=3,
        )
        warned = True
    if path.count("?") > 1:
        warn(
            f"Path {path!r} contains more than one `?`!",
            category=UserWarning,
            stacklevel=3,
        )
    for invalid_end in ("&", "?"):
        if path.endswith(invalid_end):
            warn(
                f"Path {path!r} has leading `{invalid_end}`!",
                category=UserWarning,
                stacklevel=3,
            )
            warned = True
    return warned
