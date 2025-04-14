from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Job,JobApplication
from .forms import JobForm,JobApplicationForm
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import UserProfileForm

from . forms import CustomerRegistrationForm
# Create your views here.
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation! User Registered Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'customerregistration.html',locals())

def home(request):     
    return render(request,"home.html",locals())

def job_list(request):
    jobs = Job.objects.all()
    location = request.GET.get('location')
    category = request.GET.get('category')
    company = request.GET.get('company')

    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__icontains=category)
    if company:
        jobs = jobs.filter(company__icontains=company)

    return render(request, 'job_list.html', {'jobs': jobs})

def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import JobApplication, Job
from .forms import JobApplicationForm
from django.contrib.auth.models import User

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    application_count = JobApplication.objects.filter(job=job).count()

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)

            # If the user is authenticated, use request.user
            if request.user.is_authenticated:
                user = request.user
            else:
                # Optional: Create or fetch a "Guest" user if not logged in
                user = User.objects.get_or_create(username="Guest")[0]
                request.session['guest_user'] = user.id  # Store guest user ID in session

            application.user = user  # Assign the user to the application
            application.job = job  # Assign the job to the application
            application.save()

            # Debugging: Confirm if redirect happens
            print(f"Redirecting to user_dashboard for user: {user}")

            return redirect(reverse('user_dashboard'))  # Redirect to the dashboard after applying

    else:
        form = JobApplicationForm()

    return render(request, 'apply_job.html', {
        'form': form,
        'job': job,
        'application_count': application_count
    })


def user_dashboard(request):
    # Check if there's a logged-in user
    user = request.user

    # If user is authenticated, get their applications
    if user.is_authenticated:
        applications = JobApplication.objects.filter(user=user)
    else:
        applications = JobApplication.objects.none()  # No applications for anonymous users

    # Render the dashboard template with the applications data
    return render(request, 'user_dashboard.html', {'applications': applications})

def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile, 'user': request.user})


def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def delete_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.delete()
        return redirect('user_profile')  # or logout user, or redirect somewhere else
    return render(request, 'confirm_delete.html')