from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'IT'),
         ('BP0', 'BPO'),
        ('HR', 'HR'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('General', 'General'),
        
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='General')
    company = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobApplication(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allow NULL for user
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    past_ctc = models.CharField(max_length=100)
    expected_ctc = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    project_title = models.CharField(max_length=255)
    project_description = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    banner = models.ImageField(upload_to='profile_banners/', null=True, blank=True)
    address = models.TextField(blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    interest = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='user_cvs/', null=True, blank=True)

    def __str__(self):
        return self.user.username
