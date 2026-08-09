"""
analysis/completeness.py

Algorithm for calculating resume completeness score (0-100) based on structured JSON data.
Implements fair section weighting, score caps, title deduplication, optional bonus points,
and fail-safe exception handling.
"""

from typing import Any, Dict, List, Set


# Base Weight Matrix (Sums to 100 points maximum base score)
SECTION_WEIGHTS = {
    "personal_info": 15,
    "summary": 10,
    "experience": 35,
    "education": 15,
    "skills": 15,
    "projects": 10,
}

# Bonus Weight Cap for optional sections (e.g. social links, certifications)
MAX_BONUS_POINTS = 15


def _is_filled(value: Any) -> bool:
    """Helper to check if a value contains meaningful content."""
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) > 0
    return True


def calculate_completeness(portfolio_json: dict) -> int:
    """Analyzes structured portfolio dictionary and returns a completeness score (0 to 100).

    Args:
        portfolio_json (dict): Structured resume data (typically output from AI extraction).

    Returns:
        int: Completeness percentage integer between 0 and 100.

    Raises:
        TypeError: If portfolio_json is not a dictionary.
        ValueError: If portfolio_json is empty.
    """
    if not isinstance(portfolio_json, dict):
        raise TypeError("Input portfolio_json must be a dictionary.")

    if not portfolio_json:
        raise ValueError("Input portfolio_json is empty.")

    try:
        total_score = 0.0
        missing = []

        # 1. Personal Info (Max 15 pts)
        personal_info = portfolio_json.get("personal_info")
        if isinstance(personal_info, dict) and personal_info:
            p_score = 0.0
            if _is_filled(personal_info.get("name")):
                p_score += 5.0
            if _is_filled(personal_info.get("email")):
                p_score += 5.0
            if _is_filled(personal_info.get("phone")):
                p_score += 2.5
            if _is_filled(personal_info.get("location")) or _is_filled(personal_info.get("headline")):
                p_score += 2.5
            total_score += min(p_score, SECTION_WEIGHTS["personal_info"])
            if p_score < 15.0:
                missing.append("Complete Contact Info")
        elif _is_filled(portfolio_json.get("name")):
            # Fallback for flat schema if name exists at root
            total_score += 5.0
            missing.append("Contact Details")
        else:
            missing.append("Personal Info")

        # 2. Summary (Max 10 pts)
        summary = portfolio_json.get("summary")
        if _is_filled(summary) and isinstance(summary, str) and len(summary.strip()) >= 10:
            total_score += SECTION_WEIGHTS["summary"]
        else:
            missing.append("Professional Summary")

        # 3. Experience (Max 35 pts with Deduplication & Item Caps)
        experience = portfolio_json.get("experience")
        exp_score = 0.0
        if isinstance(experience, list) and experience:
            seen_experiences: Set[str] = set()

            for item in experience:
                if not isinstance(item, dict):
                    continue

                title = str(item.get("title", "")).strip().lower()
                company = str(item.get("company", "")).strip().lower()
                key = f"{title}|{company}"

                # Deduplication check
                if key in seen_experiences or key == "|":
                    continue
                seen_experiences.add(key)

                # Award points per valid job entry (15 pts per entry up to cap)
                entry_points = 10.0
                if _is_filled(item.get("description")):
                    entry_points += 5.0
                exp_score += entry_points

            total_score += min(exp_score, SECTION_WEIGHTS["experience"])

        # 4. Education (Max 15 pts with Deduplication & Item Caps)
        education = portfolio_json.get("education")
        if isinstance(education, list) and education:
            edu_score = 0.0
            seen_education: Set[str] = set()

            for item in education:
                if not isinstance(item, dict):
                    continue

                degree = str(item.get("degree", "")).strip().lower()
                institution = str(item.get("institution", "")).strip().lower()
                key = f"{degree}|{institution}"

                if key in seen_education or key == "|":
                    continue
                seen_education.add(key)

                edu_score += 15.0

            total_score += min(edu_score, SECTION_WEIGHTS["education"])
        else:
            missing.append("Education")

        # 5. Skills (Max 15 pts with Deduplication & Item Caps)
        skills = portfolio_json.get("skills")
        if isinstance(skills, list) and skills:
            skills_score = 0.0
            seen_skills: Set[str] = set()

            for skill in skills:
                if not _is_filled(skill):
                    continue
                skill_name = str(skill).strip().lower()
                if skill_name in seen_skills:
                    continue
                seen_skills.add(skill_name)
                skills_score += 3.0  # 5 skills fill the 15 pts cap

            total_score += min(skills_score, SECTION_WEIGHTS["skills"])
            if skills_score < 15.0:
                missing.append("More Skills (only a few listed)")
        else:
            missing.append("Skills")

        # 6. Projects (Max 10 pts with Deduplication & Item Caps)
        projects = portfolio_json.get("projects")
        proj_score = 0.0
        if isinstance(projects, list) and projects:
            seen_projects: Set[str] = set()

            for proj in projects:
                if not isinstance(proj, dict):
                    continue
                title = str(proj.get("title", "")).strip().lower()
                if not title or title in seen_projects:
                    continue
                seen_projects.add(title)
                proj_score += 5.0  # 2 projects fill the 10 pts cap

            proj_weight = SECTION_WEIGHTS["projects"]
            if exp_score == 0 and proj_score > 0:
                proj_weight += SECTION_WEIGHTS["experience"]
                
            total_score += min(proj_score, proj_weight)

        if exp_score == 0 and proj_score == 0:
            missing.append("Experience or Projects")
        elif exp_score == 0:
            missing.append("Work Experience")
        elif proj_score == 0:
            missing.append("Projects")

        # 7. Optional Bonus Fields (Max 15 pts bonus to compensate missing areas)
        bonus_score = 0.0

        # Social links / Web links
        social_links = portfolio_json.get("social_links")
        if isinstance(social_links, dict):
            if _is_filled(social_links.get("linkedin")):
                bonus_score += 4.0
            if _is_filled(social_links.get("github")):
                bonus_score += 4.0
            if _is_filled(social_links.get("website")):
                bonus_score += 2.0

        # Root level github / linkedin fallback
        if _is_filled(portfolio_json.get("github")) and not (isinstance(social_links, dict) and _is_filled(social_links.get("github"))):
            bonus_score += 4.0
        if _is_filled(portfolio_json.get("linkedin")) and not (isinstance(social_links, dict) and _is_filled(social_links.get("linkedin"))):
            bonus_score += 4.0

        # Achievements / Certifications
        if _is_filled(portfolio_json.get("certifications")):
            bonus_score += 3.0
            
        if _is_filled(portfolio_json.get("achievements")):
            bonus_score += 3.0

        total_score += min(bonus_score, MAX_BONUS_POINTS)

        # Enforce firm 0 to 100 range
        final_score = int(round(min(100.0, max(0.0, total_score))))
        return {"score": final_score, "missing": missing}

    except Exception:
        # Fail-safe crash prevention: return valid dict for unparseable / malformed JSON
        return {"score": 0, "missing": ["Could not calculate score due to malformed data"]}
