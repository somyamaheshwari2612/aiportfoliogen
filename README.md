# 🎨 AI Resume Portfolio Generator

An intelligent web application that transforms your resume into a beautifully designed, downloadable portfolio website — powered by Google Gemini AI.

Upload a `.txt`, `.pdf`, or `.docx` resume, select a theme, and receive a production-ready single-page portfolio in seconds.

---

## 📁 Folder Structure

```
aiportfoliogen/
├── app.py                      # Flask web server and routes
├── services.py                 # Pipeline orchestrator (upload → parse → AI → score → generate)
├── config.py                   # Centralized configuration (themes, file limits, model name)
├── prompts.py                  # System prompt sent to Gemini
├── INTERFACES.md               # Module contract / API signatures
├── requirements.txt            # Python dependencies
│
├── input/                      # Resume parsing module
│   ├── parser.py               # Dispatcher: routes files to txt/pdf/docx sub-parsers
│   ├── txt_parser.py           # Plain text extraction (multi-encoding support)
│   ├── pdf_parser.py           # PDF text + secure hyperlink extraction
│   └── docx_parser.py          # DOCX paragraph + table extraction
│
├── ai/                         # AI integration module
│   └── gemini.py               # Google Gemini API client (JSON extraction)
│
├── analysis/                   # Resume quality analysis
│   └── completeness.py         # Completeness scoring algorithm (0–100 + missing fields)
│
├── generator/                  # HTML portfolio generation
│   └── html_generator.py       # Jinja2 renderer with inline CSS for portability
│
├── templates/                  # Jinja2 HTML templates
│   ├── index.html              # Upload page (frontend)
│   └── portfolio.html          # Generated portfolio template
│
├── static/                     # Static assets
│   ├── css/                    # Base + theme stylesheets
│   │   ├── portfolio_base.css
│   │   ├── modern.css
│   │   ├── minimal.css
│   │   ├── glass.css
│   │   └── dark.css
│   └── js/
│       └── preview.js          # Frontend preview logic
│
├── output/                     # Generated portfolio files (gitignored)
├── tests/                      # Unit test suite
│   ├── test_parser.py          # Parser tests (TXT, PDF, DOCX, edge cases)
│   ├── test_completeness.py    # Completeness scoring tests
│   └── test_gemini.py          # AI module tests (mocked)
└── .env                        # Environment variables (gitignored)
```

---

## 🛠 Installation

### Prerequisites
- Python 3.10+
- A Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Setup

```bash
# Clone the repository
git clone https://github.com/somyamaheshwari2612/aiportfoliogen.git
cd aiportfoliogen

# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

| Variable        | Required | Description                            |
|-----------------|----------|----------------------------------------|
| `GEMINI_API_KEY`| Yes      | Your Google Gemini API key             |

---

## 🚀 Running Locally

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`. Open it in your browser, upload a resume, pick a theme, and click **Generate**.

---

## 📄 Supported Resume Formats

| Format | Extension | Notes                                          |
|--------|-----------|------------------------------------------------|
| Text   | `.txt`    | UTF-8, UTF-8-BOM, UTF-16, and Latin-1 supported |
| PDF    | `.pdf`    | Text-based PDFs only (scanned images not supported) |
| Word   | `.docx`   | Microsoft Word 2007+ format                    |

---

## ✨ Features

- **AI-Powered Extraction:** Uses Google Gemini to intelligently parse resume text into structured JSON (personal info, skills, experience, education, projects, certifications, and more).
- **4 Premium Themes:** Modern, Minimal, Glass, and Dark — each with a unique visual identity.
- **Completeness Scoring:** Calculates a 0–100 quality score and lists missing fields to help improve your resume.
- **Portable Output:** The generated `portfolio.html` is a single, self-contained file with all CSS inlined — no server required to view it.
- **Security:** Jinja2 auto-escaping prevents XSS attacks. PDF hyperlink extraction is filtered to safe protocols only (`http`, `https`, `mailto`).
- **Type Sanitization:** AI output is rigorously validated and sanitized before rendering to prevent crashes from hallucinated data types.
- **Robust Parsing:** Handles corrupt files, empty files, unsupported encodings, and scanned PDFs with clear, user-friendly error messages.

---

## 🧪 Testing

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Or with `unittest`:

```bash
python -m unittest discover tests -v
```

### Test Coverage

| Module                | Test File               | What's Tested                                            |
|-----------------------|-------------------------|----------------------------------------------------------|
| `input/parser.py`     | `test_parser.py`        | TXT/PDF/DOCX parsing, empty files, corrupt files, unsupported extensions |
| `analysis/completeness.py` | `test_completeness.py` | Scoring, deduplication, bonus points, malformed data     |
| `ai/gemini.py`        | `test_gemini.py`        | Empty input, invalid JSON, empty response, API errors (mocked) |

---

## ⚠️ Known Limitations

1. **Scanned PDFs:** Image-based (scanned) PDFs cannot be parsed. OCR is not supported.
2. **Two-Column Layouts:** Complex multi-column PDF layouts may produce jumbled text extraction.
3. **AI Hallucinations:** Gemini may occasionally invent details not present in the resume, especially for well-known names.
4. **Token Limits:** Very long resumes (50+ pages, academic CVs) are rejected to prevent API token overflow.
5. **Non-English Resumes:** The AI may translate or hallucinate field names for non-English resumes.
6. **Single User:** The `output/portfolio.html` file is overwritten on each generation. Concurrent users would overwrite each other's output.

---

## 🔮 Future Improvements

- [ ] **PDF Download:** Generate a downloadable PDF version of the portfolio.
- [ ] **OCR Support:** Integrate Tesseract or Google Cloud Vision for scanned PDF parsing.
- [ ] **User Accounts:** Allow users to save and manage multiple portfolios.
- [ ] **Custom Themes:** Allow users to upload their own CSS themes.
- [ ] **Multi-Language Support:** Detect resume language and localize the portfolio output.
- [ ] **Deployment:** Deploy to a cloud platform (Railway, Render, Vercel).
- [ ] **Rate Limiting:** Add API rate limiting to prevent abuse.
