from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import *

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_blog = Blog(owner = user)
            user_blog.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_blog.save()
            user = authenticate(username=username, password = password)
            auth_login(request, user)
            return redirect('home:home')
    else:
        form = UserForm()
    context ={
        'form': form,
    }
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, form.get_user())
            next_url = request.GET.get('next')
            return redirect('home:home')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form, 
    }
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home:home')