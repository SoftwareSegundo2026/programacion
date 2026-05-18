# Guía de implementación de JWT para `fastAPI-example`

Este documento describe cómo integrar la autenticación JWT en el proyecto actual de FastAPI.
Está basado en el código que ya existe en el repositorio, así que el objetivo es conectar las piezas que ya están allí en lugar de introducir una arquitectura nueva de autenticación.

## Estado actual

El proyecto ya incluye los helpers centrales de JWT:

- `app/core/security.py` ya tiene `create_access_token`, `verify_password` y `get_password_hash`.
- `app/core/config.py` ya define `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` y `API_V1_STR`.
- `pyproject.toml` ya incluye `python-jose[cryptography]` y `passlib[bcrypt]`.
- `app/api/dependencies.py` sigue siendo mínima, así que es el lugar natural para agregar dependencias relacionadas con auth.

Eso significa que la parte que falta es la capa de integración: esquemas de token, endpoint de login, dependencia de usuario actual y rutas protegidas.

## Flujo recomendado

1. Un usuario envía sus credenciales a un endpoint de login.
2. El servidor verifica la contraseña con `verify_password`.
3. Si las credenciales son válidas, el servidor crea un JWT con `create_access_token`.
4. El cliente envía el token en `Authorization: Bearer <token>`.
5. Los endpoints protegidos validan el token y cargan al usuario actual.

## Archivos involucrados

- `app/core/security.py`
- `app/core/config.py`
- `app/api/dependencies.py`
- `app/api/v1/router.py`
- `app/*/router.py` para recursos protegidos como artistas, álbumes y géneros

## Qué implementar

### 1. Esquemas de token y usuario

Crea esquemas para el flujo de autenticación, normalmente en un módulo nuevo como `app/core/schemas.py` o en un `app/auth/schemas.py` dedicado, si prefieres mantener auth separado.

Modelos sugeridos:

- `Token` con `access_token` y `token_type`
- `TokenData` con el subject decodificado, normalmente `sub` o `username`
- `UserLogin` o `UserCredentials` opcional para el cuerpo de la solicitud de login

### 2. Endpoint de login

Agrega un router de auth que exponga un endpoint de login.

Responsabilidades:

- Recibir username y password.
- Buscar al usuario en la base de datos.
- Verificar la contraseña.
- Generar un token con un tiempo de expiración.
- Devolver el token con una forma de respuesta estándar.

Ejemplo de respuesta esperada:

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

### 3. Dependencia de usuario actual

Usa `app/api/dependencies.py` para agregar helpers como:

- `oauth2_scheme = OAuth2PasswordBearer(tokenUrl=...)`
- `get_current_user`
- `get_current_active_user` si quieres soportar usuarios deshabilitados

Esta dependencia debería:

- Leer el Bearer token desde la request.
- Decodificarlo con `jwt.decode`.
- Validar la firma usando `SECRET_KEY` y `HS256`.
- Verificar la expiración del token.
- Cargar el usuario referenciado desde la base de datos.

### 4. Proteger rutas

Una vez que exista la dependencia, aplícala a las rutas que deban requerir autenticación.

Opciones típicas:

- Proteger handlers individuales con `Depends(get_current_user)`.
- Proteger un router completo inyectando la dependencia a nivel de router.

### 5. Configuración

Mantén la configuración de los tokens en variables de entorno y deja que `app/core/config.py` las lea.

Configuración mínima:

- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

Práctica recomendada:

- Usa un `SECRET_KEY` largo y aleatorio en producción.
- Mantén la vida útil del token lo suficientemente corta para reducir riesgos.
- Carga los secretos desde `.env` en local y desde la plataforma de despliegue en producción.

## Forma sugerida del código

El helper existente `create_access_token` puede quedarse en `app/core/security.py`, pero el flujo de login debería pasar un payload que incluya el campo de identidad, normalmente `sub`.

Ejemplo de payload:

```python
data = {"sub": user.email}
token = create_access_token(data)
```

Después, la dependencia protegida debería recuperar ese mismo campo desde el token decodificado.

## Checklist por fases

El checklist de seguimiento se movió a [fases.md](fases.md).

## Notas prácticas

- `create_access_token` ya usa 15 minutos por defecto cuando no se pasa expiración, pero la configuración del proyecto actualmente establece `ACCESS_TOKEN_EXPIRE_MINUTES` en 30. Elige una única fuente de verdad y úsala de forma consistente.
- Si planeas agregar refresh tokens más adelante, mantén los access tokens de vida corta y almacena los refresh tokens por separado.
- Si tu modelo de usuario todavía no está listo, igual puedes implementar primero la infraestructura JWT y conectar la búsqueda en base de datos después.

## Próximo paso recomendado

Implementa primero la capa de dependencias de auth, porque es el cambio más pequeño que habilita rutas protegidas en toda la API.
