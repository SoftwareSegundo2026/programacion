# FastAPI Chinook API

API REST construida con **FastAPI** que expone la base de datos **Chinook** (tienda de música digital) a través de endpoints CRUD protegidos con autenticación **JWT**.

Este proyecto es un ejemplo didáctico para aprender FastAPI con Python, pensado para alumnos de programación.

---

## ¿Qué incluye?

- **CRUD completo** de Artistas, Álbumes, Géneros y Tracks (crear, leer, actualizar, eliminar)
- **Autenticación JWT** con dos roles: `admin` y `reader` (usuario deshabilitado)
- **Gestión de usuarios**: crear, activar/desactivar, cambiar/resetear contraseña, eliminar
- **Activity Logging**: registro automático de cada operación (auditoría)
- **Imágenes**: subida manual, búsqueda automática en Wikipedia, placeholders SVG por defecto
- **Paginación** en todos los listados
- **Documentación interactiva** vía Swagger UI

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy 2.0 (async) |
| Base de datos | SQLite + aiosqlite (Chinook) |
| Autenticación | JWT (python-jose) + bcrypt (passlib) |
| Validación | Pydantic v2 |
| Servidor ASGI | Uvicorn |
| Paquetería | uv |

---

## Puesta en marcha

### 1. Requisitos

- Python ≥ 3.11
- uv (gestor de paquetes y entornos virtuales)

### 2. Clonar e instalar

```bash
git clone <repo>
cd fastAPI-example
uv sync
```

### 3. Configurar `.env`

Copiar `.env.example` a `.env` y ajustar si es necesario:

```env
DATABASE_URL=sqlite+aiosqlite:///./instance/Chinook.db
SECRET_KEY=change-this-secret-key-for-jwt-development
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
LOG_FILE_PATH=./instance/fastapi-example.log
LOG_LEVEL=INFO
UPLOAD_DIR=./static/images
```

### 4. Iniciar el servidor

```bash
uv run uvicorn main:app --reload
```

Esto inicia el servidor en `http://localhost:8000` con recarga automática ante cambios.

### 5. Abrir la documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Usuarios demo

Al iniciar el servidor se crean automáticamente:

| Usuario | Password | ¿Es admin? | ¿Está activo? |
|---|---|---|---|
| `admin` | `admin123` | Sí | Sí |
| `reader` | `reader123` | No | No (deshabilitado) |

Para probar, primero obtené un token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Respuesta:

```json
{"access_token": "eyJ...", "token_type": "bearer"}
```

Luego usá ese token en el header `Authorization: Bearer eyJ...` para los endpoints protegidos.

---

## Endpoints principales

### Públicos (no requieren token)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Health check |
| GET | `/artists` | Listar artistas (paginado) |
| GET | `/artists/{id}` | Obtener artista |
| GET | `/artists/{id}/image` | Obtener imagen del artista |
| GET | `/albums` | Listar álbumes (paginado) |
| GET | `/albums/{id}` | Obtener álbum |
| GET | `/albums/{id}/image` | Obtener imagen del álbum |
| GET | `/genres` | Listar géneros |
| GET | `/genres/{id}` | Obtener género |
| GET | `/tracks` | Listar tracks |
| GET | `/tracks/{id}` | Obtener track |
| GET | `/activities` | Listar actividad (auditoría) |

### Protegidos (requieren token, cualquier usuario activo)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/artists` | Crear artista |
| PATCH | `/artists/{id}` | Actualizar artista |
| DELETE | `/artists/{id}` | Eliminar artista |
| POST | `/artists/{id}/image` | Subir imagen |
| POST | `/artists/{id}/fetch-image` | Buscar imagen en Wikipedia |
| POST | `/albums` | Crear álbum |
| PATCH | `/albums/{id}` | Actualizar álbum |
| DELETE | `/albums/{id}` | Eliminar álbum |
| POST | `/albums/{id}/image` | Subir imagen |
| POST | `/albums/{id}/fetch-image` | Buscar imagen en Wikipedia |
| POST | `/genres` | Crear género |
| PATCH | `/genres/{id}` | Actualizar género |
| DELETE | `/genres/{id}` | Eliminar género |
| POST | `/tracks` | Crear track |
| PATCH | `/tracks/{id}` | Actualizar track |
| DELETE | `/tracks/{id}` | Eliminar track |
| GET | `/users/me` | Ver perfil propio |
| PATCH | `/users/me` | Actualizar perfil propio |
| PATCH | `/users/me/password` | Cambiar propia contraseña |

### Solo admin

| Método | Ruta | Descripción |
|---|---|---|
| PATCH | `/users/{id}` | Activar/desactivar usuario |
| PATCH | `/users/{id}/password` | Resetear contraseña de otro usuario |
| DELETE | `/users/{id}` | Eliminar usuario |

---

## Estructura del proyecto

```
fastAPI-example/
├── main.py                    # Punto de entrada del servidor
├── app/
│   ├── main.py                # Configuración de la app FastAPI
│   ├── core/                  # Capa transversal
│   │   ├── config.py          # Configuración desde .env
│   │   ├── database.py        # Conexión a BD (async SQLAlchemy)
│   │   ├── security.py        # JWT y bcrypt
│   │   ├── schemas.py         # Modelo base Pydantic
│   │   ├── logging.py         # Sistema de logs
│   │   ├── base_repository.py # CRUD genérico
│   │   └── image_service.py   # Subida/Wikipedia/placeholders
│   ├── api/
│   │   ├── dependencies.py    # Dependencias de autenticación
│   │   └── v1/router.py       # Registro de todos los routers
│   ├── artists/               # CRUD + imágenes
│   ├── albums/                # CRUD + imágenes
│   ├── genres/                # CRUD
│   ├── track/                 # CRUD
│   ├── activities/            # Auditoría
│   └── users/                 # Autenticación y gestión de usuarios
├── static/images/             # Imágenes subidas + placeholders
├── instance/Chinook.db        # Base de datos SQLite
├── tests/                     # Tests automatizados
└── scripts/                   # Utilidades para fetching de imágenes
```

Cada módulo de dominio sigue el patrón de 4 capas:

```
Router (HTTP) → Service (lógica) → Repository (BD) → Model (tabla SQLAlchemy)
```

---

## Tests

```bash
uv run python -m unittest discover -s tests -p "test_*.py"
```

---

## Documentación inline

Todas las funciones del proyecto tienen comentarios en español explicando qué hacen, para facilitar el aprendizaje de alumnos que cursan programación.
