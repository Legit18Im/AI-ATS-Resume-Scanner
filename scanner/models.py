from django.db import models
from django.contrib.auth.models import User  # <--- We import the User model

class ScanHistory(models.Model):
    # Link every scan to a User. 'null=True' means old scans won't break.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    candidate_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    resume_filename = models.CharField(max_length=200)
    ats_score = models.FloatField()
    
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    scan_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.ats_score}%"
    



class ResumeProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField(help_text="A brief professional summary")
    skills = models.TextField(help_text="Comma-separated list (e.g. Python, Django, SQL)")
    experience = models.TextField(help_text="Paste your work experience here")
    education = models.TextField(help_text="Paste your education details here")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}'s Profile"