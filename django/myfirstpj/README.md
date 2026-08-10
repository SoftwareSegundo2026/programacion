# Proyecto Django "Mi Blog"

Este proyecto es una aplicación de blog mínima construida con Django. Permite crear, listar, eliminar y recuperar posts usando un soft delete.

## Estructura del proyecto

- `django/myfirstpj/myfirstpj/`
  - `settings.py`: configuración principal de Django.
  - `urls.py`: ruteo global del proyecto.
- `django/myfirstpj/blog/`
  - `models.py`: modelo `Post` con soft delete (`deleted_at`).
  - `views.py`: vistas para listar, crear, eliminar, listar eliminados y restaurar posts.
  - `urls.py`: rutas de la aplicación de blog.
  - `templates/`: plantillas HTML para las diferentes vistas.
  - `tests.py`: pruebas de "camino feliz" para las operaciones principales.

## Qué realiza cada sección

### `models.py`
- Define el modelo `Post` con campos `title`, `content`, `created_at`, `updated_at` y `deleted_at`.
- `deleted_at` se usa para marcar un post como eliminado sin borrarlo físicamente.
- Incluye la propiedad `is_deleted` para consultar el estado de eliminación.

### `views.py`
- `getPosts`: devuelve los posts activos (no eliminados).
- `createPost`: maneja creación mediante POST y renderiza el formulario en GET.
- `deletePost`: marca un post como eliminado poniendo `deleted_at`.
- `deletedPosts`: lista los posts eliminados.
- `restorePost`: restaura un post eliminado limpiando `deleted_at`.

### `urls.py` (app)
- `''`: lista posts activos.
- `create/`: formulario de creación de posts.
- `delete/<int:post_id>/`: soft delete de un post.
- `deleted/`: lista posts eliminados.
- `restore/<int:post_id>/`: restauración de post eliminado.

### `templates/`
- `base.html`: layout global con navbar y Tailwind CSS.
- `post_list.html`: listado de posts activos con botones para eliminar y ver eliminados.
- `post_form.html`: formulario de creación de posts.
- `deleted_posts.html`: vista para recuperar posts eliminados.

### `tests.py`
- Contiene pruebas de camino feliz para:
  - mostrar posts listados
  - crear un post
  - eliminar un post con soft delete
  - ver la lista de posts eliminados
  - restaurar un post eliminado

## Cómo correr el proyecto

1. Navegar a la carpeta del proyecto:

```bash
cd /home/dcazabat/Documentos/clases/programacion/Material-Clase/django/myfirstpj
```

2. Instalar dependencias de Django (si no están instaladas):

```bash
python -m pip install django
```

3. Ejecutar migraciones:

```bash
python manage.py migrate
```

4. Correr el servidor:

```bash
python manage.py runserver
```

5. Abrir `http://127.0.0.1:8000/` en el navegador.

## Cómo ejecutar los tests

```bash
python manage.py test blog
```

## Notas

- Tailwind CSS se incluye vía CDN para simplificar el setup.
- El soft delete permite recuperar posts eliminados desde la vista `deleted/`.
