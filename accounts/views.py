from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm

# Create your views here.
def register_view(request):
    if request.method =='POST':
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request, 'Registration Succeed')
            return redirect('home')
    else:
        form= CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome{username}')
                return redirect('home')
        messages.error(request,'User or password not valid')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

