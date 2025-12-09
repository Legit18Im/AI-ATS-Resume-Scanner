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



# --- NEW LAYOUT ANALYSIS LOGIC ---
def analyze_layout(resume_text):
    """
    Analyzes the raw text of the resume for common ATS formatting issues.
    Returns a list of warnings/tips.
    """
    tips = []
    
    if not resume_text:
        return [" **Empty File:** We couldn't extract any text. Try uploading a text-based PDF or DOCX."]

    # Clean text for analysis
    clean_text = resume_text.strip()
    word_count = len(clean_text.split())

    # 1. LENGTH CHECK
    if word_count < 200:
        tips.append(" **Too Short:** Your resume is under 200 words. Add more detail to your experience.")
    elif word_count > 1000:
        tips.append(" **Too Long:** Your resume is over 1000 words. Try to keep it concise (1-2 pages max).")
    else:
        tips.append(" **Good Length:** Your word count is optimal for an ATS scan.")

    # 2. BULLET POINT CHECK
    # We look for common bullet characters (•, -, *, or similar unicode bullets)
    if not any(char in clean_text for char in ['•', '·', '-', '*']):
        tips.append(" **Use Bullet Points:** We didn't detect standard bullet points. Use them to list your achievements clearly.")

    # 3. CONTACT INFO CHECK
    if "@" not in clean_text:
        tips.append(" **Missing Email:** No email address was detected. Ensure it's clearly visible in the header.")

    # 4. CLICHÉ CHECK
    if "references available upon request" in clean_text.lower():
        tips.append(" **Remove References:** You don't need 'References available upon request'. Save that space for skills!")

    # 5. SECTION HEADERS
    common_sections = ['experience', 'education', 'skills', 'projects']
    missing_sections = [sec.title() for sec in common_sections if sec not in clean_text.lower()]
    
    if missing_sections:
        tips.append(f" **Missing Sections:** We couldn't find these standard headers: {', '.join(missing_sections)}. Ensure section titles are clear.")

    return tips