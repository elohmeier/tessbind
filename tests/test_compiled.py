from __future__ import annotations

from pathlib import Path

import pytest

import tessbind._core as m
from tessbind.utils import get_tessdata_prefix

try:
    from tqdm.auto import trange
except ImportError:
    trange = range


def test_add():
    assert m.add(2, 3) == 5


def test_subtract():
    assert m.subtract(7, 5) == 2


def test_api_version():
    assert m.api_version().startswith("5.")


def test_lowlevel_ocr():
    sample_file = Path(__file__).parent / "hello.png"

    tessdata = get_tessdata_prefix()

    tb = m.TessBaseAPI(tessdata, "eng")

    tb.set_image_from_bytes(sample_file.read_bytes())

    res = tb.recognize()
    assert res == 0

    s = tb.utf8_text
    assert s == "Hello, World!\n"

    c = tb.all_word_confidences
    assert c > 0.8

    tb.end()


@pytest.mark.slow
def test_many_calls():
    sample_file = Path(__file__).parent / "hello.png"

    tessdata = get_tessdata_prefix()

    tb = m.TessBaseAPI(tessdata, "eng")

    for _ in trange(1000):
        tb.set_image_from_bytes(sample_file.read_bytes())

        res = tb.recognize()
        assert res == 0

        s = tb.utf8_text
        assert s == "Hello, World!\n"

        c = tb.all_word_confidences
        assert c > 0.8

    tb.end()
