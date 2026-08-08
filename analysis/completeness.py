def calculate_completeness(portfolio_json):
    """
    Analyzes the parsed JSON and returns a dict with:
      - 'score': completeness score from 0 to 100
      - 'missing': list of missing section names
    """
    if not isinstance(portfolio_json, dict):
        return {"score": 0, "missing": ["Everything — no data found"]}
        
    try:
        score = 0
        missing = []
        
        # Summary (10 points)
        summary = portfolio_json.get('summary', '')
        if isinstance(summary, str) and len(summary.strip()) > 10:
            score += 10
        else:
            missing.append("Professional Summary")
            
        # Education (20 points)
        education = portfolio_json.get('education', [])
        if isinstance(education, list) and len(education) > 0:
            score += 20
        else:
            missing.append("Education")
            
        # Experience (15 points per unique experience)
        experience = portfolio_json.get('experience', [])
        exp_score = 0
        seen_exp = set()
        if isinstance(experience, list):
            for exp in experience:
                if isinstance(exp, dict):
                    title = str(exp.get('title', '')).strip().lower()
                    company = str(exp.get('company', '')).strip().lower()
                    if title or company:
                        exp_hash = f"{title}-{company}"
                        if exp_hash not in seen_exp:
                            seen_exp.add(exp_hash)
                            exp_score += 15
        
        # Projects (10 points per unique project)
        projects = portfolio_json.get('projects', [])
        proj_score = 0
        seen_proj = set()
        if isinstance(projects, list):
            for proj in projects:
                if isinstance(proj, dict):
                    title = str(proj.get('title', '')).strip().lower()
                    if title and title not in seen_proj:
                        seen_proj.add(title)
                        proj_score += 10

        if exp_score == 0 and proj_score == 0:
            missing.append("Experience or Projects")
        elif exp_score == 0:
            missing.append("Work Experience")
        elif proj_score == 0:
            missing.append("Projects")
            
        # Combined Cap: 60 points
        score += min(exp_score + proj_score, 60)
        
        # Skills (10 points)
        skills = portfolio_json.get('skills', [])
        if isinstance(skills, list) and len(skills) >= 3:
            score += 10
        elif isinstance(skills, list) and len(skills) > 0:
            score += 5
            missing.append("More Skills (only a few listed)")
        else:
            missing.append("Skills")
        
        # Optionals / Bonuses
        socials = portfolio_json.get('social_links', {})
        if isinstance(socials, dict):
            if socials.get('linkedin'):
                score += 5
            else:
                missing.append("LinkedIn Profile")
            if socials.get('github'):
                score += 5
            else:
                missing.append("GitHub Profile")
            if not socials.get('website'):
                missing.append("Personal Website")
                
        certs = portfolio_json.get('certifications', [])
        if isinstance(certs, list) and len(certs) > 0:
            score += 5
        else:
            missing.append("Certifications")

        # Final cap
        return {"score": min(score, 100), "missing": missing}
        
    except Exception as e:
        print(f"Error calculating completeness: {e}")
        return {"score": 0, "missing": ["Error analyzing resume"]}
