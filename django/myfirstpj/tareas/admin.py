from django.contrib import admin

from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'prioridad', 'completada']
    list_filter = ['completada', 'prioridad']
    search_fields = ['nombre']
