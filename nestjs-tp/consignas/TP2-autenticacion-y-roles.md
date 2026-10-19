# TP-2 · Autenticación y autorización con roles (NestJS)

**Asignatura:** Programación · **Modalidad:** individual (equipo opcional para la defensa)
**Cronograma:** Clase 7 (29/06) — *Seguridad y criptografía* · Clase 21 (26/10) — Sprint 2, secretos y auth
**Requisito previo:** TP-1 aprobado (la auth se monta sobre ese catálogo)
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Proteger el catálogo del TP-1 con autenticación JWT y autorización por roles,
demostrando que la seguridad es un **requisito más de la spec** y no un parche
agregado al final.

## Alcance

1. **Spec aprobada** en `specs/002-auth-roles/spec.md`, con foco en casos límite.
2. **Registro y login** con JWT firmado y expiración configurable por `.env`.
3. **Contraseñas:** hash con salt (bcrypt o argon2). **Nunca** texto plano, nunca
   devuelto en ninguna respuesta.
4. **Guards:** `AuthGuard` global por defecto + `RolesGuard` con roles
   (`admin` / `viewer`) declarados por decorador en los endpoints.
5. **Endpoint público único:** el login. Todo lo demás exige token, salvo que
   esté declarado como público explícitamente.
6. **Secretos:** `.env` (gitignored) + `.env.example` commiteable. Ninguna clave
   en el repo, ningún token hardcodeado.
7. **Suite en verde** con los 4 gates.

## Casos límite obligatorios en la spec

Estos son los que el reviewer va a buscar uno por uno:

| # | Situación | Esperado |
|---|---|---|
| 1 | Login con contraseña incorrecta | 401, mensaje genérico (sin decir cuál falló) |
| 2 | Login con usuario inexistente | 401, mismo mensaje que el caso 1 |
| 3 | Usuario deshabilitado con token válido | 401 o 403, nunca 200 |
| 4 | Token expirado | 401 |
| 5 | Token con firma inválida / editado a mano | 401 |
| 6 | Sin header `Authorization` | 401 |
| 7 | Token válido pero rol insuficiente | 403 |
| 8 | Registro con username o email ya existente | 409 |
| 9 | Respuesta de login o de usuario | sin `hashedPassword`, sin `iat`/`exp` internos |
| 10 | Dos logins simultáneos | ambos responden, sin condición de carrera |

## Fuera de alcance

- Refresh tokens y rotación.
- OAuth / login con terceros.
- Recuperación de contraseña por email.

## Flujo esperado

```bash
/sdd-spec 002-auth-roles        # → aprobación
/sdd-clarify 002-auth-roles     # el reviewer revisa los 10 casos límite
/sdd-plan 002-auth-roles        # → aprobación
/sdd-tasks 002-auth-roles       # → aprobación
/sdd-implement 002-auth-roles T1   # … hasta Tn, una por vez
/sdd-validate 002-auth-roles
```

## Preguntas que la spec debe responder antes de escribir código

El comando `/sdd-spec` hace **5 preguntas como máximo**. Entre las esperadas:

1. ¿El rol se decide por decorador en el controller o por tabla en la base?
2. ¿Cuánto vive el token (minutos)? ¿Se configura por `.env`?
3. ¿Los usuarios del catálogo son los mismos que los del login, o es una tabla aparte?
4. ¿Qué pasa al editar un usuario: se puede cambiar su propio rol desde la API?
5. ¿El endpoint de registro es público o solo lo crea un admin?

Si el alumno responde estas preguntas **sin pasar por la spec**, la clarificación
le va a devolver la spec con `VEREDICTO: CAMBIOS NECESARIOS`.

## Criterios de evaluación

Mismos ítems que el TP-1, más:

- Los 10 casos límite tienen test automatizado que los comprobra.
- Ninguna clave o token aparece en `git log`.
- Los endpoints de escritura quedan protegidos **por defecto** (el que olvida
  decorar un endpoint lo descubre con un test de regresión, no en producción).
