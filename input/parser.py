"""
Main parser interface for processing resume files in TXT, PDF, and DOCX formats.
"""

import os
from input.txt_parser import read_txt
from input.pdf_parser import read_pdf
from input.docx_parser import read_docx


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def parse_resume(path: str) -> str:
    """Reads a resume file, routes it to the correct parser by file extension,
    normalizes the extracted text, and strips blank lines.

    Args:
        path (str): File path to the resume document (.txt, .pdf, .docx).

    Returns:
        str: A single normalized string containing the full text of the resume.

    Raises:
        FileNotFoundError: If the provided path does not exist or is not a valid file.
        ValueError: If the file extension is unsupported or the file contains no text.
        RuntimeError: If document parsing fails due to corruption or formatting errors.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("Invalid path parameter. Expected a non-empty string.")

    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"Resume file not found at path: '{path}'")

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format '{ext}'. Supported extensions are: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    # Route to appropriate parser
    if ext == ".txt":
        raw_text = read_txt(path)
    elif ext == ".pdf":
        raw_text = read_pdf(path)
    elif ext == ".docx":
        raw_text = read_docx(path)
    else:
        raise ValueError(f"No parser available for extension '{ext}'")

    # Normalize text: strip lines, eliminate empty/blank lines
    normalized_lines = [
        line.strip() for line in raw_text.splitlines() if line.strip()
    ]

    cleaned_text = "\n".join(normalized_lines)

    if not cleaned_text:
        raise ValueError(f"Resume file '{path}' is empty or contains no readable text content.")

    return cleaned_text
