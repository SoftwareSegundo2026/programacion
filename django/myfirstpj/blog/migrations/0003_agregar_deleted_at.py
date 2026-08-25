from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_quitar_deleted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
