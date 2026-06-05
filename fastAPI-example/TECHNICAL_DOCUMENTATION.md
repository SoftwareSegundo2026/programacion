# Documentación Técnica — FastAPI Chinook API

**Versión:** 1.0.0  
**Última actualización:** Junio 2026  
**Repositorio:** `Material-Clase/fastAPI-example`

---

## Índice

1. [Descripción General](#1-descripción-general)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Arquitectura del Proyecto](#3-arquitectura-del-proyecto)
4. [Base de Datos](#4-base-de-datos)
5. [Autenticación y Autorización](#5-autenticación-y-autorización)
6. [API Reference](#6-api-reference)
7. [Modelo de Actividades (Audit Log)](#7-modelo-de-actividades-audit-log)
8. [Módulo de Imágenes](#8-módulo-de-imágenes)
9. [Seguridad](#9-seguridad)
10. [Despliegue](#10-despliegue)
11. [Pruebas](#11-pruebas)
12. [Mantenimiento](#12-mantenimiento)

---

## 1. Descripción General

API REST construida con **FastAPI** que expone la base de datos **Chinook** (SQLite) a través de endpoints CRUD protegidos con autenticación JWT. Incluye:

- CRUD completo para **Artistas, Álbumes, Géneros y Tracks**
- **Autenticación JWT** con dos roles: `admin` y `reader`
- **Gestión de usuarios** (crear, activar/desactivar, cambio de contraseña, reset por admin, eliminar)
- **Activity Logging** (auditoría de todas las operaciones)
- **Servicio de imágenes** (subida, Wikipedia fetch, placeholders SVG)
- **Paginación** en todos los endpoints GET de listado
- **Documentación interactiva** via Swagger UI y ReDoc

### Propósito

Servir como backend para aplicaciones de catálogo musical, permitiendo la administración de una biblioteca de artistas, álbumes, géneros y pistas musicales, con control de acceso basado en roles.

---

## 2. Stack Tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| Framework Web | FastAPI | ≥0.135.3 |
| ORM | SQLAlchemy 2.0 (async) | ≥2.0.49 |
| Base de Datos | SQLite + aiosqlite | ≥0.19.0 |
| Autenticación | python-jose + passlib (bcrypt) | ≥3.3.0 / ≥1.7.4 |
| Validación | Pydantic v2 | — |
| Servidor ASGI | Uvicorn | ≥0.44.0 |
| HTTP Client | httpx | ≥0.27.0 |
| File Uploads | python-multipart | ≥0.0.9 |
| Configuración | pydantic-settings | ≥2.0.0 |
| Lenguaje | Python | ≥3.11 |
| Entorno | uv (package manager) | — |

---

## 3. Arquitectura del Proyecto

### 3.1 Estructura de directorios

```
fastAPI-example/
├── main.py                          # Entry point del servidor
├── pyproject.toml                   # Dependencias y metadatos
├── .env                             # Variables de entorno
│
├── app/
│   ├── main.py                      # FastAPI app, lifespan, middleware
│   │
│   ├── core/                        # Capa transversal
│   │   ├── config.py                # Settings via .env
│   │   ├── database.py              # Async engine, session, Base
│   │   ├── schemas.py               # CustomModel base para Pydantic
│   │   ├── security.py             # JWT y bcrypt
│   │   ├── logging.py              # Logger configuración y trazabilidad
│   │   ├── base_repository.py      # Generic CRUD: BaseRepository
│   │   └── image_service.py        # Upload, Wikipedia fetch, placeholders
│   │
│   ├── api/
│   │   ├── dependencies.py         # Dependencias de auth
│   │   └── v1/
│   │       └── router.py           # Registro de todos los routers
│   │
│   ├── auth/                       # Módulo de autenticación
│   │   ├── model.py                # User (ORM)
│   │   ├── schemas.py              # Token, User, UserInDB, UserCreate
│   │   ├── service.py              # Lógica de negocio: auth, users
│   │   ├── seeder.py               # Usuarios demo
│   │   └── router.py               # POST /auth/token
│   │
│   ├── users/                      # Gestión de usuarios
│   │   ├── schemas.py              # PasswordChange, PasswordReset, UserUpdateDisabled
│   │   └── router.py              # CRUD usuarios + /me + password
│   │
│   ├── activities/                 # Auditoría
│   │   ├── model.py                # Activity (ORM)
│   │   ├── schemas.py              # ActivityResponse
│   │   ├── service.py              # log_activity, list_activities
│   │   └── router.py              # GET /activities
│   │
│   ├── artists/                    # Módulo Artist
│   │   ├── model.py / schemas.py / repository.py / service.py / router.py
│   │
│   ├── albums/                     # Módulo Album
│   │   ├── model.py / schemas.py / repository.py / service.py / router.py
│   │
│   ├── genres/                     # Módulo Genre
│   │   ├── model.py / schemas.py / repository.py / service.py / router.py
│   │
│   └── track/                      # Módulo Track
│       ├── model.py / schemas.py / repository.py / service.py / router.py
│
├── static/images/                  # Uploads de imágenes + defaults
│   ├── default-artist.svg
│   ├── default-album.svg
│   ├── artists/                    # Imágenes de artistas
│   └── albums/                     # Imágenes de álbumes
│
├── instance/
│   ├── Chinook.db                  # Base de datos SQLite
│   └── fastapi-example.log         # Logs de aplicación
│
├── tests/
│   ├── test_jwt_flow.py            # Tests de autenticación
│   └── test_track_flow.py          # Tests CRUD tracks
│
└── scripts/
    ├── fetch_from_deezer.py
    ├── fetch_all_images.py
    └── fetch_remaining_images.py
```

### 3.2 Patrón por capas (Domain-Driven)

Cada módulo de dominio (artists, albums, genres, track) sigue el mismo patrón:

```
router.py  →  service.py  →  repository.py  →  model.py (ORM)
```

| Capa | Responsabilidad |
|---|---|
| **Router** | Endpoints HTTP, validación de entrada, dependencias de auth |
| **Service** | Lógica de negocio, coordinación entre repositorios |
| **Repository** | Consultas a base de datos (hereda de `BaseRepository`) |
| **Model** | Definición de tablas SQLAlchemy |

### 3.3 Flujo de una petición

```
Cliente → FastAPI → Router → Dependencies (auth) → Service → Repository → DB
                                                             ↓
                                                         Response ← Serializer (Pydantic)
```

Toda petición POST/PATCH/DELETE pasa por `get_current_active_user` (JWT + usuario activo). Las rutas GET de consulta son públicas.

---

## 4. Base de Datos

### 4.1 Esquema

La base de datos es **Chinook**, un dataset de muestra de una tienda de música digital. Tablas principales:

| Tabla | Columnas clave |
|---|---|
| `Artist` | `ArtistId`, `Name`, `ImageUrl` |
| `Album` | `AlbumId`, `Title`, `ArtistId` (FK), `ImageUrl` |
| `Track` | `TrackId`, `Name`, `AlbumId` (FK), `MediaTypeId` (FK), `GenreId` (FK), `Composer`, `Milliseconds`, `Bytes`, `UnitPrice` |
| `Genre` | `GenreId`, `Name` |
| `MediaType` | `MediaTypeId`, `Name` |
| `User` | `UserId`, `Username`, `Email`, `FullName`, `Disabled`, `IsAdmin`, `HashedPassword` |
| `Activity` | `ActivityId`, `Timestamp`, `Username`, `ActionType`, `Detail` |

### 4.2 Migraciones automáticas

En el startup (`lifespan`), la aplicación ejecuta:

```python
Base.metadata.create_all       # Crea tablas nuevas (User, Activity)
ALTER TABLE Artist ADD COLUMN ImageUrl VARCHAR(500)
ALTER TABLE Album ADD COLUMN ImageUrl VARCHAR(500)
ALTER TABLE User ADD COLUMN IsAdmin BOOLEAN DEFAULT 0
UPDATE "User" SET IsAdmin = 1 WHERE Username = 'admin'
```

### 4.3 Datos semilla

Se crean automáticamente dos usuarios demo si no existen:

| Usuario | Password | Admin | Activo |
|---|---|---|---|
| `admin` | `admin123` | Sí | Sí |
| `reader` | `reader123` | No | No (disabled) |

---

## 5. Autenticación y Autorización

### 5.1 Flujo JWT

```
POST /api/v1/auth/token
Body: { "username": "admin", "password": "admin123" }
→ 200: { "access_token": "eyJ...", "token_type": "bearer" }
```

El token JWT contiene únicamente el `sub` (username). No incluye roles ni claims adicionales. Para obtener el perfil completo (incluyendo `is_admin`) se debe consultar `GET /users/me` con el token.

### 5.2 Jerarquía de dependencias

```
get_optional_user          → UserInDB | None (no lanza error)
get_current_user           → UserInDB o 401
get_current_active_user    → UserInDB (verifica disabled=False) o 400
get_current_admin_user     → UserInDB (verifica is_admin=True) o 403
```

### 5.3 Endpoints por nivel de acceso

| Nivel | Endpoints |
|---|---|
| **Público** | GET `/artists`, GET `/artists/{id}`, GET `/artists/{id}/image`, GET `/albums`, GET `/albums/{id}`, GET `/albums/{id}/image`, GET `/genres`, GET `/genres/{id}`, GET `/tracks`, GET `/tracks/{id}`, GET `/activities` |
| **Usuario activo** | POST/PATCH/DELETE de todas las entidades, GET/POST `/users`, GET `/users/me`, PATCH `/users/me/password` |
| **Admin** | PATCH `/users/{id}` (activate/deactivate), PATCH `/users/{id}/password` (reset), DELETE `/users/{id}` |

---

## 6. API Reference

### 6.1 Auth

| Método | Ruta | Auth | Request | Response | Descripción |
|---|---|---|---|---|---|
| POST | `/auth/token` | — | `{username, password}` | `{access_token, token_type}` | Login JWT |

### 6.2 Users

| Método | Ruta | Auth | Request | Response | Descripción |
|---|---|---|---|---|---|
| GET | `/users` | active | `?skip=0&limit=100` | `[User]` | Listar usuarios |
| POST | `/users` | active | `UserCreate` | `User` | Crear usuario |
| GET | `/users/me` | active | — | `User` | Perfil del usuario autenticado |
| PATCH | `/users/me/password` | active | `{current_password, new_password}` | 204 | Cambiar contraseña propia |
| PATCH | `/users/{id}` | admin | `{disabled: bool}` | `User` | Activar/desactivar usuario |
| PATCH | `/users/{id}/password` | admin | `{new_password}` | 204 | Reset de contraseña |
| DELETE | `/users/{id}` | admin | — | 204 | Eliminar usuario |

### 6.3 Artists

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/artists` | — | Lista paginada (`?skip=0&limit=100`) |
| GET | `/artists/{id}` | — | Obtener por ID |
| POST | `/artists` | active | Crear |
| PATCH | `/artists/{id}` | active | Actualizar |
| DELETE | `/artists/{id}` | active | Eliminar |
| POST | `/artists/{id}/image` | active | Subir imagen (multipart) |
| GET | `/artists/{id}/image` | — | Servir imagen o placeholder |
| POST | `/artists/{id}/fetch-image` | active | Buscar imagen en Wikipedia |

### 6.4 Albums

Mismos endpoints que Artists, reemplazando `artists` por `albums`.

### 6.5 Genres

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/genres` | — | Lista paginada |
| GET | `/genres/{id}` | — | Obtener por ID |
| POST | `/genres` | active | Crear |
| PATCH | `/genres/{id}` | active | Actualizar |
| DELETE | `/genres/{id}` | active | Eliminar |

### 6.6 Tracks

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/tracks` | — | Lista paginada |
| GET | `/tracks/{id}` | — | Obtener por ID |
| POST | `/tracks` | active | Crear |
| PATCH | `/tracks/{id}` | active | Actualizar |
| DELETE | `/tracks/{id}` | active | Eliminar |

> Los tracks incluyen en su respuesta los campos calculados `AlbumTitle`, `GenreName` y `MediaTypeName` para facilitar el consumo desde el frontend.

### 6.7 Activities

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/activities` | Pública* | Lista paginada de auditoría |

**Filtrado automático:** Si el usuario autenticado es **admin**, ve **todas** las actividades. Si es **anónimo** o **usuario regular**, ve solo las actividades que **no** involucren a usuarios admin.

El listado se ordena por `activity_id` descendente (más recientes primero).

### 6.8 Modelos de datos (schemas)

#### User
```json
{
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Demo Admin",
  "disabled": false,
  "is_admin": true
}
```

#### Artist
```json
{
  "ArtistId": 1,
  "Name": "AC/DC",
  "ImageUrl": "/static/images/artists/1.jpg"
}
```

#### Album
```json
{
  "AlbumId": 1,
  "Title": "For Those About To Rock We Salute You",
  "ArtistId": 1,
  "ArtistName": "AC/DC",
  "ImageUrl": "/static/images/albums/1.jpg"
}
```

#### Track
```json
{
  "TrackId": 1,
  "Name": "For Those About To Rock (We Salute You)",
  "AlbumId": 1,
  "AlbumTitle": "For Those About To Rock We Salute You",
  "MediaTypeId": 1,
  "MediaTypeName": "MPEG audio file",
  "GenreId": 1,
  "GenreName": "Rock",
  "Composer": "Angus Young, Malcolm Young, Brian Johnson",
  "Milliseconds": 343719,
  "Bytes": 11170334,
  "UnitPrice": 0.99
}
```

#### Activity
```json
{
  "activity_id": 1,
  "timestamp": "2026-06-04T21:01:28",
  "username": "admin",
  "action_type": "login",
  "detail": null
}
```

---

## 7. Modelo de Actividades (Audit Log)

Cada operación relevante registra automáticamente una entrada en la tabla `Activity`:

| Acción | `action_type` | `detail` ejemplo |
|---|---|---|
| Login exitoso | `login` | `null` |
| Crear artista | `create` | `Artist: AC/DC (id=1)` |
| Actualizar álbum | `update` | `Album id=1` |
| Eliminar track | `delete` | `Track id=1` |
| Activar/desactivar usuario | `update` | `User activate: reader (id=2)` |
| Cambio de contraseña | `update` | `Password changed` |
| Reset de contraseña | `update` | `Password reset for user id=2` |
| Crear usuario | `create` | `User: newuser` |

---

## 8. Módulo de Imágenes

### 8.1 Subida manual

`POST /{entity}/{id}/image` acepta un archivo multipart (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`). Reemplaza automáticamente la imagen anterior si existe.

### 8.2 Wikipedia Fetch

`POST /{entity}/{id}/fetch-image` busca la imagen en Wikipedia usando el nombre de la entidad como query, descarga la miniatura y la guarda localmente.

### 8.3 Servir imágenes

`GET /{entity}/{id}/image` resuelve la imagen según el `ImageUrl` almacenado:

| `ImageUrl` | Comportamiento |
|---|---|
| Ruta local (`/static/images/...`) | `FileResponse` con el archivo |
| URL externa | `RedirectResponse` a la URL |
| `null` o vacío | Placeholder SVG (`default-artist.svg` o `default-album.svg`) |

### 8.4 Directorio de uploads

```
static/images/
├── default-artist.svg        # Placeholder artista
├── default-album.svg         # Placeholder álbum
├── artists/
│   ├── 1.jpg                 # ArtistId=1
│   ├── 2.png
│   └── ...
└── albums/
    ├── 1.jpg
    └── ...
```

---

## 9. Seguridad

### 9.1 Contraseñas

- Hash: **bcrypt** via `passlib`
- Sal automática por algoritmo
- Nunca se almacenan en texto plano

### 9.2 JWT

- Algoritmo: **HS256**
- Expiración configurable (`ACCESS_TOKEN_EXPIRE_MINUTES`, default 30 min)
- Secret key via variable de entorno (`SECRET_KEY`)

### 9.3 Protección de endpoints

- Todos los endpoints mutantes (POST/PATCH/DELETE) requieren autenticación
- Endpoints sensibles (gestión de usuarios) requieren rol admin
- Las rutas GET de consulta son públicas
- Endpoint `/activities` es público pero filta actividades de admin para usuarios no admin

### 9.4 Variables de entorno sensibles

```env
SECRET_KEY=change-this-secret-key-for-jwt-development
```

> **⚠️ Importante:** Cambiar `SECRET_KEY` por un valor seguro en producción. Se recomienda `openssl rand -hex 32`.

---

## 10. Despliegue

### 10.1 Requisitos

- Python ≥ 3.11
- uv (gestor de paquetes)

### 10.2 Instalación

```bash
git clone <repo>
cd fastAPI-example
uv sync
source .venv/bin/activate
```

### 10.3 Configuración

Copiar `.env.example` a `.env` y ajustar:

```env
DATABASE_URL=sqlite+aiosqlite:///./instance/Chinook.db
SECRET_KEY=<generar-clave-segura>
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
LOG_FILE_PATH=./instance/fastapi-example.log
LOG_LEVEL=INFO
UPLOAD_DIR=./static/images
```

### 10.4 Ejecución

```bash
# Desarrollo (hot reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 10.5 Endpoints de documentación

| URL | Descripción |
|---|---|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |
| `http://localhost:8000/openapi.json` | OpenAPI Schema |

### 10.6 Notas de producción

- **SQLite** no está recomendado para alta concurrencia. Migrar a PostgreSQL reemplazando `DATABASE_URL` y el driver async (`asyncpg`).
- El directorio `static/images` debe tener permisos de escritura para el usuario del proceso.
- El archivo `instance/fastapi-example.log` rotará según la configuración de logging del sistema operativo.
- En producción establecer `LOG_LEVEL=INFO` o `WARNING` para evitar saturación de logs.

---

## 11. Pruebas

### 11.1 Suite de tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### 11.2 Cobertura

| Archivo | Escenario |
|---|---|
| `test_jwt_flow.py` | Login exitoso, credenciales incorrectas, token expirado, usuario inactivo |
| `test_track_flow.py` | CRUD completo de track autenticado |

### 11.3 Tests manuales recomendados

- Verificar que GET públicos funcionan sin token
- Verificar 401 en endpoints protegidos sin token
- Verificar 403 en endpoints admin con token de usuario regular
- Verificar 400 para usuarios disabled
- Verificar paginación con `?skip=0&limit=5`
- Verificar subida de imágenes y placeholder por defecto
- Verificar filtrado de activities para usuarios no admin

---

## 12. Mantenimiento

### 12.1 Agregar un nuevo módulo CRUD

1. Crear `app/<entity>/` con: `model.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`
2. Heredar `BaseRepository` en repository
3. Agregar `from app.<entity>.router import router as <entity>_router` en `app/api/v1/router.py`
4. Agregar migración ALTER TABLE si es necesario en `main.py`

### 12.2 Agregar un nuevo campo a un modelo existente

1. Agregar columna al modelo SQLAlchemy
2. Agregar campo al schema Pydantic
3. Agregar `ALTER TABLE` en el bloque de migraciones de `main.py`
4. Si requiere valores default para registros existentes, agregar `UPDATE`

### 12.3 Posibles mejoras futuras

| Mejora | Impacto |
|---|---|
| Migrar a PostgreSQL | Concurrencia, transacciones robustas |
| Implementar refresh tokens | Mayor seguridad JWT |
| Rate limiting | Prevención de abuso en endpoints públicos |
| Paginación con cursor | Performance en tablas grandes |
| Tests con base de datos de prueba | Aislamiento de tests |
| CI/CD pipeline | Integración continua automatizada |
| Dockerizar la aplicación | Despliegue reproducible |
| Búsqueda full-text en tracks | Mejora UX del catálogo |
| Caché con Redis | Performance en endpoints muy consultados |
| Webhooks para eventos | Integración con sistemas externos |

---

*Documentación generada para el departamento técnico del cliente. Para preguntas técnicas contactar al equipo de desarrollo.*
