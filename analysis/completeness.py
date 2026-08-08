"""
analysis/completeness.py

Ye module resume ke JSON data ko dekh kar ek "Completeness Score"
nikalta hai — matlab batata hai resume kitna complete hai.

Important:
- Isme Flask ka koi import nahi hai
- Isme Gemini/API call nahi hai
- Ye sirf ek dictionary (data) leta hai aur ek dictionary (result) return karta hai
"""

from typing import Any, Dict, List


# Har section ke liye:
# - "key" -> data me is naam se cheez dhundhi jayegi
# - "label" -> user ko dikhane wala friendly naam
# - "suggestion" -> agar ye section missing hai to kya suggest karna hai
SECTION_RULES: List[Dict[str, Any]] = [
    {
        "key": "name",
        "label": "Name",
        "suggestion": "Apna pura naam add karo taaki visitors ko pata chale ye kiska portfolio hai.",
    },
    {
        "key": "headline",
        "label": "Headline",
        "suggestion": "Ek chhota professional headline add karo (jaise 'Full Stack Developer | AI Enthusiast').",
    },
    {
        "key": "email",
        "label": "Email",
        "suggestion": "Apna email address add karo taaki recruiters contact kar sakein.",
    },
    {
        "key": "phone",
        "label": "Phone",
        "suggestion": "Direct contact ke liye phone number add karo.",
    },
    {
        "key": "education",
        "label": "Education",
        "suggestion": "Apni education details add karo (degree, institution, year).",
    },
    {
        "key": "experience",
        "label": "Experience",
        "suggestion": "Apna work experience ya internships add karo, chhota hi sahi.",
    },
    {
        "key": "skills",
        "label": "Skills",
        "suggestion": "Apni technical aur soft skills list karo.",
    },
    {
        "key": "projects",
        "label": "Projects",
        "suggestion": "2-3 projects dikhao, har ek ka chhota description ke saath.",
    },
    {
        "key": "github",
        "label": "GitHub",
        "suggestion": "Apna GitHub profile link add karo taaki tumhara code dikhe.",
    },
    {
        "key": "linkedin",
        "label": "LinkedIn",
        "suggestion": "Professional networking ke liye LinkedIn profile link add karo.",
    },
    {
        "key": "achievements",
        "label": "Achievements",
        "suggestion": "Awards, hackathon wins ya doosri achievements mention karo.",
    },
    {
        "key": "certifications",
        "label": "Certifications",
        "suggestion": "Apni profile strong banane ke liye relevant certifications add karo.",
    },
]


def _is_filled(value: Any) -> bool:
    """
    Check karta hai ki ye value 'present' maani jaye ya nahi.

    - None -> False (nahi hai)
    - Empty string ya sirf spaces wali string -> False
    - Empty list ya dictionary -> False
    - Kuch bhi aur (non-empty string/list/dict/number) -> True
    """
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def calculate_completeness(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resume ki completeness calculate karta hai.

    Args:
        data: Gemini se aayi structured resume JSON (Python dictionary).
              Expected keys jaise:
              {
                  "name": "...",
                  "headline": "...",
                  "email": "...",
                  "phone": "...",
                  "education": [...],
                  "experience": [...],
                  "skills": [...],
                  "projects": [...],
                  "github": "...",
                  "linkedin": "...",
                  "achievements": [...],
                  "certifications": [...]
              }

    Returns:
        {
            "score": int,               # 0-100 ke beech percentage
            "completed": [str, ...],    # jo sections present hain unke naam
            "missing": [str, ...],      # jo sections missing hain unke naam
            "suggestions": [str, ...]   # missing sections ke liye friendly tips
        }
    """
    if not isinstance(data, dict):
        raise TypeError("calculate_completeness ko ek dictionary chahiye input me")

    completed: List[str] = []
    missing: List[str] = []
    suggestions: List[str] = []

    for rule in SECTION_RULES:
        value = data.get(rule["key"])
        if _is_filled(value):
            completed.append(rule["label"])
        else:
            missing.append(rule["label"])
            suggestions.append(rule["suggestion"])

    total_sections = len(SECTION_RULES)
    score = round((len(completed) / total_sections) * 100)

    return {
        "score": score,
        "completed": completed,
        "missing": missing,
        "suggestions": suggestions,
    }


# Ye neeche wala hissa sirf testing ke liye hai.
# Jab tum seedha "python completeness.py" chalaogi, to ye check hoga.
if __name__ == "__main__":
    sample_data = {
        "name": "Somya Maheshwari",
        "email": "somya@example.com",
        "skills": ["Python", "Flask", "Gemini API"],
        "projects": [{"title": "AI Portfolio Generator"}],
        # baaki fields yaha nahi diye — isse "missing" me aayenge
    }

    result = calculate_completeness(sample_data)
    print("Score:", result["score"])
    print("Completed:", result["completed"])
    print("Missing:", result["missing"])
    print("Suggestions:", result["suggestions"])