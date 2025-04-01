from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')    
    else:
        form = CustomUserCreationForm()
        
    context = {
        'form':form, 
        
    }
    return render(request, 'signup.html', context)

def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')
            
    else:
        form = CustomAuthenticationForm()
        
    context = {
        'form':form,
        
    }
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('posts:index')

def profile(request, username):
    user_profile = user = User.objects.get(username=username)
    
    context = {
        'user_profile' : user_profile, 
    }
    
    return render(request, 'profile.html', context)