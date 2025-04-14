__all__ = (
    "DEFAULT_API_KEY",
    "__py_version__",
    "__repository__",
    "__version__",
)


# standard library
import sys


__version__: str = "0.1.1"
__repository__: str = "https://github.com/AlbertUnruh/py-nasa-api/"


__py_version__: str = ".".join(map(str, sys.version_info[:2]))

DEFAULT_API_KEY: str = "DEMO_KEY"
