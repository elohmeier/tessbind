from __future__ import annotations

def add(_x: int, _y: int) -> int:
    """
    Add two numbers.
    """

def subtract(_x: int, _y: int) -> int:
    """
    Subtract two numbers.

    Args:
        _x (int): The first number.
        _y (int): The second number to subtract from the first.

    Returns:
        int: The result of subtracting _y from _x.
    """

def api_version() -> str:
    """
    Returns the version identifier of the Tesseract API.

    Returns:
        str: A string representing the version of the Tesseract API.
    """

class TessBaseAPI:
    """
    A class that provides an low-level interface to the Tesseract OCR engine.

    This class allows for initialization of the Tesseract API, setting image data,
    performing OCR, and retrieving results. It also provides control over page
    segmentation modes and access to word confidences.
    """

    def __init__(self, datapath: str, language: str) -> None:
        """
        Initialize Tesseract API with the given datapath and language.

        Args:
            datapath (str): Path to the Tesseract data directory.
            language (str): Language for OCR.
        """

    def end(self) -> None:
        """
        Close down tesseract and free up all memory, after which the instance should not be reused.
        """

    @property
    def page_seg_mode(self) -> PageSegMode:
        """Get the current page segmentation mode."""

    @page_seg_mode.setter
    def page_seg_mode(self, value: PageSegMode) -> None:
        """
        Set the page segmentation mode.
        """

    def set_image_from_bytes(self, content: bytes) -> None:
        """
        Set the image data for OCR processing.

        Args:
            content (bytes): The image data as bytes.
        """

    @property
    def utf8_text(self) -> str:
        """
        Get the OCR result as UTF-8 text.

        Returns:
            str: The recognized text in UTF-8 encoding.
        """

    @property
    def all_word_confidences(self) -> int:
        """
        Get the confidence values for all words in the result.

        Returns:
            int: An integer representing the confidence values.
        """

    def recognize(self) -> int:
        """
        Perform OCR on the set image.

        Returns:
            int: An integer indicating the success of the OCR operation.
        """

class PageSegMode:
    """Enumeration of page segmentation settings."""

    OSD_ONLY: PageSegMode
    """Segment the page in "OSD only" mode"""

    AUTO_OSD: PageSegMode
    """Segment the page in "Auto OSD" mode"""

    AUTO_ONLY: PageSegMode
    """Segment the page in "Automatic only" mode"""

    AUTO: PageSegMode
    """Segment the page in "Automatic" mode"""

    SINGLE_COLUMN: PageSegMode
    """Segment the page in "Single column" mode"""

    SINGLE_BLOCK_VERT_TEXT: PageSegMode
    """Segment the page in "Single block of vertical text" mode"""

    SINGLE_BLOCK: PageSegMode
    """Segment the page in "Single block" mode"""

    SINGLE_LINE: PageSegMode
    """Segment the page in "Single line" mode"""

    SINGLE_WORD: PageSegMode
    """Segment the page in "Single word" mode"""

    CIRCLE_WORD: PageSegMode
    """Segment the page in "Circle word" mode"""

    SINGLE_CHAR: PageSegMode
    """Segment the page in "Single character" mode"""

    SPARSE_TEXT: PageSegMode
    """Segment the page in "Sparse text" mode"""

    SPARSE_TEXT_OSD: PageSegMode
    """Segment the page in "Sparse text OSD" mode"""

    RAW_LINE: PageSegMode
    """Segment the page in "Raw line" mode"""

    COUNT: PageSegMode
    """Segment the page in "Count" mode"""
