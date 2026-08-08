"""
Input document parsing package for AI Resume Portfolio Generator.
Exposes parsers for TXT, PDF, and DOCX files along with main parse_resume interface.
"""

from input.parser import parse_resume
from input.txt_parser import read_txt, parse_txt
from input.pdf_parser import read_pdf, parse_pdf
from input.docx_parser import read_docx, parse_docx

__all__ = [
    "parse_resume",
    "read_txt",
    "parse_txt",
    "read_pdf",
    "parse_pdf",
    "read_docx",
    "parse_docx",
]
