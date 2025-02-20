# Copyright (c) 2024, Enno Richter
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/elohmeier/tessbind for details.

from __future__ import annotations

import subprocess
from pathlib import Path

from setuptools import setup  # isort:skip
from setuptools.command.build_ext import build_ext

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)


def get_lib_dirs() -> dict[str, str]:
    """Get the library directory names from the build process."""
    lib_dirs = {"ZLIB_LIB": "lib", "LIBPNG_LIB": "lib", "LEPTONICA_LIB": "lib", "TESSERACT_LIB": "lib"}
    try:
        with Path("lib_dirs.txt").open() as f:
            for line in f:
                key, value = line.strip().split("=")
                lib_dirs[key] = value
    except FileNotFoundError:
        pass  # Use defaults
    return lib_dirs

lib_dirs = get_lib_dirs()

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
            f"extern/tesseract/tesseract-install/{lib_dirs['TESSERACT_LIB']}/libtesseract.a",
            f"extern/leptonica/leptonica-install/{lib_dirs['LEPTONICA_LIB']}/libleptonica.a",
            f"extern/libpng/libpng-install/{lib_dirs['LIBPNG_LIB']}/libpng16.a",
            f"extern/zlib/zlib-install/{lib_dirs['ZLIB_LIB']}/libz.a",
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
