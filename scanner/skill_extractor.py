# ats_web/scanner/skill_extractor.py


import re
import csv
import os
from django.conf import settings

def load_skill_taxonomy():
    # Dynamically find the file inside the 'dataset' folder
    path = os.path.join(settings.BASE_DIR, 'dataset', 'skill_taxonomy.csv')
    
    skills_set = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    skills_set.add(row[0].strip().lower())
    except FileNotFoundError:
        print(f"[ERROR] Skill taxonomy not found at: {path}")
    return skills_set


def extract_skills_from_text(text: str, skill_list: set) -> list:
    """
    Extract skills from the resume text based on the skill_list.
    This uses regex to find whole word matches.
    """
    found_skills = set()
    text_lower = text.lower()

    for skill in skill_list:
        # Create a regex pattern to match the skill as a whole word
        # This prevents "java" from matching "javascript"
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(list(found_skills))