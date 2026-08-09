"""
Module for extracting raw text from plain text (.txt) files.
"""

import os


def read_txt(path: str) -> str:
    """Reads and extracts text from a plain text (.txt) file.

    Args:
        path (str): The absolute or relative file path to the text file.

    Returns:
        str: The raw text extracted from the file.

    Raises:
        FileNotFoundError: If the file at path does not exist or is not a file.
        RuntimeError: If an error occurs while reading the file.
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"Text file not found: {path}")

    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin-1']
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except Exception as err:
            raise RuntimeError(f"Failed to read text file '{path}': {err}") from err
            
    raise RuntimeError(f"Failed to decode text file '{path}'. Unsupported encoding.")



