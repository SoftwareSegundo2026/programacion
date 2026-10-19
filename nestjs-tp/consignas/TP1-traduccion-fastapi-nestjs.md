# TP-1 · De FastAPI a NestJS: catálogo Chinook

**Asignatura:** Programación · **Modalidad:** individual
**Cronograma:** Clase 3 (01/06) — *Traducir un servicio de FastAPI a NestJS* · Clase 14 (31/08) — cierre de TPs
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Traducir el backend de ejemplo `Material-Clase/fastAPI-example` (Chinook: artistas,
álbumes, géneros y pistas) a **NestJS**, demostrando que la arquitectura en capas y
los patrones (Facade, DAO, DTO) son independientes del lenguaje.

> El punto de partida es `Material-Clase/nestjs-music`, que ya trae el andamio del
> módulo `albums` (controller/service/dto/entity), Vitest y `@nestjs/config`.

## Alcance

1. **Spec aprobada** en `specs/001-chinook-nest/spec.md` (el modelo es
   `specs/000-ejemplo-chinook/spec.md`).
2. **CRUD completo** de `artists`, `albums`, `genres` y `tracks`.
3. **Arquitectura obligatoria:** `controller` (solo HTTP) → `service` (lógica) →
   `repository` (DAO) → `dto/` validado.
4. **Respuestas enriquecidas:** un álbum trae el nombre de su artista; una pista
   trae título de álbum, género y tipo de medio.
5. **Paginación** con `skip`/`limit` y `limit` acotado.
6. **Códigos de estado correctos:** 200 / 201 / 204 / 400 / 401 / 404 / 409.
7. **Documentación** de la API generada y sincronizada con los endpoints reales.
8. **Suite en verde:** `pnpm lint && pnpm build && pnpm test && pnpm test:e2e`.

## Fuera de alcance

- Roles y permisos (va en el TP-2).
- Filtros de búsqueda complejos y full-text.
- Frontend.

## Flujo esperado

```bash
/sdd-constitution 001        # una sola vez por proyecto
/sdd-spec 001-chinook-nest   # → aprobación
/sdd-clarify 001-chinook-nest
/sdd-plan 001-chinook-nest   # → aprobación
/sdd-tasks 001-chinook-nest  # → aprobación
/sdd-implement 001-chinook-nest T1   # … hasta Tn, una por vez
/sdd-validate 001-chinook-nest
```

## Criterios de evaluación

| Ítem | Qué se mira |
|---|---|
| Spec | HU completas, RF en EARS, casos límite, sin dudas sin resolver |
| Plan y tareas | Mapeo RF ↔ tareas, "Hecho cuando:" verificable, ≤ 20-30 min c/u |
| Arquitectura | Ningún SQL ni regla de negocio en el controller; DTOs validados |
| Código | TypeScript estricto (sin `any`, sin `@ts-ignore`), imports ESM con `.js` |
| Tests | Cada RF cubierto por al menos un test; unit + e2e |
| Gates | Los 4 comandos en verde |
| Proceso | Un commit por tarea, `MEMORY.md` actualizado, sin fases saltadas |

Detalle de la rúbrica: [`../rubrica/rubrica-entrega.md`](../rubrica/rubrica-entrega.md).

## Puntos que el reviewer va a marcar (los que más se repiten)

- `GET /albums/:id` inexistente devolviendo `null` con 200 en vez de 404.
- Imports locales sin `.js` → build en verde y e2e que no arranca.
- DTO sin decoradores → la validación no existe aunque el DTO esté "definido".
- `limit` sin tope → el listado trae el catálogo entero.
- Test que solo verifica que no revienta, sin comprobar el RF.
