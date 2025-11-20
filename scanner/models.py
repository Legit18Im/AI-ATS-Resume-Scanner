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