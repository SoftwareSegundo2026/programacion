# fastAPI-example

API REST en FastAPI con autenticación JWT, CRUD completo para artistas/álbumes/géneros/tracks, imágenes, activity logging y control de usuarios admin.

## Stack

- **FastAPI** — async web framework
- **SQLAlchemy 2.0** (async) — ORM
- **SQLite + aiosqlite** — base de datos (Chinook)
- **python-jose + passlib** — JWT + bcrypt
- **httpx** — Wikipedia API calls
- **Pydantic v2** — validación

## Estructura del proyecto

```
fastAPI-example/
├── main.py                    # Entry point (uvicorn)
├── app/
│   ├── main.py                # FastAPI app (importado por main.py)
│   ├── core/
│   │   ├── config.py          # Settings via .env
│   │   ├── database.py        # AsyncSession, Base, get_db
│   │   ├── schemas.py         # CustomModel base
│   │   ├── security.py        # JWT create/verify, bcrypt hash
│   │   ├── logging.py         # setup_logging + get_logger
│   │   ├── base_repository.py # BaseRepository genérico (CRUD)
│   │   └── image_service.py   # Upload, Wikipedia fetch, placeholders
│   ├── auth/                  # Autenticación JWT
│   │   ├── model.py           # User (UserId, Username, Disabled, IsAdmin…)
│   │   ├── schemas.py         # Token, User, UserInDB, UserCreate, UserLogin
│   │   ├── service.py         # get_user, authenticate, create, change/reset password
│   │   ├── seeder.py          # Crea admin + reader demo
│   │   └── router.py          # POST /auth/token
│   ├── users/                 # Gestión de usuarios
│   │   ├── schemas.py         # UserUpdateDisabled, PasswordChange, PasswordReset
│   │   └── router.py          # GET/POST /users, PATCH activate/deactivate, password
│   ├── activities/            # Activity logging
│   │   ├── model.py           # Activity (ActivityId, Timestamp, Username, ActionType, Detail)
│   │   ├── schemas.py         # ActivityResponse
│   │   ├── service.py         # log_activity, list_activities (filtra admins)
│   │   └── router.py          # GET /activities (público, filtra por admin)
│   ├── artists/               # CRUD + imágenes
│   ├── albums/                # CRUD + imágenes
│   ├── genres/                # CRUD
│   ├── track/                 # CRUD
│   └── api/
│       ├── dependencies.py    # get_current_user, get_current_active_user, get_current_admin_user, get_optional_user
│       └── v1/router.py       # Registro de todos los routers
├── static/images/             # Uploads + default-artist.svg, default-album.svg
├── instance/Chinook.db        # BD SQLite
├── tests/
│   ├── test_jwt_flow.py       # Login, token inválido, usuario inactivo
│   └── test_track_flow.py     # CRUD de tracks autenticado
└── .env                       # Configuración
```

## Base de datos

Usa [Chinook](https://www.sqlite.org/chinook.html) (`instance/Chinook.db`), una BD de muestra con tablas `Artist`, `Album`, `Track`, `Genre`, `MediaType` y relaciones.

Columnas agregadas vía migration en startup:
- `Artist.ImageUrl`
- `Album.ImageUrl`
- `User.IsAdmin`

Y tablas nuevas creadas por SQLAlchemy `create_all`:
- `User`
- `Activity`

## Autenticación

`POST /api/v1/auth/token`

```json
{ "username": "admin", "password": "admin123" }
```

```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

### Usuarios demo

| Usuario | Password | Admin | Activo |
|---------|----------|-------|--------|
| `admin` | `admin123` | Sí | Sí |
| `reader` | `reader123` | No | No (disabled) |

### Dependencias de seguridad

| Dependencia | Uso |
|---|---|
| `get_current_user` | Valida JWT, devuelve `UserInDB` o 401 |
| `get_current_active_user` | Como arriba + verifica `disabled=False` |
| `get_current_admin_user` | Como arriba + verifica `is_admin=True` o 403 |
| `get_optional_user` | Devuelve `UserInDB` o `None` (no lanza error) |

Las rutas GET de artists, albums, genres, tracks son públicas. POST/PATCH/DELETE requieren `get_current_active_user`.

## Endpoints

### Auth

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/token` | — | Login, devuelve JWT |

### Users

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/users` | active | Lista usuarios (paginado: `?skip=0&limit=100`) |
| POST | `/users` | active | Crear usuario |
| PATCH | `/users/{id}` | admin | Activar/desactivar (`{"disabled": bool}`) |
| PATCH | `/users/me/password` | active | Cambiar propia contraseña (`{"current_password", "new_password"}`) |
| PATCH | `/users/{id}/password` | admin | Reset de contraseña (`{"new_password"}`) |

### Artists

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/artists` | — | Lista (paginado) |
| GET | `/artists/{id}` | — | Obtener uno |
| POST | `/artists` | active | Crear |
| PATCH | `/artists/{id}` | active | Actualizar |
| DELETE | `/artists/{id}` | active | Eliminar |
| POST | `/artists/{id}/image` | active | Subir imagen |
| GET | `/artists/{id}/image` | — | Obtener imagen |
| POST | `/artists/{id}/fetch-image` | active | Buscar imagen en Wikipedia |

### Albums

Igual que Artists: `GET/POST/PATCH/DELETE /albums`, más `/albums/{id}/image` y `/albums/{id}/fetch-image`.

### Genres / Tracks

CRUD completo: `GET/POST/PATCH/DELETE /genres` y `/tracks`. Tracks incluye `AlbumTitle`, `GenreName`, `MediaTypeName` en respuestas.

### Activities

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/activities` | pública* | Lista actividades (paginado) |

- **Admin** → ve todas
- **Anónimo / usuario regular** → ve todas excepto las realizadas por admins

Las actividades se registran automáticamente en: login, create/update/delete de cualquier entidad, cambios de contraseña, activate/deactivate de usuarios.

## Imágenes

Endpoints específicos para artists y albums:

- **Subir**: `POST /{entity}/{id}/image` (multipart, soporta jpg/png/gif/webp)
- **Servir**: `GET /{entity}/{id}/image` — devuelve el archivo subido, placeholder SVG por defecto (`default-artist.svg` / `default-album.svg`), o redirect a URL externa
- **Wikipedia fetch**: `POST /{entity}/{id}/fetch-image` — busca en Wikipedia la imagen y la guarda localmente

## Configuración

Variables de entorno (`.env`):

```
DATABASE_URL=sqlite+aiosqlite:///./instance/Chinook.db
SECRET_KEY=change-this-secret-key-for-jwt-development
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
LOG_FILE_PATH=./instance/fastapi-example.log
LOG_LEVEL=DEBUG
UPLOAD_DIR=./static/images
```

## Ejecución

```bash
# Instalar dependencias
uv sync

# Activar venv
source .venv/bin/activate

# Iniciar servidor (hot reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Swagger UI

`GET /docs` — Documentación interactiva. Pulsa `Authorize` y pega el token JWT para probar endpoints protegidos.

## Logs

Cada operación escribe trazas numeradas en consola y en `./instance/fastapi-example.log`. Además, las actividades se persisten en la tabla `Activity` y son consultables via `GET /activities`.

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Cubre:
- Login con credenciales válidas/incorrectas
- Token expirado
- Acceso de usuario inactivo
- CRUD completo de Track autenticado
