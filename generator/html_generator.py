from jinja2 import Environment, FileSystemLoader

VALID_THEMES = ["modern", "minimal", "glass", "dark"]

def generate_portfolio(data, theme="modern", output_path="portfolio.html", template_name="portfolio.html"):
    """
    data: dict (parsed Gemini JSON) - from Member 1
    theme: 'modern' | 'minimal' | 'glass' | 'dark'
    output_path: file to save final HTML to
    template_name: which template to render (portfolio.html or preview.html)
    """
    if theme not in VALID_THEMES:
        theme = "modern"

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)

    rendered_html = template.render(data=data, theme=theme)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"Portfolio generated: {output_path} (theme: {theme})")
    return output_path


if __name__ == "__main__":
    sample_data = {
        "name": "Test User",
        "headline": "Aspiring Developer",
        "summary": "A short bio goes here for testing purposes.",
        "skills": ["Python", "HTML", "CSS", "Jinja2"],
        "education": [
            {"degree": "B.Tech CSE", "institution": "ABC University", "year": "2025"}
        ],
        "experience": [],
        "projects": [
            {"title": "Portfolio Generator", "description": "This exact project.", "technologies": "Python, Jinja2"}
        ],
        "achievements": ["Hackathon Winner 2025"],
        "contact": {"email": "test@test.com", "github": "github.com/test"}
    }

    for t in VALID_THEMES:
        generate_portfolio(sample_data, theme=t, output_path=f"portfolio_{t}.html")