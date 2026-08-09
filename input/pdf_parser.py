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
        secure_links = set()

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(text)
                
            # Securely extract hidden hyperlinks
            if '/Annots' in page:
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    if obj.get('/Subtype') == '/Link' and '/A' in obj and '/URI' in obj['/A']:
                        uri = obj['/A']['/URI']
                        if hasattr(uri, "get_object"):
                            uri = uri.get_object()
                        if isinstance(uri, str) and uri.lower().startswith(('http://', 'https://', 'mailto:')):
                            secure_links.add(uri)

        full_text = "\n".join(extracted_pages)
        if secure_links:
            full_text += "\n\n--- EMBEDDED LINKS ---\n"
            for link in secure_links:
                full_text += f"- {link}\n"
                
        return full_text
    except PyPdfError as err:
        raise RuntimeError(f"Corrupted or invalid PDF file '{path}': {err}") from err
    except Exception as err:
        raise RuntimeError(f"Failed to read PDF file '{path}': {err}") from err



