# TP-3 · Motor de búsqueda y paginación (NestJS)

**Asignatura:** Programación · **Modalidad:** individual
**Cronograma:** Clase 5 (15/06) — *modelado y relaciones* · Clase 6 (22/06) — *Proyecto 2: Motor de Búsqueda*
**Requisito previo:** TP-1 aprobado
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Implementar búsqueda con **filtros combinados** sobre varias tablas (JOINs), con
paginación y ordenamiento, tomando decisiones de contrato que el reviewer va a
exigir estén **en la spec** y no improvisadas en el código.

## Alcance

1. **Spec aprobada** en `specs/003-busqueda/spec.md`.
2. **Filtros combinados por query params** sobre al menos 2 recursos con relación
   (ej. tracks: texto, género, artista, rango de precio y duración).
3. **Ordenamiento** por campo whitelist (nunca por campo arbitrario del cliente).
4. **Paginación** con metadatos: `total`, `skip`, `limit`, `hasMore`.
5. **Eficiencia:** consultas paginadas en la base (no cargar todo y filtrar en memoria),
   índices sobre los campos filtrados, y evidencia de ello (plan de consulta o descripción).
6. **Documentación** de todos los query params en la API.
7. **Suite en verde** con los 4 gates.

## Decisiones que la spec debe obligar a tomar

Esto es lo que separa un TP aprobado de uno devuelto:

| Pregunta | Por qué importa |
|---|---|
| ¿Filtro que no matchea nada? | 200 con lista vacía ≠ 404 |
| ¿`limit=999999`? | Hay tope, o la spec dice explícitamente que no lo hay |
| ¿`sort=campo_hackers`? | Whitelist de campos, si no → 400 |
| ¿`skip` negativo o no numérico? | 400, validado antes de llegar al repository |
| ¿Texto con `%`, `_`, `'` o acentos? | Se parametriza: **cero** concatenación de SQL |
| ¿Sin ningún filtro? | ¿Devuelve todo paginado o pide al menos uno? |

## Casos límite con test obligatorio

- Sin coincidencias → 200 y `[]` (con metadatos en 0).
- `skip` mayor que el total → 200 y `[]`, no error.
- Combinación de los 5 filtros a la vez.
- Orden inválido y orden por campo inexistente → 400.
- Caracteres especiales y SQL injection en el parámetro de texto.
- Relación vacía (track sin género) → no desaparece de los resultados cuando no se filtra por género.

## Fuera de alcance

- Búsqueda full-text (tsvector, ElasticSearch, Meilisearch).
- Autenticación con roles (TP-2).
- Búsqueda por voz/imágenes, sugerencias y "fuzzy".

## Flujo esperado

```bash
/sdd-spec 003-busqueda → /sdd-clarify → /sdd-plan → /sdd-tasks
/sdd-implement 003-busqueda T1 … Tn
/sdd-validate 003-busqueda
```

## Criterios de evaluación

Los de la rúbrica estándar, más:

- Cada decisión de la tabla anterior está **justificada en la spec**, no en un comentario del código.
- Ninguna consulta arma SQL concatenando el valor del query param.
- Los metadatos de paginación son consistentes en todos los recursos.
