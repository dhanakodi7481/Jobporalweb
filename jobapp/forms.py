from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from .models import UserProfile

from .models import Job ,JobApplication

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus' : 'True','class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control',}),initial="password")


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus' : 'True','class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control',}),initial="password")
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))     
    usable_password = None

    class Meta:
        model = User
        fields = ["username","email" ,"password1","password2"]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'salary', 'location', 'category', 'company']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'phone', 'email', 'past_ctc', 'expected_ctc',
                  'experience', 'project_title', 'project_description', 'resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError('Please upload a PDF file.')
        return resume
    
class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = UserProfile
        fields = [
            'image', 'banner', 'address', 'current_company',
            'designation', 'interest', 'skills', 'phone', 'resume'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email

