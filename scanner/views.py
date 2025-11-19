
# Create  views here.
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Import your AI modules
from . import extractor, parser, skill_extractor, jd_processor, semantic_matcher, scorer, suggestions, recommender

# Load data once when the server starts
SKILL_LIST = skill_extractor.load_skill_taxonomy()
JD_PATH = os.path.join(settings.BASE_DIR, 'dataset', 'sample_jds')
JD_DATABASE = recommender.load_sample_jds(JD_PATH)

def home(request):
    context = {}
    
    if request.method == 'POST' and request.FILES.get('resume'):
        # 1. Get the file and JD text
        resume_file = request.FILES['resume']
        jd_text = request.POST.get('jd_text', '')

        # 2. Save file temporarily so we can read it
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        uploaded_file_url = fs.path(filename)

        try:
            # 3. Run the AI Pipeline (Same logic as your old app.py)
            resume_content = extractor.extract_text(uploaded_file_url)
            basic_info = parser.parse_basic_info(resume_content)
            resume_skills = skill_extractor.extract_skills_from_text(resume_content, SKILL_LIST)
            jd_data = jd_processor.process_jd_text(jd_text)
            
            match_results = semantic_matcher.semantic_skill_match(resume_skills, jd_data)
            ats_score = scorer.calculate_ats_score(match_results)
            tips = suggestions.generate_resume_suggestions(resume_content, basic_info, resume_skills)
            jobs = recommender.recommend_jobs(resume_skills, JD_DATABASE)

            # 4. Pack data to send to HTML
            context = {
                'result': True,
                'basic_info': basic_info,
                'ats_score': ats_score,
                'matched_skills': match_results['matched_skills'],
                'missing_skills': match_results['missing_skills'],
                'tips': tips,
                'jobs': jobs
            }

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Cleanup: delete the temp file
            if os.path.exists(uploaded_file_url):
                os.remove(uploaded_file_url)

    return render(request, 'scanner/index.html', context)