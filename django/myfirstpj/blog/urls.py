from django.urls import path
from . import views
from .urls_crud import urlpatterns as crud_urlpatterns

urlpatterns = [
    path('', views.getPosts, name='getPosts'),
    path('create/', views.createPost, name='createPost'),
] + crud_urlpatterns