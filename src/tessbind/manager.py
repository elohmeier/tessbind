from __future__ import annotations

from typing import Any

import tessbind._core as m
from tessbind.utils import get_tessdata_prefix


class RecognitionFailedError(Exception):
    """An error raised when OCR recognition fails."""

    def __init__(self) -> None:
        """Initialize the RecognitionFailedError."""
        super().__init__("OCR recognition failed.")


class TessbindManager:
    """A context manager for handling Tesseract OCR bindings.

    This class manages the lifecycle of a Tessbind object, which provides
    bindings to the Tesseract OCR engine.
    """

    _api: m.TessBaseAPI
    """The low-level Tesseract API object."""

    tessdata_prefix: str
    """The path to the Tesseract data directory."""

    lang: str
    """The language used for OCR."""

    def __init__(
        self,
        tessdata_prefix: str | None = None,
        lang: str = "eng",
        page_seg_mode: m.PageSegMode | None = None,
    ) -> None:
        """Initialize the TessbindManager.

        Args:
            tessdata_prefix (Optional[str]): The path to the Tesseract data directory.
                If None, it will try to use the TESSDATA_PREFIX environment variable.
            lang (str): The language to use for OCR. Defaults to "eng".
            page_seg_mode (Optional[PageSegMode]): The page segmentation mode to use by default.
        """
        if tessdata_prefix is None:
            tessdata_prefix = get_tessdata_prefix()

        self.tessdata_prefix = tessdata_prefix
        self.lang = lang

        self._api = m.TessBaseAPI(self.tessdata_prefix, self.lang)

        if page_seg_mode is not None:
            self.page_seg_mode = page_seg_mode

    def __enter__(self) -> TessbindManager:
        """Enter the runtime context and initialize the Tessbind object.

        Returns:
            TessbindManager: The initialized TessbindManager object.
        """
        return self

    def ocr_image_bytes(self, img_bytes: bytes) -> tuple[str, int]:
        """Perform OCR on an image represented as bytes.

        Args:
            img_bytes (bytes): The image data as bytes.

        Returns:
            tuple[str, int]: A tuple containing the OCR text result and the confidence score (0-100).
        """
        self._api.set_image_from_bytes(img_bytes)

        ret = self._api.recognize()

        if ret != 0:
            raise RecognitionFailedError()

        return self._api.utf8_text, self._api.all_word_confidences

    @property
    def page_seg_mode(self) -> m.PageSegMode:
        """Get the current page segmentation mode."""
        return self._api.page_seg_mode

    @page_seg_mode.setter
    def page_seg_mode(self, value: m.PageSegMode) -> None:
        """Set the page segmentation mode."""
        self._api.page_seg_mode = value

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit the runtime context and clean up the Tessbind object.

        Args:
            exc_type: The exception type, if an exception was raised.
            exc_val: The exception value, if an exception was raised.
            exc_tb: The traceback, if an exception was raised.
        """
        if self._api is not None:
            self._api.end()
