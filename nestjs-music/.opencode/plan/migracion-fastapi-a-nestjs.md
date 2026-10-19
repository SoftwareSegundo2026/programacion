# Plan de migración: fastAPI-example → NestJS

> Documento vivo. Revisá las **decisiones abiertas** (§0) y marcá las fases a medida que avancen.
> Fuente: `../fastAPI-example` · Destino: este proyecto (`nestjs-music`)

---

## 0. Decisiones abiertas

**Cómo marcar**: cambiá `[ ]` por `[x]` en la opción elegida (una sola por fila).
🌟 marca la recomendación por defecto; si no tocás nada, se asume esa.

### 0.1 Stack y comportamiento

| #   | Punto                        | Opción 1                                                                           | Opción 2                                                         | Opción 3                             | Opción 4       |
| --- | ---------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------ | -------------- |
| 1   | **ORM**                      | `[ ]` 🌟 TypeORM — el más cercano a SQLAlchemy, es el de las docs de Nest          | `[ ]` Prisma                                                     | `[ ]` Drizzle                        | `[ ]` MikroORM |
| 2   | **Estrategia de esquema BD** | `[ ]` 🌟 Script idempotente en `OnModuleInit` (igual que el `lifespan` de FastAPI) | `[ ]` Migrations de TypeORM                                      | `[ ]` `synchronize: true` (solo dev) | —              |
| 3   | **Archivo de BD**            | `[ ]` 🌟 Mismo `../fastAPI-example/instance/Chinook.db` (sin migrar datos)         | `[ ]` Copia en `instance/Chinook.db`                             | `[ ]` BD nueva + seed                | —              |
| 4   | **Gestor de paquetes**       | `[ ]` 🌟 pnpm (el actual del proyecto)                                             | `[ ]` npm                                                        | `[ ]` yarn                           | `[ ]` bun      |
| 5   | **Puerto por defecto**       | `[ ]` 🌟 3300 (el actual en `.env`)                                                | `[ ]` 3000 (default de Nest)                                     | —                                    | —              |
| 6   | **Contraseñas**              | `[ ]` 🌟 `bcryptjs` — JS puro, sin compilar, ideal para alumnos                    | `[ ]` `bcrypt` (nativo)                                          | —                                    | —              |
| 7   | **Autenticación**            | `[ ]` 🌟 Guard propio + `@nestjs/jwt` — se ve todo el flujo, menos dependencias    | `[ ]` `@nestjs/passport` + `passport-jwt`                        | —                                    | —              |
| 8   | **Rutas / slash final**      | `[ ]` 🌟 Sin slash: `/api/v1/artists` (como documenta el README del fuente)        | `[ ]` Con slash: `/api/v1/artists/` (el fuente redirige con 307) | `[ ]` Ambas variantes aceptadas      | —              |
| 9   | **Idioma de comentarios**    | `[ ]` 🌟 Español (el fuente es didáctico, material de cátedra)                     | `[ ]` Inglés                                                     | —                                    | —              |
| 10  | **Bugs del fuente (§1.1)**   | `[ ]` 🌟 Corregirlos en `fastAPI-example` y además implementar bien en Nest        | `[ ]` Solo corregir en NestJS (el fuente queda roto)             | —                                    | —              |

### 0.2 Sí / No

| #   | Punto                                                                                            | Sí 🌟 | No    | Nota                                              |
| --- | ------------------------------------------------------------------------------------------------ | ----- | ----- | ------------------------------------------------- |
| 1   | ¿Migrar los tests Python (`test_jwt_flow`, `test_track_flow`) a Vitest en la Fase 6?             | `[ ]` | `[ ]` | Dan la paridad verificable                        |
| 2   | ¿Conservar `@nestjs/observe`?                                                                    | `[ ]` | `[ ]` | Sin credenciales queda desactivado, no spamea 401 |
| 3   | ¿Commitear `nestjs-music/` al repo `Material-Clase` (`SoftwareSegundo2026/programacion`)?        | `[ ]` | `[ ]` | Hoy está sin trackear                             |
| 4   | ¿Cerrar estas decisiones y generar el resto del `.opencode` (AGENTS.md, agent, skill, commands)? | `[ ]` | `[ ]` | Se genera en base a lo que marques arriba         |

