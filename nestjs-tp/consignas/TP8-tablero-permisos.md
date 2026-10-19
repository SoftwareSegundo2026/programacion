# TP-8 · Tablero de tareas con permisos (NestJS) — *optativo / Proyecto 5*

**Asignatura:** Programación · **Modalidad:** binaria o ternaria
**Cronograma:** consolidación (Clase 14, 31/08) o como preparación del Proyecto Integrador (Clase 19, 19/10)
**Requisito previo:** TP-1 y TP-2 (este TP los integra)
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Backend tipo Trello (tableros, listas, tarjetas, miembros) donde lo que se
practica es **manejar un dominio grande sin romper el flujo SDD**: varias specs
encadenadas, roles y permisos, y auditoría de quién hizo qué.

A diferencia de los anteriores, este TP **no cabe en una spec**: obliga a partir
el trabajo en specs encadenadas respetando el límite de 10 tareas por spec.

## Alcance

| Spec | Contenido |
|---|---|
| `specs/008-tableros` | Tableros y listas: CRUD, propiedad, miembros |
| `specs/008-tarjetas` | Tarjetas: crear, mover entre listas, orden, etiquetas, checklist |
| `specs/008-permisos` | Roles (`owner` / `member` / `viewer`), invitaciones y authorization center |
| `specs/008-auditoria` | Quién hizo qué y cuándo (actividad), consultable por tablero |

Además:

- **Invitación a tablero** con estado pendiente/aceptada y expiración.
- **Movimiento de tarjeta entre listas** transaccional (posición + lista juntas).
- **Autorización centralizada:** un solo punto que decide (nunca `if (user.id === owner)`
  regado por todos los controllers).
- **Suite en verde** con los 4 gates.

## Casos límite con test obligatorio

- Usuario sin permiso sobre el tablero → 404 (no 403, para no revelar que existe) o 403
  **decidido en la spec** y consistente en todos los endpoints.
- `viewer` que intenta mover una tarjeta → 403.
- Mover una tarjeta a una lista de **otro** tablero → 409 o 404 según la spec.
- Borrar un tablero con tarjetas → la spec decide (borrado en cascada o 409) y lo prueba.
- Invitar a alguien ya miembro → 409.
- Dos movimientos simultáneos de la misma tarjeta → un orden consistente, sin posiciones duplicadas.
- Borrar la cuenta del owner del tablero → el tablero no queda huérfano (dueño alternativo o bloqueo, según spec).

## Fuera de alcance

- Tiempo real (websockets, colaboración simultánea en pantalla).
- Frontend.
- Adjuntos de archivos.

## Por qué este TP es el mejor "examen de la metodología"

- El dominio es grande ⇒ **hay que partir specs** y eso obliga a respetar
  "nada se implementa si no está en la spec activa".
- Tiene roles ⇒ obliga a que la autorización sea requisito de la spec y no un afterthought.
- Al ser binario/ternario, **la evidencia de contribución es el artefacto**:
  cada alumno debe poder señalar sus RF, sus tareas y sus commits.

## Flujo esperado (una vuelta completa por spec)

```bash
/sdd-spec 008-tableros → clarify → plan → tasks → implement → validate
# recién después:
/sdd-spec 008-tarjetas  → clarify → plan → tasks → implement → validate
# … y así con permisos y auditoría
```

## Criterios de evaluación

- Cada spec cerrada con `VEREDICTO: APROBADO` **antes** de arrancar la siguiente.
- La autorización implementada en un solo punto y testeada por endpoint.
- `MEMORY.md` narra el avance entre specs (qué cambió y por qué).
- Aportación individual visible: specs, tareas y commits por alumno.
