from pypdf import PdfReader
from pypdf.errors import PdfReadError

def parse_pdf(path):
    """
    Parses a PDF file and extracts text from all pages.
    """
    try:
        text_parts = []
        links_found = set()
        
        with open(path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                # Extract visual text
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    
        return "\n".join(text_parts)
    except PdfReadError as e:
        raise RuntimeError(f"Corrupted or invalid PDF file: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF file: {e}")
