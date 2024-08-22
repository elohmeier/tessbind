from __future__ import annotations

import os
import pathlib
import platform
import shutil
import subprocess


class TessdataPrefixUnsetError(Exception):
    """Raised when the TESSDATA_PREFIX environment variable is not set."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__("TESSDATA_PREFIX not set")


def get_tessdata_prefix() -> str:
    """Get the path to the Tesseract data directory.

    This function will attempt to find the Tesseract data directory by checking
    the TESSDATA_PREFIX environment variable and common system locations.
    """

    # Environment variable takes precedence
    tessdata = os.environ.get("TESSDATA_PREFIX")
    if tessdata:
        return tessdata

    system = platform.system()

    if system == "Linux":
        path = pathlib.Path(
            "/usr/share/tesseract-ocr/5/tessdata"
        )  # Ubuntu default location
        if path.exists():
            return str(path)

    def _find_tessdata(root_dir: str) -> str | None:
        root = pathlib.Path(root_dir)

        if not root.exists():
            return None

        for path in root.iterdir():
            if path.is_dir() and path.name.startswith("5."):
                return str(path / "share/tessdata")

        return None

    if system == "Darwin":
        brew_path = shutil.which("brew")
        if brew_path:
            brew_prefix = subprocess.check_output(
                [brew_path, "--prefix"], text=True
            ).strip()
            tessdata = _find_tessdata(f"{brew_prefix}/Cellar/tesseract/")
            if tessdata:
                return str(tessdata)

    raise TessdataPrefixUnsetError()
