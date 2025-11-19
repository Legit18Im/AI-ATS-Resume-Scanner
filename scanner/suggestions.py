# backend/suggestions.py

import re

def generate_resume_suggestions(resume_text: str, basic_info: dict, extracted_skills: list) -> list:
    """
    Analyzes the resume text and extracted info to provide simple,
    rule-based improvement suggestions.
    """
    suggestions = []
    text_lower = resume_text.lower()

    # --- Basic Info Checks ---
    if not basic_info.get("email"):
        suggestions.append("Critical: Your resume is missing an email address.")
    
    if not basic_info.get("phone"):
        suggestions.append("Critical: Your resume is missing a phone number.")

    if not basic_info.get("name"):
        suggestions.append("Warning: Could not detect a name. Ensure your name is at the top.")

    # --- Section Checks ---
    if "skills" not in text_lower and not extracted_skills:
        suggestions.append("Recommendation: Add a dedicated 'Skills' section to improve ATS parsing.")
        
    if "experience" not in text_lower and "employment" not in text_lower:
        suggestions.append("Recommendation: Add a 'Work Experience' section with clear job titles and dates.")

    if "education" not in text_lower:
        suggestions.append("Recommendation: Add an 'Education' section detailing your degrees.")
        
    if "project" not in text_lower:
        suggestions.append("Tip: Consider adding a 'Projects' section to showcase your practical skills.")

    # --- Content Checks ---
    # Check for "action verbs" (a simple proxy for good bullet points)
    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'optimized']
    if not any(verb in text_lower for verb in action_verbs):
        suggestions.append("Tip: Improve your experience bullet points by starting them with action verbs (e.g., 'Developed', 'Managed', 'Led').")

    return suggestions