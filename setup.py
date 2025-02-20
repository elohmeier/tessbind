# Copyright (c) 2024, Enno Richter
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/elohmeier/tessbind for details.

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from setuptools import setup  # isort:skip
from setuptools.command.build_ext import build_ext

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
        include_dirs=[
            "extern/leptonica/leptonica-install/include",
            "extern/tesseract/tesseract-install/include",
        ],
        extra_objects=[
            "extern/leptonica/leptonica-install/lib/libleptonica.a",
            "extern/libpng/libpng-install/lib/libpng16.a",
            "extern/tesseract/tesseract-install/lib/libtesseract.a",
        ],
    ),
]


class CustomBuildExt(build_ext):
    def run(self):
        # Build dependencies first
        subprocess.check_call(["./build_dependencies.sh"])
        super().run()


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
)
