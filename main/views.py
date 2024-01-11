from django.shortcuts import render, redirect
from .models import *
from accounts.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return redirect('home:home')

def main(request, username):
    owner = User.objects.get(username=username)
    postlist = Post.objects.filter(user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    post = sorted_posts.first()
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = list(set(category.name for category in categories))
    context = {
        'owner':owner,
        'postlist':postlist,
        'sorted_posts':sorted_posts,
        'categoryList':categoryList,
        'post':post,
    }
    return render(request, 'main.html', context)

@login_required
def create(request, username):
    owner = User.objects.get(username=username)
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = list(set(category.name for category in categories))

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:detail', username=username, number=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'categoryList': categoryList,
    }
    return render(request, 'writepage.html', context)

def detail(request, username, number):
    owner = User.objects.get(username=username)
    postlist = Post.objects.filter(user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    post = postlist.get(id=number)
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = list(set(category.name for category in categories))
    context = {
        'owner':owner,
        'postlist':postlist,
        'sorted_posts':sorted_posts,
        'post':post,
        'categoryList':categoryList
    }
    return render(request, 'detail.html', context)

@login_required
def delete(request, username, number):
    post = Post.objects.get(id=number)
    if request.user == post.user:
        post.delete()

    return redirect('main:main', username=username)

@login_required
def update(request, username, number):
    post = Post.objects.get(id=number)
    if request.user != post.user:
        return redirect('main:detail', username=username, number=number)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:detail', username=username, number=number)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'writepage.html', context)

@login_required
def category(request, username):
    owner = User.objects.get(username=username)
    if request.user == owner:
        categories = Category.objects.filter(owner_id=owner.id).order_by('name')
        standard = categories.first()
        if not categories:
            Category.objects.create(name='기본 카테고리' ,owner=owner)
        context = {
            'owner':owner,
            'categories':categories,
            'standard':standard,
        }
        return render(request, 'category/category.html', context)
    else:
        return redirect('main:main', username=username)

@login_required
def Create_category(request, username):
    owner = User.objects.get(username=username)
    category_name = request.POST['categoryName']
    new_categories = Category(name=category_name, owner_id=owner.id)
    new_categories.save()
    categories = Category.objects.filter(owner_id=owner.id).order_by('name')
    context = {
        'owner':owner,
        'categories':categories,
        }
    return render(request, 'category/setting.html', context)

@login_required
def Delete_category(request, username):
    category_id = request.POST['categoryId']    
    delete_category = Category.objects.get(id = category_id)
    delete_category.delete()
    return redirect('main:category', username=username)