# backend/jd_processor.py

from .skill_extractor import load_skill_taxonomy, extract_skills_from_text
from . import extractor  # We'll re-use the text extractor
import os

def process_jd_text(jd_text: str) -> list:
    """
    Takes raw JD text, loads the skill taxonomy,
    and returns a clean list of skills found in the JD.
    """
    # Load the master list of all possible skills
    skill_list_set = load_skill_taxonomy()
    
    # Extract skills from the JD text
    jd_skills = extract_skills_from_text(jd_text, skill_list_set)
    
    return sorted(list(set(jd_skills)))

def process_jd_file(file_path: str) -> list:
    """
    Takes a file path (.txt, .pdf, .docx) to a JD,
    extracts the text, and returns its skill list.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] Job description file not found at: {file_path}")
        return []
        
    jd_text = extractor.extract_text(file_path)
    
    if not jd_text:
        print(f"[ERROR] Could not extract text from JD file: {file_path}")
        return []
        
    return process_jd_text(jd_text)