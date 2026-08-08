def generate_portfolio_json(resume_text, prompt):
    """
    TODO(AI Team): Implement actual Gemini API call using google-genai.
    MOCK IMPLEMENTATION: Returns hardcoded dict for end-to-end pipeline testing.
    """
    print("⚠️ WARNING: generate_portfolio_json() is currently using a MOCK implementation.")
    return {
        "personal_info": {
            "name": "Placeholder Name",
            "headline": "Placeholder Headline",
            "email": "test@example.com",
            "phone": "555-555-5555",
            "location": "Remote"
        },
        "social_links": {
            "linkedin": "https://linkedin.com/in/placeholder",
            "github": "https://github.com/placeholder",
            "website": "",
            "other": []
        },
        "summary": "This is a placeholder summary.",
        "skills": ["Python", "Flask", "AI"],
        "experience": [
            {
                "title": "Placeholder Title",
                "company": "Placeholder Company",
                "duration": "2020 - Present",
                "description": ["Did some things.", "Did some other things."]
            }
        ],
        "education": [],
        "projects": [],
        "achievements": [],
        "certifications": [],
        "languages": [],
        "interests": []
    }
