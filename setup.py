# Copyright (c) 2024, Enno Richter
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/elohmeier/tessbind for details.

from __future__ import annotations

import platform
import subprocess

from setuptools import setup  # isort:skip
from setuptools.command.build_ext import build_ext

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)


def get_lib_dir() -> str:
    """Get the library directory name based on platform."""
    if platform.system() == "Linux" and platform.machine() == "x86_64":
        return "lib64"
    return "lib"


lib_dir = get_lib_dir()

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
            # do not change the ordering of these objects
            f"extern/tesseract/tesseract-install/{lib_dir}/libtesseract.a",
            "extern/leptonica/leptonica-install/lib/libleptonica.a",  # leptonica always uses `lib`
            f"extern/libpng/libpng-install/{lib_dir}/libpng16.a",
            f"extern/zlib/zlib-install/{lib_dir}/libz.a",
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
