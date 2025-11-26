from __future__ import annotations

from pathlib import Path

import pytest

import tessbind._core as m
from tessbind.manager import TessbindManager
from tessbind.utils import get_tessdata_prefix

try:
    from tqdm.auto import trange
except ImportError:
    trange = range


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

    confidences = tb.all_word_confidences
    assert confidences
    assert all(80 <= c <= 100 for c in confidences)

    tb.end()


def test_manager_roundtrip():
    sample_file = Path(__file__).parent / "hello.png"

    with TessbindManager() as tm:
        text, confidences = tm.ocr_image_bytes(sample_file.read_bytes())

    assert text == "Hello, World!\n"
    assert confidences
    assert all(80 <= c <= 100 for c in confidences)


def test_manager_after_close():
    tm = TessbindManager()
    tm.close()

    with pytest.raises(RuntimeError):
        tm.ocr_image_bytes(b"invalid")


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

        confidences = tb.all_word_confidences
        assert confidences
        assert all(0 <= c <= 100 for c in confidences)

    tb.end()
