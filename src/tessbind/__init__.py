"""
Copyright (c) 2024 Enno Richter. All rights reserved.

tessbind: Tesseract pybind11 bindings
"""

from __future__ import annotations

from ._core import PageSegMode
from ._version import version as __version__
from .manager import TessbindManager

__all__ = ["PageSegMode", "TessbindManager", "__version__"]