---

## 1. Contexto

### 1.1 Estado del proyecto fuente ⚠️

**El fuente está roto hoy: `uv run python -m unittest discover -s tests` → `FAILED (errors=5)`.
La causa raíz de los 5 errores es el endpoint de login.** Defectos detectados:

| #   | Archivo                                          | Defecto                                                                                                                                     | Efecto                                                           |
| --- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 1   | `app/users/router.py` → `login_for_access_token` | `if user is None:` pero **`user` nunca se asigna** (falta `user = await authenticate_user(db, credentials.username, credentials.password)`) | `NameError` → 500 en `POST /auth/token` → **los 5 tests fallan** |
| 2   | `app/users/router.py` → `read_users`             | función **sin cuerpo/return** con `response_model=list[User]`                                                                               | `GET /users` no puede responder                                  |

**Recomendación**: corregir los dos defectos en el fuente (2 líneas) _antes_ de migrar, para que el fuente sea una referencia ejecutable contra la cual comparar paridad. La versión NestJS igualmente implementa la lógica correcta.

### 1.2 Stack

|               | Fuente                           | Destino                                            |
| ------------- | -------------------------------- | -------------------------------------------------- |
| Framework     | FastAPI (async)                  | NestJS 12 (TypeScript **ESM**, `"type": "module"`) |
| ORM           | SQLAlchemy 2.0 async             | TypeORM (pendiente §0)                             |
| BD            | SQLite `instance/Chinook.db`     | el mismo archivo (pendiente §0)                    |
| Validación    | Pydantic v2                      | `class-validator` + `class-transformer`            |
| Auth          | `python-jose` + `passlib/bcrypt` | `@nestjs/jwt` + `bcryptjs`                         |
| Tests         | `unittest` + `TestClient`        | Vitest + supertest                                 |
| Lint / format | —                                | oxlint (type-aware) + Prettier                     |
| Config        | `pydantic-settings` + `.env`     | `@nestjs/config` + `.env` (⚠️ ver nota abajo)      |

> **Nota**: `nest start` **no** carga `.env` por sí solo; en este proyecto lo hace `ConfigModule.forRoot()`
> en `src/app.module.ts` (guardado en una variable _antes_ de leer `process.env` — ver comentario ahí).
> `src/main.ts` lee `PORT` con `ConfigService`. Esto ya está funcionando, no romperlo.

### 1.3 Tablas de Chinook en la BD

Ya existen: `Activity`, `Album`, `Artist`, `Customer`, `Employee`, `Genre`, `Invoice`, `InvoiceLine`, `MediaType`, `Playlist`, `PlaylistTrack`, `Track`, `User`.

Se usan **solo** las que cubre la API: `Artist`, `Album`, `Genre`, `Track`, `MediaType`, `User`, `Activity`.
`Customer/Employee/Invoice/Playlist*` quedan fuera de alcance (documentadas en `../fastAPI-example/models-all/models.py`).

Columnas clave a respetar (PascalCase en BD, snake_case en Python):

- `User(UserId, Username, Email, FullName, Disabled, IsAdmin, HashedPassword)`
- `Artist(ArtistId, Name, ImageUrl)` — `ImageUrl` agregada por migración ad-hoc en `lifespan`
- `Album(AlbumId, Title, ArtistId, ImageUrl)`
- `Genre(GenreId, Name)`
- `Track(TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)`
- `Activity(ActivityId, Timestamp, Username, ActionType, Detail)`

### 1.4 Inventario de endpoints (paridad obligatoria)

Prefijo global: `/api/v1` (`API_V1_STR`).

**Auth — público**

