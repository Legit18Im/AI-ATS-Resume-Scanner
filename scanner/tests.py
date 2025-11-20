
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class ScannerTests(TestCase):
    def setUp(self):
        # 1. Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        
    def test_login_required_for_history(self):
        """Test that history page redirects if not logged in"""
        response = self.client.get('/history/')
        self.assertNotEqual(response.status_code, 200) # Should be 302 (Redirect)

    def test_scan_resume(self):
        """Test the core scanning functionality"""
        # Log in
        self.client.login(username='testuser', password='password123')

        # Create dummy files
        resume_content = b"Name: John Doe\nEmail: john@example.com\nSkills: Python, Django"
        resume_file = SimpleUploadedFile("test_resume.txt", resume_content, content_type="text/plain")
        
        jd_text = "We need a Python Developer with Django skills."

        # Post data to the home view
        response = self.client.post('/', {
            'resume': resume_file,
            'jd_text': jd_text
        })

        # Check if it worked (200 OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the context contains the score
        self.assertIn('ats_score', response.context)
        print("\n Test Scan Score:", response.context['ats_score']['score'])