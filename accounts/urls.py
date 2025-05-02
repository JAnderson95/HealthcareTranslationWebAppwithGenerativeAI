from django.urls import path
from django.contrib.auth import views as  auth_views
from . import views

app_name= 'accounts'

urlpatterns = [
    # Registration and authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    # User Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Password change (When user is authenticated)
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',success_url='/accounts/password-change/done/'),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
]