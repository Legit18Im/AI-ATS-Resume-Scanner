from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Import our AI modules
from . import extractor, parser, skill_extractor, jd_processor, semantic_matcher, scorer, suggestions, recommender

# 1. IMPORT THE DATABASE MODEL
from .models import ScanHistory

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
            # 3. Run the AI Pipeline
            resume_content = extractor.extract_text(uploaded_file_url)
            basic_info = parser.parse_basic_info(resume_content)
            resume_skills = skill_extractor.extract_skills_from_text(resume_content, SKILL_LIST)
            jd_data = jd_processor.process_jd_text(jd_text)
            
            match_results = semantic_matcher.semantic_skill_match(resume_skills, jd_data)
            ats_score = scorer.calculate_ats_score(match_results)
            tips = suggestions.generate_resume_suggestions(resume_content, basic_info, resume_skills)
            jobs = recommender.recommend_jobs(resume_skills, JD_DATABASE)

            # ---------------------------------------------------------
            # 4. NEW: SAVE SCAN TO DATABASE
            # ---------------------------------------------------------
            ScanHistory.objects.create(
                candidate_name=basic_info.get('name') or "Unknown Candidate",
                email=basic_info.get('email') or "No Email",
                resume_filename=resume_file.name,
                ats_score=ats_score.get('score', 0),
                matched_skills=match_results.get('matched_skills', []),
                missing_skills=match_results.get('missing_skills', []),
                user=request.user if request.user.is_authenticated else None,
            )
            # ---------------------------------------------------------

            # 5. Pack data to send to HTML
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

# ---------------------------------------------------------
# 2. NEW: HISTORY VIEW FUNCTION
# ---------------------------------------------------------
@login_required(login_url='/login/')
def history(request):
    # Only show scans belonging to the current user
    scans = ScanHistory.objects.filter(user=request.user).order_by('-scan_date')
    return render(request, 'scanner/history.html', {'scans': scans})

def view_scan(request, pk):
    # 1. Fetch the specific scan from DB or 404
    scan = get_object_or_404(ScanHistory, pk=pk)

    # 2. PRO FEATURE: Re-generate Job Recommendations dynamically!
    # Since we saved the 'matched_skills', we can run them against the DB again.
    # We combine matched + missing to get the full list of skills the resume had (roughly)
    # OR just use matched_skills if that's what we stored. 
    # Let's use matched_skills for safe recommendations.
    suggested_jobs = recommender.recommend_jobs(scan.matched_skills, JD_DATABASE)

    context = {
        'scan': scan,
        'jobs': suggested_jobs
    }
    return render(request, 'scanner/scan_detail.html', context)


def download_report(request, pk):
    # 1. Fetch data (same as view_scan)
    scan = get_object_or_404(ScanHistory, pk=pk)
    suggested_jobs = recommender.recommend_jobs(scan.matched_skills, JD_DATABASE)

    # 2. Load the special PDF template
    template_path = 'scanner/pdf_report.html'
    context = {'scan': scan, 'jobs': suggested_jobs}

    # 3. Render PDF
    response = HttpResponse(content_type='application/pdf')
    # Set filename to include candidate name
    filename = f"Report_{scan.candidate_name.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



# --- AUTHENTICATION VIEWS ---

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in immediately
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'scanner/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'scanner/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'scanner/about.html')