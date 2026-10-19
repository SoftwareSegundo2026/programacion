--description: SDD · Implementa UNA tarea con tests primero (uso: /sdd-implement 002-nombre T3)
agent: implementer
--
Implementá **UNA sola tarea**: `$2` de `specs/$1/tasks.md`. No rediseñes el plan y no
empieces la siguiente tarea.

Pasos obligatorios:
1. Leé `tasks.md`, `plan.md`, `spec.md`, `docs/constitution.md`, `MEMORY.md` y la skill `nestjs-esm`.
   Si la tarea no está marcada como pendiente o falta alguna fase previa aprobada, **PARA**.
2. **Tests primero**: escribí los tests en rojo y ejecutá `pnpm test` para verlos fallar.
3. Escribí el código mínimo hasta que pasen.
4. Gates: `pnpm lint && pnpm build && pnpm test` y, si toca un endpoint, `pnpm test:e2e`.
   **Prohibido** marcar la tarea con los gates en rojo o comentarios puestos para que pasen.
5. Un solo commit: `Tn: <descripción>`.
6. Marcá `[x]` en `tasks.md`, actualizá `MEMORY.md` y **PARA**.
