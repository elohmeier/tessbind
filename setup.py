# Copyright (c) 2024, Enno Richter
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/elohmeier/tessbind for details.

from __future__ import annotations

import subprocess

from setuptools import setup  # isort:skip
from setuptools.command.build_ext import build_ext

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)


def get_lib_dirs() -> dict[str, str]:
    """Detect if we installed libs in lib64 or lib."""

    from pathlib import Path

    zlib_lib = "lib64" if Path("extern/zlib/zlib-install/lib64").exists() else "lib"
    libpng_lib = (
        "lib64" if Path("extern/libpng/libpng-install/lib64").exists() else "lib"
    )
    leptonica_lib = (
        "lib64" if Path("extern/leptonica/leptonica-install/lib64").exists() else "lib"
    )
    tesseract_lib = (
        "lib64" if Path("extern/tesseract/tesseract-install/lib64").exists() else "lib"
    )

    return {
        "ZLIB_LIB": zlib_lib,
        "LIBPNG_LIB": libpng_lib,
        "LEPTONICA_LIB": leptonica_lib,
        "TESSERACT_LIB": tesseract_lib,
    }


ext_modules = [
    Pybind11Extension(
        "tessbind._core",
        ["src/main.cpp"],
        cxx_std=11,
        include_dirs=[
            "extern/leptonica/leptonica-install/include",
            "extern/tesseract/tesseract-install/include",
        ],
    ),
]


class CustomBuildExt(build_ext):
    def run(self):
        # Build dependencies first
        subprocess.check_call(["./build_dependencies.sh"])
        # Now that lib_dirs.txt is created, read it and assign extra_objects
        libs = get_lib_dirs()
        for ext in self.extensions:
            if ext.name == "tessbind._core":
                ext.extra_objects = [
                    # do not change the ordering of these objects
                    f"extern/tesseract/tesseract-install/{libs['TESSERACT_LIB']}/libtesseract.a",
                    f"extern/leptonica/leptonica-install/{libs['LEPTONICA_LIB']}/libleptonica.a",
                    f"extern/libpng/libpng-install/{libs['LIBPNG_LIB']}/libpng16.a",
                    f"extern/zlib/zlib-install/{libs['ZLIB_LIB']}/libz.a",
                ]
        super().run()


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
)
