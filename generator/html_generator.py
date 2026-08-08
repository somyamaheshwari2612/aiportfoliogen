import os
from jinja2 import Environment, FileSystemLoader, TemplateError

VALID_THEMES = ["modern", "minimal", "glass", "dark"]


def generate_portfolio(portfolio_json: dict, theme: str = "modern") -> str:
    """
    portfolio_json: dict - structured data from Gemini (Teammate 2's output)
    theme: 'modern' | 'minimal' | 'glass' | 'dark'
    Returns: absolute path to the saved portfolio.html file
    """
    if theme not in VALID_THEMES:
        raise ValueError(f"Unsupported theme '{theme}'. Must be one of {VALID_THEMES}")

    try:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("portfolio.html")
        
        # Read CSS to inline it so the downloaded HTML works standalone
        with open("static/css/portfolio_base.css", "r", encoding="utf-8") as f:
            base_css = f.read()
        with open(f"static/css/{theme}.css", "r", encoding="utf-8") as f:
            theme_css = f.read()
            
        rendered_html = template.render(data=portfolio_json, theme=theme, base_css=base_css, theme_css=theme_css)
    except TemplateError as e:
        raise RuntimeError(f"Jinja2 template rendering failed: {e}")

    output_dir = "output"
    output_path = os.path.join(output_dir, "portfolio.html")

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
    except IOError as e:
        raise IOError(f"Failed to write portfolio.html: {e}")

    return os.path.abspath(output_path)


if __name__ == "__main__":
    # PLACEHOLDER — matches real schema from INTERFACES.md
    sample_data = {
        "personal_info": {
            "name": "Test User",
            "email": "test@test.com",
            "location": "New York"
        },
        "social_links": {
            "linkedin": "https://linkedin.com/in/testuser",
            "github": "https://github.com/testuser",
            "website": "",
            "other": []
        },
        "summary": "A short bio goes here for testing purposes.",
        "skills": ["Python", "HTML", "CSS", "Jinja2"],
        "education": [
            {"degree": "B.Tech CSE", "institution": "ABC University", "year": "2025"}
        ],
        "experience": [],
        "projects": [
            {"title": "Portfolio Generator", "description": "This exact project.", "technologies": "Python, Jinja2"}
        ]
    }

    for t in VALID_THEMES:
        path = generate_portfolio(sample_data, theme=t)
        print(f"Generated: {path}")