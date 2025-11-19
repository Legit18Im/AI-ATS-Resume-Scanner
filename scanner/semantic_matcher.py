# backend/semantic_matcher.py

from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load the SBERT model. This will download it the first time we run it.
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_skills(skills: list):
    """
    Convert a list of skill strings into numerical vectors (embeddings).
    """
    if not skills:
        return None
    # convert_to_tensor=True makes it faster for comparison
    return model.encode(skills, convert_to_tensor=True)


def semantic_skill_match(resume_skills: list, jd_skills: list, threshold=0.70):
    """
    Compares resume skills and JD skills using semantic similarity.
    
    Returns a dictionary containing:
    - matched skills
    - missing skills from the JD
    - similarity scores for matched items
    """
    if not resume_skills or not jd_skills:
        return {
            "matched_skills": [],
            "missing_skills": jd_skills,
            "match_scores": {}
        }

    # Generate embeddings for both lists
    resume_embeddings = embed_skills(resume_skills)
    jd_embeddings = embed_skills(jd_skills)

    # Compute cosine similarity between all pairs
    # This creates a matrix of [JD Skills x Resume Skills]
    cosine_scores = util.cos_sim(jd_embeddings, resume_embeddings).cpu().numpy()

    matched_skills = []
    missing_skills = []
    match_scores = {}

    # Find the best match for each JD skill
    for i, jd_skill in enumerate(jd_skills):
        best_resume_skill_index = np.argmax(cosine_scores[i])
        best_score = cosine_scores[i][best_resume_skill_index]

        if best_score >= threshold:
            best_matching_resume_skill = resume_skills[best_resume_skill_index]
            matched_skills.append(best_matching_resume_skill)
            match_scores[jd_skill] = {
                "matched_with": best_matching_resume_skill,
                "score": float(best_score)
            }
        else:
            missing_skills.append(jd_skill)

    return {
        "matched_skills": sorted(list(set(matched_skills))), # Unique list
        "missing_skills": sorted(missing_skills),
        "match_scores": match_scores
    }