from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth.decorators import login_required
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
@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')

def profile(request, username):
    user_profile = user = User.objects.get(username=username)
    
    context = {
        'user_profile' : user_profile, 
    }
    
    return render(request, 'profile.html', context)
@login_required
def follow(request, username):
    me = request.user # 로그인한사람
    you = User.objects.get(username=username) # 내가 들어간 페이지의 유저
    
    if me == you: # 내가 내 페이지 들어간 경우
        return redirect('accounts:profile', username)
    # if you in me.followings.all(): 
    if me in you.followers.all():
        you.followers.remove(me)
        # me.followings.remove(you)
    else:
        you.followers.add(me)
        # me.followings.add(you)
        
    return redirect('accounts:profile', username)