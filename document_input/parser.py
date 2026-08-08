import os
import re
from .txt_parser import parse_txt
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx

def parse_resume(path):
    """
    Routes the file to the correct parser based on extension and cleans the resulting text.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == '.txt':
        raw_text = parse_txt(path)
    elif ext == '.pdf':
        raw_text = parse_pdf(path)
    elif ext == '.docx':
        raw_text = parse_docx(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    if not raw_text or not raw_text.strip():
        raise ValueError("Parsed document is empty or could not be read.")

    # Global whitespace cleaning
    cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
    return cleaned_text
