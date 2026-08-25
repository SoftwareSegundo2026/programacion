from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>/', views.verPost, name='verPost'),
    path('delete/<int:post_id>/', views.deletePost, name='deletePost'),
    path('deleted/', views.deletedPosts, name='deletedPosts'),
    path('restore/<int:post_id>/', views.restorePost, name='restorePost'),
]