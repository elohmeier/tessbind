# tessbind

[![CI][ci-badge]][ci-link]
[![CD][cd-badge]][cd-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
[![License][license-badge]][license-link]

Python 3.12+ bindings for Tesseract built with pybind11. The package vendors the native dependencies (leptonica, libpng, zlib) so you only need Tesseract's trained data files available at runtime.

## Installation

```bash
pip install tessbind
```

Tesseract language data must be discoverable. If it is not installed in a default location (e.g., `/usr/share/tesseract-ocr/5/tessdata` on Linux or the Homebrew Cellar on macOS), set `TESSDATA_PREFIX` to the directory that contains the `tessdata` folder.

## Usage

`TessbindManager` wraps the underlying API in a context manager and exposes the recognized UTF-8 text plus per-word confidences:

```python
from pathlib import Path

from tessbind import PageSegMode, TessbindManager

img_bytes = Path("tests/hello.png").read_bytes()

with TessbindManager(lang="eng", page_seg_mode=PageSegMode.SINGLE_LINE) as tb:
    text, confidences = tb.ocr_image_bytes(img_bytes)

print(text)         # -> Hello, World!
print(confidences)  # list of word-level confidences (0-100)
```

Use the `page_seg_mode` setter to change segmentation between calls, or omit it to rely on Tesseract's default.

## Development

- `uv sync --extra test` to create the venv and build vendored libraries.
- `uv run pytest -m "not slow"` to run the test suite.

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[ci-badge]:       https://github.com/elohmeier/tessbind/actions/workflows/ci.yaml/badge.svg
[ci-link]:        https://github.com/elohmeier/tessbind/actions/workflows/ci.yaml
[cd-badge]:       https://github.com/elohmeier/tessbind/actions/workflows/cd.yaml/badge.svg
[cd-link]:        https://github.com/elohmeier/tessbind/actions/workflows/cd.yaml
[pypi-link]:      https://pypi.org/project/tessbind/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/tessbind
[pypi-version]:   https://img.shields.io/pypi/v/tessbind
[license-badge]:  https://img.shields.io/pypi/l/tessbind
[license-link]:   https://github.com/elohmeier/tessbind/blob/master/LICENSE

<!-- prettier-ignore-end -->
