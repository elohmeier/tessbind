"""
Copyright (c) 2024 Enno Richter. All rights reserved.

tessbind: Tesseract pybind11 bindings
"""

from __future__ import annotations

from ._core import PageSegMode
from .manager import TessbindManager

__version__ = "0.0.6"

__all__ = ["__version__", "PageSegMode", "TessbindManager"]
