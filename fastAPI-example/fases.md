# Fases de implementación JWT

## Fase 0 - Definición y base

- [x] Alinear el campo de identidad del JWT (`sub`).
- [x] Definir una sola fuente de verdad para la expiración: `ACCESS_TOKEN_EXPIRE_MINUTES`.
- [x] Cargar `SECRET_KEY` y la expiración desde `.env`.

## Fase 1 - Contrato y esquemas

- [x] Crear `Token` con `access_token` y `token_type`.
- [x] Crear `TokenData` para representar el `sub` decodificado.
- [x] Crear el esquema de login (`UserLogin` o `UserCredentials`).

## Fase 2 - Emisión del token

- [x] Agregar el router de auth.
- [x] Implementar el login: recibir credenciales, validar la contraseña y buscar el usuario.
- [x] Emitir el JWT con `create_access_token`.
- [x] Responder con `{ "access_token": "...", "token_type": "bearer" }`.

## Fase 3 - Validación y dependencias

- [x] Agregar `OAuth2PasswordBearer` en `app/api/dependencies.py`.
- [x] Implementar `get_current_user`.
- [x] Agregar `get_current_active_user` si el modelo de usuario tiene estado activo/inactivo.
- [x] Verificar firma y expiración con `jwt.decode`.

## Fase 4 - Protección de rutas

- [x] Proteger al menos un endpoint existente con `Depends(get_current_user)`.
- [x] Proteger un router completo si el flujo ya está estable.
- [x] Confirmar que las solicitudes sin token devuelven `401`.

## Fase 5 - Verificación y cierre

- [x] Probar token válido.
- [x] Probar token expirado.
- [x] Probar credenciales incorrectas.
- [x] Documentar las variables de entorno necesarias en `.env` o en `README.md`.

## Seguimiento futuro

- [x] Definir si habrá refresh tokens. Se dejan fuera de esta iteración.
- [x] Revisar si conviene separar auth en un módulo dedicado (`app/auth/`).
- [x] Registrar cualquier cambio pendiente en los routers protegidos.
