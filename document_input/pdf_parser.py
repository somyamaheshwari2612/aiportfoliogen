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
                
                # Extract hidden hyperlink annotations
                if '/Annots' in page:
                    for annot in page['/Annots']:
                        obj = annot.get_object()
                        if obj.get('/Subtype') == '/Link':
                            # Check for a URI action
                            if '/A' in obj and '/URI' in obj['/A']:
                                uri = obj['/A']['/URI']
                                if isinstance(uri, str):
                                    links_found.add(uri)
                                elif hasattr(uri, "get_object"):
                                    # Sometimes it's an indirect object
                                    uri_str = uri.get_object()
                                    if isinstance(uri_str, str):
                                        links_found.add(uri_str)

        full_text = "\n".join(text_parts)
        if links_found:
            full_text += "\n\n--- HIDDEN URLS FOUND IN DOCUMENT ---\n"
            for link in links_found:
                full_text += f"- {link}\n"
                
        return full_text
    except PdfReadError as e:
        raise RuntimeError(f"Corrupted or invalid PDF file: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF file: {e}")
