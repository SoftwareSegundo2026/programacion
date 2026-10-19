# Tareas 000 — API de catálogo musical (Chinook)

> Archivo de **referencia**: respetá el formato (20-30 min, orden de dependencia,
> "Hecho cuando:" verificable con un comando, tests antes que el código).

Estado: pendiente · Plan: `specs/000-ejemplo-chinook/plan.md`

- [ ] **T1. Andamio del módulo `albums`.** RF-1
      Hecho cuando: `pnpm build` pasa y `GET /albums` responde `[]`.
- [ ] **T2. Tests e2e en rojo para lectura.** RF-1, RF-2
      Hecho cuando: `pnpm test:e2e` falla exactamente en los 2 tests de lectura y el resto ni corre.
- [ ] **T3. Lectura: listado paginado y por id con 404.** RF-1, RF-2, RF-8
      Hecho cuando: `pnpm test:e2e` pasa los tests de T2 y `pnpm test` sigue en verde.
- [ ] **T4. Tests en rojo para escritura.** RF-3, RF-4, RF-5, RF-6
      Hecho cuando: `pnpm test:e2e` marca en rojo crear, validación, patch y delete.
- [ ] **T5. DTOs de entrada con `class-validator` + `ValidationPipe` global.** RF-4
      Hecho cuando: `pnpm test:e2e` pasa el test de datos inválidos (400) y no hay `@ts-ignore`.
- [ ] **T6. Escritura: crear, patch parcial y delete.** RF-3, RF-5, RF-6
      Hecho cuando: `pnpm test:e2e` pasa todos los tests de escritura.
- [ ] **T7. Integridad referencial: no borrar artista con álbumes.** RF-9
      Hecho cuando: `pnpm test` tiene un test que verifica 409 y otro que verifica que el álbum siga existiendo.
- [ ] **T8. Gate de lectura sin credenciales.** RF-7
      Hecho cuando: `pnpm test:e2e` verifica 401 en POST/PATCH/DELETE sin token y 200 en GET.
- [ ] **T9. Repetir el patrón en `artists`, `genres` y `tracks`.** RF-1…RF-6
      Hecho cuando: `pnpm lint && pnpm build && pnpm test && pnpm test:e2e` quedan todos en verde.
- [ ] **T10. Cierre: documentación y memoria.** RNF-1, RNF-3
      Hecho cuando: la documentación refleja los endpoints reales y `MEMORY.md` quedó actualizado.

---

## Notas de referencia

- **Una tarea por llamada** a `/sdd-implement 000-ejemplo-chinook Tn`.
- Cada tarea cerrada = **un commit** (`Tn: <descripción>`).
- Ninguna tarea se marca `[x]` con los gates en rojo.
