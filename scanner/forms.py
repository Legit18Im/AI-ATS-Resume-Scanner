from django import forms
from .models import ResumeProfile

class ResumeBuilderForm(forms.ModelForm):
    class Meta:
        model = ResumeProfile
        fields = ['full_name', 'email', 'phone', 'summary', 'skills', 'experience', 'education']
        
        # Add Bootstrap styling to every input field
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 890'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Passionate AI Engineer...'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Python, Django, Machine Learning...'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Software Engineer at Google (2020-Present)...'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'B.Tech in CS, Mumbai University...'}),
        }