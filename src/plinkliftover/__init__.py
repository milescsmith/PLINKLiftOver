# type: ignore[attr-defined]
"""Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""
from typing import Optional

import logging

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