| Método | Ruta          | Éxito                                     | Notas                                             |
| ------ | ------------- | ----------------------------------------- | ------------------------------------------------- |
| POST   | `/auth/token` | 200 `{access_token, token_type:"bearer"}` | 401 `{"detail":"Incorrect username or password"}` |

**Users**

| Método | Ruta                   | Auth      | Éxito                                      |
| ------ | ---------------------- | --------- | ------------------------------------------ |
| GET    | `/users`               | activo    | 200 `list[User]` (paginado `skip`/`limit`) |
| POST   | `/users`               | activo    | 201 · 409 si username/email existe         |
| GET    | `/users/me`            | activo    | 200                                        |
| PATCH  | `/users/me`            | activo    | 200                                        |
| PATCH  | `/users/me/password`   | activo    | 204 · 400 si password actual incorrecto    |
| PATCH  | `/users/{id}`          | **admin** | 200 · 404                                  |
| PATCH  | `/users/{id}/password` | **admin** | 204 · 404                                  |
| DELETE | `/users/{id}`          | **admin** | 204 · 404                                  |

**Artists** (`/artists`) — 8 rutas

| Método | Ruta                        | Auth    | Éxito                                    |
| ------ | --------------------------- | ------- | ---------------------------------------- |
| POST   | `/artists`                  | activo  | 201 + `log_activity`                     |
| GET    | `/artists`                  | público | 200 lista paginada                       |
| GET    | `/artists/{id}`             | público | 200 · 404 `Artist not found`             |
| PATCH  | `/artists/{id}`             | activo  | 200 · 404                                |
| DELETE | `/artists/{id}`             | activo  | 204 · 404                                |
| POST   | `/artists/{id}/image`       | activo  | 200 · 400 ext inválida                   |
| GET    | `/artists/{id}/image`       | público | archivo / 302 redirect / SVG placeholder |
| POST   | `/artists/{id}/fetch-image` | activo  | 200 · 404 / 503 (Wikipedia rate-limit)   |

**Albums** (`/albums`) — mismas 8 rutas que artists (recurso `Album`, 404 `Album not found`).

**Genres** (`/genres`) — 5 rutas (POST, GET lista, GET one, PATCH, DELETE). Sin imágenes.

**Tracks** (`/tracks`) — 5 rutas (POST, GET lista, GET one, PATCH, DELETE). Sin imágenes.

- `Response` incluye `AlbumTitle`, `GenreName`, `MediaTypeName` (propiedades derivadas de relaciones).
- `UnitPrice` es `Decimal(10,2)`.

**Activities**

| Método | Ruta          | Auth         | Éxito                                                                        |
| ------ | ------------- | ------------ | ---------------------------------------------------------------------------- |
| GET    | `/activities` | **opcional** | 200 lista paginada · un no-admin **no ve** las actividades de usuarios admin |

**Raíz / infra**

| Método | Ruta           | Comportamiento                        |
| ------ | -------------- | ------------------------------------- |
| GET    | `/`            | devuelve `static/index.html`          |
| GET    | `/favicon.ico` | 302 → `/static/favicon.svg`           |
| *      | `/static/**`   | archivos estáticos (imágenes subidas) |

### 1.5 Comportamientos transversales a replicar

- **Paginación**: query params `skip` (default 0) y `limit` (default 100) en todos los listados.
- **Errores**: cuerpo FastAPI `{"detail": "..."}` → usar un **exception filter** que emita ese formato (la Nest por defecto usa `{statusCode, message, error}`).
- **Auditoría**: `log_activity(db, username, action_type, detail)` en cada POST/PATCH/DELETE y en el login.
- **Semanía de arranque** (equivalente al `lifespan` de FastAPI → `OnModuleInit`):
  1. `create_all` / `synchronize` de tablas
  2. migración ad-hoc: `ALTER TABLE` para `Artist.ImageUrl`, `Album.ImageUrl`, `User.IsAdmin` (si no existen)
  3. `UPDATE "User" SET IsAdmin = 1 WHERE Username = 'admin'`
  4. seed de usuarios demo: `admin/admin123` (activo, admin) y `reader/reader123` (**deshabilitado**)
