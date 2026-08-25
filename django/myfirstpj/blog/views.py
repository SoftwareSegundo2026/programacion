from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Post


def getPosts(request):
    posts = Post.objects.filter(deleted_at__isnull=True)
    return render(request, 'post_list.html', {'posts': posts})


def verPost(request, post_id):
    post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)
    return render(request, 'post_detail.html', {'post': post})


@login_required
def deletePost(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)
        post.deleted_at = timezone.now()
        post.save()
        messages.success(request, 'Post eliminado.')
    return redirect('getPosts')


def deletedPosts(request):
    deleted_posts = Post.objects.filter(deleted_at__isnull=False).order_by('-deleted_at')
    return render(request, 'deleted_posts.html', {'posts': deleted_posts})


@login_required
def restorePost(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, deleted_at__isnull=False)
        post.deleted_at = None
        post.save()
        messages.success(request, 'Post restaurado.')
    return redirect('deletedPosts')


@login_required
def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post creado correctamente.')
            return redirect('getPosts')
    else:
        form = PostForm()

    return render(request, 'post_form.html', {'form': form})
