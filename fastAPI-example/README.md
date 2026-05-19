# fastAPI-example

Ejemplo de API en FastAPI con autenticación JWT y recursos CRUD para artistas, álbumes y géneros.

## Autenticación

Endpoint de login:

- `POST /api/v1/auth/token`

Ejemplo de cuerpo:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta esperada:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Usuarios de demostración:

- `admin` / `admin123`  
- `reader` / `reader123`  

`reader` está marcado como inactivo para validar la protección con `get_current_active_user`.

Endpoints de administración de usuarios:

- `GET /api/v1/users`
- `POST /api/v1/users`

Ambos requieren un `Bearer token` válido. `POST /api/v1/users` crea un usuario nuevo con contraseña hasheada en la base de datos.

## Swagger UI

Abre `GET /docs`, pulsa `Authorize` y pega el `access_token` obtenido en el login.
El esquema de seguridad aparece como `bearerAuth`, así que Swagger enviará el token como Bearer en las rutas protegidas.

## Logs

El flujo de `GET /api/v1/artists/` escribe trazas numeradas y descriptivas en consola y en `./instance/fastapi-example.log` cuando `LOG_LEVEL=DEBUG`.
Cada línea indica la función, la tarea y si el paso recibe o no token JWT.

## Variables de entorno

Configura como mínimo estas variables en `.env`:

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `API_V1_STR`
- `LOG_FILE_PATH`
- `LOG_LEVEL`

Puedes copiar el archivo [`.env.example`](.env.example) a [`.env`](.env) y ajustar el secreto antes de ejecutar la app.

## Verificación

Para ejecutar la verificación JWT incluida en el repositorio:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

La suite cubre:

- credenciales válidas,
- credenciales incorrectas,
- token expirado,
- acceso de usuario inactivo.