- **Imágenes** (`../fastAPI-example/app/core/image_service.py`):
  - extensiones permitidas: `.jpg .jpeg .png .gif .webp`
  - guardado en `static/images/{artists|albums}/{id}{ext}`, reemplaza la anterior
  - `GET .../image`: si `ImageUrl` empieza con `/static/` → FileResponse; si es externa → redirect; si es `null` → SVG placeholder (`default-artist.svg` / `default-album.svg`)
  - `fetch-image`: busca en la API de Wikipedia (pageimages), descarga el thumbnail y lo guarda localmente; 403 de Wikipedia → 503 con mensaje
- **CORS**: `allow_origins=["*"]` → `app.enableCors()` en `main.ts`.
- **Seed/demo**: usuarios demo y usuarios creados por test quedan en la BD (el fuente no los limpia).

---

## 2. Estructura destino propuesta

```
src/
├── main.ts                      # CORS, PORT (ConfigService), static, index.html
├── app.module.ts                # ConfigModule + módulos
├── app.controller.ts / .service.ts   # GET / (index.html) — reemplazar Hello World
├── database/
│   ├── data-source.ts           # TypeORM DataSource (si aplica)
│   └── seed.ts                  # usuarios demo + migración de columnas
├── common/
│   ├── base-repository.ts       # genérico (equiv. app/core/base_repository.py)
│   ├── dto/pagination.dto.ts    # skip/limit
│   ├── filters/http-exception.filter.ts  # → {"detail": ...}
│   ├── decorators/current-user.decorator.ts
│   └── guards/
│       ├── auth.guard.ts        # equival. get_current_active_user
│       ├── admin.guard.ts       # equival. get_current_admin_user
│       └── optional-auth.guard.ts  # equival. get_optional_user
├── security/
│   ├── hash.service.ts          # bcryptjs: hash/verify
│   └── jwt.module.ts            # JwtModule global
├── artists/   albums/   genres/   tracks/
│   ├── <ent>.entity.ts
│   ├── dto/create-<ent>.dto.ts / update-<ent>.dto.ts / <ent>.response.ts
│   ├── <ent>.repository.ts
│   ├── <ent>.service.ts
│   └── <ent>.controller.ts
├── auth/      # controller de login + servicio
├── users/     # CRUD + me + passwords (usa hash.service)
├── activities/
└── images/
    ├── image.service.ts         # saveUpload / resolve / fetchFromWikipedia
    └── images.module.ts
```

Patrón por dominio (espejo de la arquitectura de 4 capas del fuente):

```
Router (FastAPI) → Controller (Nest)
Service          → Service (provider)
Repository       → Repository (extiende BaseRepository<T>)
Model (SQLAlchemy) → Entity (TypeORM)
Schemas (Pydantic) → DTOs (class-validator)
Depends(auth)    → @UseGuards + @CurrentUser()
```

---

## 3. Fases

Cada fase cierra con su **verificación**: `pnpm run build && pnpm run lint && pnpm run test && pnpm run test:e2e`.

### Fase 0 — Setup del proyecto

- [ ] **Cerrar §0** (tablas de decisiones) — todo lo que sigue depende de esas marcas
- [ ] Instalar dependencias según lo elegido: base `typeorm @nestjs/typeorm sqlite3 @nestjs/config @nestjs/jwt bcryptjs class-validator class-transformer multer` (+ variaciones según ORM/auth de §0)
- [ ] `.env` / `.env.example`: `PORT`, `JWT_SECRET`, `JWT_EXPIRES_IN`, `UPLOAD_DIR`, `LOG_LEVEL`
- [ ] DataSource + `synchronize: false` (la BD ya existe) + conexión al archivo Chinook
- [ ] Confirmar que `GET /` sigue sirviendo algo y que `pnpm build` pasa

### Fase 1 — Núcleo transversal

