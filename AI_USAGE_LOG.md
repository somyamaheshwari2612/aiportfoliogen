# AI Usage Log

This document tracks the use of AI tools during the development of this project.

---

## Log Entry Template

| Field            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Date**         | Date of usage                                                               |
| **AI Tool**      | Name and version of the AI tool (e.g., Google Gemini 2.5 Pro, ChatGPT-4o)  |
| **Prompt**       | The exact prompt or instruction given to the AI                             |
| **Generated Output** | Summary or excerpt of what the AI produced                             |
| **Changes Made** | What was actually used, modified, or discarded from the AI's output         |

---

## Entries

### Entry 1
- **Date:** 2026-08-09
- **AI Tool:** Google Gemini (Antigravity IDE Agent)
- **Prompt:** Review the parser implementation for security issues, crash vectors, and interface mismatches.
- **Generated Output:** Identified that the PDF hyperlink extractor was missing `mailto:` URL filtering, the completeness algorithm returned `int` instead of `dict` on failure, and the Jinja template inconsistently used dot vs `.get()` notation.
- **Changes Made:** Applied targeted fixes to `pdf_parser.py`, `completeness.py`, and `portfolio.html`. Added `sanitize_portfolio_data()` to `services.py` to enforce type safety on AI outputs.

### Entry 2
- **Date:** 2026-08-09
- **AI Tool:** Google Gemini (Antigravity IDE Agent)
- **Prompt:** List 20 realistic inputs that will cause failures, incorrect outputs, or unexpected behavior. Prioritize bugs over style issues.
- **Generated Output:** Identified critical failure modes including UTF-16 encoding crashes, truncated Gemini JSON, type mismatches (string vs list), and "None" string links rendering as broken HTML anchors.
- **Changes Made:** Added multi-encoding fallback to `txt_parser.py`, user-friendly JSON error messages in `gemini.py`, and comprehensive type sanitization in `services.py`.

### Entry 3
- **Date:** 2026-08-09
- **AI Tool:** Google Gemini (Antigravity IDE Agent)
- **Prompt:** Create comprehensive unit tests for parsers and AI module. Update README and INTERFACES.md.
- **Generated Output:** Generated test suites for TXT/PDF/DOCX parsers, mocked Gemini API tests, and full project documentation.
- **Changes Made:** Created `tests/test_gemini.py`, updated `tests/test_parser.py`, rewrote `README.md`, updated `INTERFACES.md` to match actual function signatures, and created this `AI_USAGE_LOG.md`.

---

*Add new entries above this line following the template.*
