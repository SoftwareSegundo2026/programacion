from django.urls import path
from . import views

urlpatterns = [
    path('', views.getPosts, name='getPosts'),
    path('create/', views.createPost, name='createPost'),
    path('delete/<int:post_id>/', views.deletePost, name='deletePost'),
    path('deleted/', views.deletedPosts, name='deletedPosts'),
    path('restore/<int:post_id>/', views.restorePost, name='restorePost'),
]