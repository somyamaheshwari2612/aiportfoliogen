import os
from document_input.parser import parse_resume
from ai.gemini import generate_portfolio_json
from analysis.completeness import calculate_completeness
from generator.html_generator import generate_portfolio
from prompts import PORTFOLIO_GENERATION_PROMPT
from config import Config

import tempfile

def save_uploaded_file(file):
    """Saves the uploaded file to a temporary file and returns the path."""
    fd, filepath = tempfile.mkstemp(suffix=os.path.splitext(file.filename)[1])
    with os.fdopen(fd, 'wb') as f:
        file.save(f)
    return filepath

def generate_resume_portfolio(file, theme):
    """
    Orchestrates the pipeline:
    1. Save file
    2. Parse text
    3. Generate JSON via AI
    4. Calculate completeness
    5. Generate HTML
    6. Save HTML to output
    """
    filepath = None
    try:
        # 1. Save
        filepath = save_uploaded_file(file)
        
        # 2. Parse
        resume_text = parse_resume(filepath)
        
        # 3. AI
        portfolio_json = generate_portfolio_json(resume_text, PORTFOLIO_GENERATION_PROMPT)
        
        # 4. Completeness
        result = calculate_completeness(portfolio_json)
        completeness = result["score"]
        missing = result["missing"]
        
        # 5. Generate & Save HTML
        output_path = generate_portfolio(portfolio_json, theme=theme)
        
        # We could also generate PDF here in the future
        
        return {
            "success": True,
            "completeness": completeness,
            "missing": missing,
            "theme": theme,
            "output_path": output_path
        }
    finally:
        # Cleanup temporary file to prevent disk exhaustion
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
