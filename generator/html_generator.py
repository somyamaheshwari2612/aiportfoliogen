import os
from flask import render_template
from config import Config

def generate_portfolio(portfolio_json, theme="modern"):
    """
    TODO(Generator Team): Implement proper jinja variables and theming logic.
    MOCK IMPLEMENTATION: Renders the template for end-to-end pipeline testing.
    """
    print("⚠️ WARNING: generate_portfolio() is currently using a MOCK implementation.")
    # Render the template using Flask/Jinja
    html_content = render_template("portfolio.html", portfolio=portfolio_json, theme=theme)
    
    # Write to output folder
    if not os.path.exists(Config.OUTPUT_FOLDER):
        os.makedirs(Config.OUTPUT_FOLDER)
        
    output_html_path = os.path.join(Config.OUTPUT_FOLDER, "portfolio.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return output_html_path
