from django.shortcuts import render, redirect
from .models import *
from accounts.models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return redirect('home:home')

def main(request, username):
    owner = User.objects.get(username=username)
    context = {
        'owner':owner,
    }
    return render(request, 'main.html', context)

@login_required
def create(request, username):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print('글 저장을 완료했습니다.')
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home:home')
    else:
        form = PostForm()
    
    context = {
        'form': form, 
    }
    print('글 저장에 실패했습니다.')
    return render(request, 'writepage.html', context)
