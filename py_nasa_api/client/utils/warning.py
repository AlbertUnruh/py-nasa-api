__all__ = ("warn_if_is_default_api_key",)


# standard library
from warnings import warn

# first party
from py_nasa_api.client.const import DEFAULT_API_KEY


def warn_if_is_default_api_key(api_key: str) -> bool:
    """Warn if the default API key is used."""
    if api_key == DEFAULT_API_KEY:
        warn(
            f"You are using the default API key ({DEFAULT_API_KEY}). "
            f"This will greatly impact call limits! "
            f"Please consider generating a personal API key over at https://api.nasa.gov/#signUp",
            category=RuntimeWarning,
            stacklevel=3,
        )
        return True
    return False
