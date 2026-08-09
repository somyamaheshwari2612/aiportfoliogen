def parse_txt(path):
    """
    Parses a plain text file.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback for Windows-1252 or other encodings if UTF-8 fails
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read TXT file: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read TXT file: {e}")
