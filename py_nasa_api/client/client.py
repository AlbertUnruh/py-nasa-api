__all__ = ("APIClient",)


# local
from .utils.warning import warn_if_is_default_api_key


class APIClient:
    """The API client which acts as an interface between every NASA endpoint and your code."""

    # APIs
    ...  # noqa

    def __init__(self, api_key: str):
        warn_if_is_default_api_key(api_key)
        ...  # noqa
