# backend/scorer.py

def calculate_ats_score(match_results: dict, weights=None) -> dict:
    """
    Calculates the final ATS score based on the semantic match results.
    
    'match_results' is the dictionary from semantic_matcher.py:
    {
        "matched_skills": [...],
        "missing_skills": [...],
        "match_scores": { "jd_skill": {"score": 0.8} ... }
    }
    """
    
    if weights is None:
        # Define how much each component is worth.
        # This is easily tunable.
        weights = {
            "skill_match_ratio": 0.7,  # 70% of score is based on % of skills matched
            "avg_similarity": 0.3       # 30% is based on *how well* they matched
        }

    total_jd_skills = len(match_results["matched_skills"]) + len(match_results["missing_skills"])
    
    if total_jd_skills == 0:
        return {"score": 0, "skill_match_ratio": 0, "avg_similarity": 0}

    # 1. Calculate Skill Match Ratio (e.g., 4 out of 5 skills matched = 0.8)
    matched_skill_count = len(match_results["matched_skills"])
    skill_match_ratio = matched_skill_count / total_jd_skills
    
    # 2. Calculate Average Similarity Score
    total_similarity_score = 0
    num_scores = len(match_results["match_scores"])
    
    if num_scores > 0:
        for jd_skill, match_data in match_results["match_scores"].items():
            total_similarity_score += match_data["score"]
        avg_similarity = total_similarity_score / num_scores
    else:
        avg_similarity = 0 # No matches, so similarity is 0

    # 3. Calculate Final Weighted Score
    final_score = (skill_match_ratio * weights["skill_match_ratio"]) + \
                  (avg_similarity * weights["avg_similarity"])
                  
    # Return a dictionary with the final score and the components
    return {
        "score": round(final_score * 100, 2), # Convert to percentage
        "skill_match_ratio": round(skill_match_ratio * 100, 2),
        "avg_similarity": round(avg_similarity * 100, 2)
    }