from django.shortcuts import render, redirect
from .models import *
from accounts.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

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
    if not categories:
        Category.objects.create(name='기본 카테고리' ,owner=owner)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.category_id = request.POST.get('category')
            post.save()
            return redirect('main:detail', username=username, number=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'categories': categories,
        'owner':owner,
    }
    return render(request, 'writepage.html', context)

def detail(request, username, number):
    owner = User.objects.get(username=username)
    postlist = Post.objects.filter(user_id=owner.id)
    sorted_posts = postlist.all().order_by('-created_at')
    post = postlist.get(id=number)
    categories = Category.objects.filter(owner_id=owner.id)
    categoryList = list(set(category.name for category in categories))
    comment_form = CommentForm()
    reply_form = ReplyForm()
    context = {
        'owner':owner,
        'postlist':postlist,
        'sorted_posts':sorted_posts,
        'post':post,
        'categoryList':categoryList,
        'comment_form':comment_form,
        'reply_form':reply_form,
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
    owner = User.objects.get(username=username)
    categories = Category.objects.filter(owner_id=owner.id)
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
        'categories': categories,
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

@login_required
def likes_async(request, owner, number):
    user = request.user
    post = Post.objects.get(id=number)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False

    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(post.like_users.all()),
        'owner': owner,
    }
    return JsonResponse(context)

@login_required
def comment_create(request, owner, number):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = number
        comment.save()
    context = {
        'id': comment.id,
        'postId': number,
        'username': comment.user.username,
        'content': comment.content,
        'owner': owner,
    }

    return JsonResponse(context)


@login_required
def comment_update(request, owner, number, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.user != comment.user:
        return redirect('main:detail', owner=owner, number=number, comment_id=comment_id)
    
    if request.method == 'POST':
        comment.content = request.POST.get('comment_content')
        comment.save()
        data = {
        'comment_id': comment_id,
        'post_id': owner,
        'number': number,
    }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


@login_required
def comment_delete(request, owner, number, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.user != comment.user:
        return redirect('main:detail', owner=owner, number=number, comment_id=comment_id)
    
    else:
        comment.delete()
        data = {
            'owner':owner,
            'post_id': number,
            'comment_id' : comment_id,
        }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')

@login_required
def comment_likes_async(request, owner, number, comment_id):
    user = request.user
    post = Post.objects.get(id=number)
    comment = Comment.objects.get(id=comment_id)

    if user in comment.like_users.all():
        comment.like_users.remove(user)
        status = False

    else:
        comment.like_users.add(user)
        status = True

    context = {
        'owner': owner,
        'status': status,
        'count': len(comment.like_users.all()),
        'number': post.id,
        'comment_id': comment.id,
    }
    return JsonResponse(context)

@login_required
def reply_create(request, owner, number, comment_id):
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.post_id = number
        reply.user = request.user
        reply.comment_id = comment_id
        reply.save()
    context = {
        'owner': owner,
        'id': reply.id,
        'postId': number,
        'commentId': comment_id,
        'username': reply.user.username,
        'content': reply.content,
        }

    return JsonResponse(context)


@login_required
def reply_delete(request, owner, number, comment_id, reply_id):
    reply = Reply.objects.get(id=reply_id)

    if request.user != reply.user:
        return redirect('main:home', owner=owner, number=number, comment_id=comment_id, reply_id=reply_id)
    
    else:
        reply.delete()
        data = {
            'reply_id': reply_id,
            'post_id': number,
            'comment_id' : comment_id,
        }
    
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


@login_required
def reply_update(request, owner, number, comment_id, reply_id):
    reply = Reply.objects.get(id=reply_id)

    if request.user != reply.user:
        return redirect('posts:home')

    if request.method == 'POST':
        reply.content = request.POST.get('reply_content')
        reply.save()
        data = {
        'reply_id': id,
        'post_id': number,
        'comment_id' : comment_id,
    }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')
    