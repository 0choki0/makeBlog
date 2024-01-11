from django.shortcuts import render, redirect
from accounts.models import *
from main.models import *
from main.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts':posts,
    }
    return render(request, 'home.html', context)