from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Post

# Create your views here.

def getPosts(request):
    posts = Post.objects.filter(deleted_at__isnull=True)
    return render(request, 'post_list.html', {'posts': posts})


def deletePost(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)
        post.deleted_at = timezone.now()
        post.save()
    return redirect('getPosts')


def deletedPosts(request):
    deleted_posts = Post.objects.filter(deleted_at__isnull=False).order_by('-deleted_at')
    return render(request, 'deleted_posts.html', {'posts': deleted_posts})


def restorePost(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, deleted_at__isnull=False)
        post.deleted_at = None
        post.save()
    return redirect('deletedPosts')


def createPost(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            Post.objects.create(title=title, content=content)
            return redirect('getPosts')

        return render(request, 'post_form.html', {
            'error': 'El título y el contenido son obligatorios.',
            'title': title,
            'content': content,
        })

    return render(request, 'post_form.html')