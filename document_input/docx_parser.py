import docx

def parse_docx(path):
    """
    Parses a DOCX file and extracts text from all paragraphs.
    """
    try:
        doc = docx.Document(path)
        text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(text_parts)
    except docx.opc.exceptions.PackageNotFoundError as e:
        raise RuntimeError(f"Corrupted or invalid DOCX file: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read DOCX file: {e}")
