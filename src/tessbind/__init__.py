"""
Copyright (c) 2024 Enno Richter. All rights reserved.

tessbind: Tesseract pybind11 bindings
"""

from __future__ import annotations

from importlib.metadata import version

from ._core import PageSegMode
from .manager import TessbindManager

__version__ = version("tessbind")

__all__ = ["PageSegMode", "TessbindManager", "__version__"]