- [ ] `BaseRepository<T>` genérico (get / get_multi / create / update / delete)
- [ ] `PaginationDto` (`skip`, `limit`)
- [ ] `HttpExceptionFilter` → `{"detail": ...}` (paridad de errores)
- [ ] `HashService` (bcryptjs) y `JwtModule` global (`sub` = username, expiración desde `.env`)
- [ ] Guards: `auth`, `admin`, `optional-auth` + decorator `@CurrentUser()`
- [ ] Módulo `database` con `OnModuleInit`: columnas extra + `IsAdmin` + seed demo (§1.5)
- [ ] CORS habilitado

### Fase 2 — Dominios CRUD

Orden por complejidad creciente: **genres → artists → albums → tracks**

- [ ] `genres` (5 rutas)
- [ ] `artists` CRUD (5 rutas sin imágenes) + relaciones `albums`
- [ ] `albums` CRUD (5 rutas sin imágenes) + propiedad `ArtistName`
- [ ] `tracks` CRUD (5 rutas) + `AlbumTitle` / `GenreName` / `MediaTypeName` + `UnitPrice` decimal
- [ ] `log_activity` en cada POST/PATCH/DELETE

### Fase 3 — Auth y usuarios

- [ ] `POST /auth/token` — **implementación correcta** (`authenticate_user` + 401 si falla)
- [ ] Guard de auth aplicado a todos los POST/PATCH/DELETE de la Fase 2
- [ ] `users`: GET lista, POST (409), GET/PATCH `me`, PATCH `me/password` (204/400)
- [ ] Admin: PATCH `{id}`, PATCH `{id}/password`, DELETE `{id}`
- [ ] Verificar 401 sin token, 403 con `reader` (deshabilitado → 400), 403 en rutas admin

### Fase 4 — Activities

- [ ] `GET /activities` con auth opcional + filtro de actividades de admins para no-admins
- [ ] Orden `ActivityId` desc, paginación

### Fase 5 — Imágenes y estáticos

- [ ] `POST {artists|albums}/{id}/image` (FileInterceptor, extensiones permitidas, 400 si no)
- [ ] `GET {artists|albums}/{id}/image` (file / redirect / placeholder SVG)
- [ ] `POST {artists|albums}/{id}/fetch-image` (Wikipedia: search → pageimages → descarga; 404/503)
- [ ] Montar `/static` y `GET /` → `static/index.html`, favicon → `/static/favicon.svg`

### Fase 6 — Tests y documentación

- [ ] Port de `tests/test_jwt_flow.py` → Vitest (token válido, inválido, expirado, inactivo, flujo de creación de usuario)
- [ ] Port de `tests/test_track_flow.py` → Vitest (CRUD completo de track con supertest)
- [ ] Tests e2e de paridad por módulo (artists/albums/genres/activities)
- [ ] README del proyecto: puesta en marcha, usuarios demo, tabla de endpoints
- [ ] Checklist final de §1.4 (30 rutas) firmado
- [ ] Actualizar memoria de proyectos (`MEMORIA_PROYECTOS`)

---

## 4. Fuera de alcance (dejar explícito)

- Migración de datos: no aplica (misma BD).
- Endpoints de Chinook no expuestos por el fuente (`Customer`, `Employee`, `Invoice`, `Playlist`).
- Refresh tokens (el fuente los descartó en `fases.md`).
- Despliegue / Docker / CI.
- `@nestjs/observe`: opcional, sin credenciales queda desactivado (no tocar el manejo actual).

---

## 5. Registro de trabajo

<!-- Append nuevas notas con fecha: qué se hizo, qué se verificó, decisiones tomadas. -->

- **2026-10-05**: plan creado. Hallazgo principal: **el fuente tiene los 5 tests en roto** por el `NameError` en `login_for_access_token` + `read_users` sin cuerpo (§1.1). §0 pasó a tablas para marcar la elección.
- **2026-10-05 (decisiones)**: pendiente de marcar — se asume la 🌟 mientras no se indique lo contrario.
