from django.contrib import admin
from django.urls import include, path

from tareas import views as tareas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('cuentas/registro/', tareas_views.registro, name='register'),
    path('cuentas/perfil/', tareas_views.ver_perfil, name='ver_perfil'),
    path('', include('blog.urls')),
    path('tareas/', include('tareas.urls')),
]
