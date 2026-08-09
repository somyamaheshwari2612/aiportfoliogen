# Teammate Module Interfaces

This document serves as the contract between the different modules of the AI Resume Portfolio Generator. When building your assigned module, please ensure your functions match these signatures, return the expected types, and raise the specified exceptions when things go wrong.

---

### 1. Document Parsing (`input/parser.py`)

```python
def parse_resume(path: str) -> str
```

**Description:** Reads the uploaded file from the local disk, determines the file type (`.txt`, `.pdf`, `.docx`), and delegates to the appropriate sub-parser to extract the raw text.
**Expected Input:** `/absolute/path/to/resume.pdf`
**Expected Output:** `"John Doe\nSoftware Engineer\nExperience...\n"`
**Raises:**
- `FileNotFoundError`: If the provided path does not exist.
- `ValueError`: If the file extension is not supported.
- `RuntimeError`: If the text extraction library (e.g., pypdf, docx) fails to read the file.

---

### 2. AI Extraction (`ai/gemini.py`)

```python
def generate_portfolio_json(resume_text: str, prompt: str) -> dict
```

**Description:** Sends the raw resume text and system prompt to the Google Gemini API to extract structured information.
**Expected Input:** `"John Doe\nSoftware Engineer..."`, `"You are an expert AI..."`
**Expected Output:** 
```json
{
  "personal_info": {"name": "John Doe", "email": "john@example.com", "location": "New York"},
  "social_links": {
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "website": "",
    "other": []
  },
  "summary": "Experienced software engineer...",
  "experience": [],
  "education": [],
  "skills": ["Python", "Flask"],
  "projects": []
}
```
**Raises:**
- `ValueError`: If the provided resume text is empty, if the AI detects the file is not a resume (`is_resume=False`), or if the JSON cannot be parsed.
- `Exception`: Bubbles up any underlying `google.genai` exceptions if the API is unreachable or times out.

---

### 3. Completeness Scoring (`analysis/completeness.py`)

```python
```python
def calculate_completeness(portfolio_json: dict) -> dict
```

**Description:** Analyzes the structured portfolio dictionary and calculates a score representing how thoroughly the resume was parsed (e.g., checking if all standard sections exist).
**Expected Input:** The dictionary output from `generate_portfolio_json`.
**Expected Output:** `{"score": 85, "missing": ["Education", "GitHub Profile"]}`
**Raises:**
- None. This module is guaranteed to act as a fail-safe. If the dictionary is completely empty or grossly malformed, it catches all internal exceptions and returns `{"score": 0, "missing": ["Could not calculate score due to malformed data"]}`.

---

### 4. HTML Generation (`generator/html_generator.py`)

```python
def generate_portfolio(portfolio_json: dict, theme: str = "modern") -> str
```

**Description:** Injects the portfolio dictionary into a Jinja2 template (`templates/portfolio.html`), applies the selected CSS theme, and writes the final rendered HTML to the disk.
**Expected Input:** The dictionary output from `generate_portfolio_json`, and a theme string (`"modern"`, `"minimal"`, `"glass"`, `"dark"`).
**Expected Output:** `/absolute/path/to/output/portfolio.html` (The path to the saved file).
**Raises:**
- `ValueError`: If an unsupported theme name is provided.
- `RuntimeError`: If Jinja2 template rendering fails.
- `IOError`: If the application lacks permission to write to the `output/` directory.
