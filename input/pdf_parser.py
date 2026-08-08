"""
Module for extracting text content from PDF (.pdf) files using pypdf.
"""

import os
import pypdf
from pypdf.errors import PyPdfError


def read_pdf(path: str) -> str:
    """Extracts text content from a PDF document across all pages.

    Args:
        path (str): Path to the PDF file.

    Returns:
        str: Concatenated text content extracted from all PDF pages.

    Raises:
        FileNotFoundError: If the PDF file does not exist at the specified path.
        RuntimeError: If the PDF is corrupted, encrypted with unknown key, or unparseable.
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"PDF file not found: {path}")

    try:
        reader = pypdf.PdfReader(path)
        extracted_pages = []

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(text)

        return "\n".join(extracted_pages)
    except PyPdfError as err:
        raise RuntimeError(f"Corrupted or invalid PDF file '{path}': {err}") from err
    except Exception as err:
        raise RuntimeError(f"Failed to read PDF file '{path}': {err}") from err


def parse_pdf(path: str) -> str:
    """Alias for read_pdf to maintain interface flexibility.

    Args:
        path (str): Path to the PDF file.

    Returns:
        str: Extracted text content from the PDF.
    """
    return read_pdf(path)
