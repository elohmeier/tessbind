from __future__ import annotations

import importlib.metadata
from pathlib import Path

import tessbind as m


def test_version():
    assert importlib.metadata.version("tessbind") == m.__version__


def test_ocr_mgr():
    sample_file = Path(__file__).parent / "hello.png"

    with m.TessbindManager() as tb:
        s, c = tb.ocr_image_bytes(sample_file.read_bytes())
        assert s == "Hello, World!\n"
        assert c >= 0.8
