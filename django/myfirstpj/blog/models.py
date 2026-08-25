from django.db import models


class Post(models.Model):
    CATEGORIAS = [
        ('sistemas', 'Sistemas'),
        ('analisis', 'Analisis'),
        ('engineering', 'Engineering'),
        ('economia', 'Economia'),
        ('other', 'Otro'),
    ]

    objects = models.Manager()

    title = models.CharField(max_length=200)
    content = models.TextField()
    imagen = models.ImageField(
        upload_to='blog/imagenes/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Imagen',
        help_text='Opcional — imagen de portada para el post.',
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='other',
        blank=True,
        verbose_name='Categoria',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_deleted(self):
        return self.deleted_at is not None
