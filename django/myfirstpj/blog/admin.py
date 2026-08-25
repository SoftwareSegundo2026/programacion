from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


class EstadoFilter(admin.SimpleListFilter):
    title = _('estado')
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
        return (
            ('activo', _('Activo')),
            ('eliminado', _('Eliminado')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'activo':
            return queryset.filter(deleted_at__isnull=True)
        if self.value() == 'eliminado':
            return queryset.filter(deleted_at__isnull=False)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'es_eliminado_display']
    list_filter = [EstadoFilter]
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    actions = ['restore_selected_posts']

    @admin.display(boolean=True, description=_('Estado'))
    def es_eliminado_display(self, obj):
        return obj.is_deleted

    @admin.action(description='Restaurar posts eliminados seleccionados')
    def restore_selected_posts(self, request, queryset):
        restored = queryset.filter(deleted_at__isnull=False).update(deleted_at=None)
        self.message_user(request, f'Se restauraron {restored} posts.')
