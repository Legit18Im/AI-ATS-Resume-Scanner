# backend/recommender.py

import os
from . import jd_processor
from . import semantic_matcher
from .skill_extractor import extract_skills_from_text, load_skill_taxonomy

# --- Missing Skill Recommendation ---

def get_missing_skills(match_results: dict) -> list:
    """
    A simple helper function to return the missing_skills list 
    from the match_results.
    """
    return match_results.get("missing_skills", [])


# --- Job Recommendation Engine ---

def load_sample_jds(jd_directory="D:\Team_Project\ATS Scanner\dataset\sample_jds"):
    """
    Loads all sample JDs from a directory and processes them
    to get their skill lists.
    
    Returns a dictionary like:
    { "ML Engineer.txt": ["python", "ml", "tensorflow"], ... }
    """
    jd_skill_database = {}
    if not os.path.exists(jd_directory):
        print(f"[Warning] Job directory not found: {jd_directory}. Job recommender will be empty.")
        return jd_skill_database

    skill_list_set = load_skill_taxonomy()

    for filename in os.listdir(jd_directory):
        file_path = os.path.join(jd_directory, filename)
        
        # We re-use the extractor from Step 1
        jd_text = jd_processor.extractor.extract_text(file_path)
        
        if jd_text:
            # We re-use the skill extractor from Step 2
            jd_skills = extract_skills_from_text(jd_text, skill_list_set)
            jd_skill_database[filename] = jd_skills
            
    return jd_skill_database


def recommend_jobs(resume_skills: list, jd_skill_database: dict, top_n=3) -> list:
    """
    Compares the resume's skills against all loaded JDs and
    returns the top N best matches.
    """
    recommendations = []

    if not resume_skills or not jd_skill_database:
        return []

    for job_title, jd_skills in jd_skill_database.items():
        
        # We re-use the semantic matcher from Step 2
        # We are matching the RESUME (as if it's the JD) vs. the JOB (as if it's the resume)
        # This checks "How many of the JOB's skills are in my resume?"
        
        # To get a better "fit" score, let's match the Resume TO the JD
        # "How many of the JD's skills are in my resume?"
        match_results = semantic_matcher.semantic_skill_match(resume_skills=resume_skills, jd_skills=jd_skills)
        
        # Use the same scorer from Step 3
        # This will give us a 0-100 score for *this* job
        from . import scorer 
        score_data = scorer.calculate_ats_score(match_results)
        
        recommendations.append({
            "job_title": job_title.replace('.txt', '').replace('.pdf', '').replace('.docx', ''),
            "match_score": score_data["score"]
        })

    # Sort by the highest score and return the top N
    sorted_recommendations = sorted(recommendations, key=lambda x: x["match_score"], reverse=True)
    
    return sorted_recommendations[:top_n]