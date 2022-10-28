"""Auto versioning code."""
from importlib.metadata import PackageNotFoundError, version

"""Get version or set it to 0.0.0."""
try:
    __version__ = version("oakx-oger")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
