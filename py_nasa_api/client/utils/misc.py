__all__ = ("add_missing_parameters",)


# standard library
from collections.abc import Iterable


def add_missing_parameters(path: str, parameters: Iterable[str]) -> str:
    """Add any missing parameters to the path.

    Parameters
    ----------
    path : str
        The possibly incomplete path.
    parameters : Iterable[str]
        The names of the parameters.

    Returns
    -------
    str
        The updated path.
    """
    to_append: list[str] = [f"{parameter}={key}" for parameter in parameters if (key := f"{{{parameter}}}") not in path]

    if to_append:
        path += ("&" if "?" in path else "?") + "&".join(to_append)
    return path
