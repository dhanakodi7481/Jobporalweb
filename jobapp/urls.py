from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from jobapp.forms import LoginForm
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ Root path redirects to home view
    path('', views.home, name='home'),

    # Auth views
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('account/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    # Optional: Keep '/home/' too if needed
    path('home/', views.home, name='home'),
    path('job_list/', views.job_list, name='job_list'),
    path('post_job/', views.post_job, name='post_job'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)