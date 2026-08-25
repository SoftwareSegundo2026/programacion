from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0003_agregar_deleted_at'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DELETE FROM django_migrations WHERE app='blog';",
            reverse_sql="INSERT INTO django_migrations (app, name, applied) VALUES "
                       "('blog', '0001_initial', CURRENT_TIMESTAMP), "
                       "('blog', '0002_quitar_deleted_at', CURRENT_TIMESTAMP), "
                       "('blog', '0003_agregar_deleted_at', CURRENT_TIMESTAMP);"
        ),
    ]
