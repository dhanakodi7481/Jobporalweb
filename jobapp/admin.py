from django.contrib import admin
from .models import Job,JobApplication,UserProfile

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'category', 'posted_at')
    search_fields = ('title', 'company', 'location')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job', 'email', 'applied_at')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'current_company', 'designation')
    search_fields = ('user__username', 'current_company')

