"""StockScope - A Python package for tracking and analyzing stock data."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("stockscope")
except PackageNotFoundError:
    __version__ = "unknown"
