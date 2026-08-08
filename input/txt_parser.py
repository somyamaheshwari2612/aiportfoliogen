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

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as file:
                return file.read()
        except Exception as err:
            raise RuntimeError(f"Failed to read text file '{path}': {err}") from err
    except Exception as err:
        raise RuntimeError(f"Failed to read text file '{path}': {err}") from err


def parse_txt(path: str) -> str:
    """Alias for read_txt to ensure backwards and interface compatibility.

    Args:
        path (str): The absolute or relative file path to the text file.

    Returns:
        str: The raw text extracted from the file.
    """
    return read_txt(path)
