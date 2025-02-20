# Copyright (c) 2024, Enno Richter
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/elohmeier/tessbind for details.

from __future__ import annotations

import os
import sys

from setuptools import setup  # isort:skip

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        "tessbind._core",
        ["src/main.cpp"],
        cxx_std=11,
        libraries=["leptonica", "tesseract"],
        include_dirs=[
            "extern/leptonica/leptonica-install/include",
            "extern/tesseract/tesseract-install/include",
        ],
        library_dirs=[
            "extern/leptonica/leptonica-install/lib",
            "extern/tesseract/tesseract-install/lib",
        ],
    ),
]


# Add PNG paths on macOS
if sys.platform == "darwin":
    from subprocess import check_output

    png_prefix = check_output(["brew", "--prefix", "libpng"]).decode().strip()
    for ext in ext_modules:
        ext.include_dirs.append(os.path.join(png_prefix, "include"))
        ext.library_dirs.append(os.path.join(png_prefix, "lib"))
        ext.libraries.append("png")


setup(
    ext_modules=ext_modules,
)
