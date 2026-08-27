from django.conf import settings
from django.db import migrations, models


def assign_tareas_to_first_user(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Tarea = apps.get_model('tareas', 'Tarea')
    user = User.objects.first()
    if user:
        Tarea.objects.filter(user__isnull=True).update(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0003_tarea_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(assign_tareas_to_first_user, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tarea',
            name='user',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='tareas', to=settings.AUTH_USER_MODEL),
        ),
    ]
