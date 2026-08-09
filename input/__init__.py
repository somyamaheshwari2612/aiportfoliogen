"""
Input document parsing package for AI Resume Portfolio Generator.
Exposes parsers for TXT, PDF, and DOCX files along with main parse_resume interface.
"""

from input.parser import parse_resume
from input.txt_parser import read_txt
from input.pdf_parser import read_pdf
from input.docx_parser import read_docx

__all__ = [
    "parse_resume",
    "read_txt",
    "read_pdf",
    "read_docx",
]
