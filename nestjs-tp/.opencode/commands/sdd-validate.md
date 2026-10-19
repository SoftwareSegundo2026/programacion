--description: SDD · Valida la spec RF por RF (uso: /sdd-validate 002-nombre)
agent: reviewer
--
NO modifiques ningún archivo. Validá la implementación de `specs/$1/` contra su propia spec.

1. Leé `spec.md`, `plan.md`, `tasks.md`, `MEMORY.md`, `docs/constitution.md` y el
   historial (`git log`, `git diff`).
2. Ejecutá los gates: `pnpm lint`, `pnpm build`, `pnpm test`, `pnpm test:e2e`.
3. Recorré la spec **RF por RF**: para cada RF, indicá qué test lo cubre y su resultado.
   Un RF sin test que lo cubra **no está implementado**.
4. Verificá los criterios de finalización, que cada tarea hecha tenga su commit y que
   `MEMORY.md` esté actualizado.
5. Salida: **tabla RF → test → resultado** y luego, en la primera línea,
   `VEREDICTO: APROBADO` o `VEREDICTO: CAMBIOS NECESARIOS`.
