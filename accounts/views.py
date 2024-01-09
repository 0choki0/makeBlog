from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = password)
            login(request, user)
            return redirect('home:home')
    else:
        form = UserForm()
    context ={
        'form': form,
    }
    return render(request, 'signup.html', context)