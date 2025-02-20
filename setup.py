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


# Add macOS-specific link arguments
if sys.platform == "darwin":
    png_prefix = (
        subprocess.check_output(["brew", "--prefix", "libpng"]).decode().strip()
    )
    for ext in ext_modules:
        # Add RPATH entries
        ext.extra_link_args = [
            "-Wl,-rpath,@loader_path/../../extern/leptonica/leptonica-install/lib",
            "-Wl,-rpath,@loader_path/../../extern/tesseract/tesseract-install/lib",
        ]

        # Add PNG paths
        ext.include_dirs.append(str(Path(png_prefix) / "include"))
        ext.library_dirs.append(str(Path(png_prefix) / "lib"))
        ext.libraries.append("png")
elif sys.platform == "linux":
    for ext in ext_modules:
        # Add RPATH entries for Linux
        ext.extra_link_args = [
            "-Wl,-rpath,$ORIGIN/../../extern/leptonica/leptonica-install/lib",
            "-Wl,-rpath,$ORIGIN/../../extern/tesseract/tesseract-install/lib",
        ]

        # On Linux, libpng-dev installs to system paths
        ext.libraries.append("png")


class CustomBuildExt(build_ext):
    def run(self):
        # Build dependencies first
        subprocess.check_call(["./build_dependencies.sh"])
        super().run()


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
)
