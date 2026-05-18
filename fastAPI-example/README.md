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

## Variables de entorno

Configura como mínimo estas variables en `.env`:

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `API_V1_STR`

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
