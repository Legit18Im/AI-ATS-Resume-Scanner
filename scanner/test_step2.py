from skill_extractor import load_skill_taxonomy, extract_skills_from_text
from semantic_matcher import semantic_skill_match

resume_text = """
Experienced in Python, machine learning, pandas,
tensorflow, deep learning, SQL and cloud technologies.
"""

jd_skills = ["python", "sql", "spark", "deep learning", "mlops"]

taxonomy = load_skill_taxonomy()
resume_skills = extract_skills_from_text(resume_text, taxonomy)

print("\n=== Extracted Resume Skills ===")
print(resume_skills)

result = semantic_skill_match(resume_skills, jd_skills)

print("\n=== Semantic Matching ===")
print("Matched Skills:", result["matched"])
print("Missing Skills:", result["missing"])
print("Similarity Scores:", result["similarities"])
