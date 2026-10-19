--description: SDD · Estado actual: fase y siguiente paso (uso: /sdd-status 002-nombre)
agent: coordinator
--
NO escribas ni modifiques ningún archivo. Solo lectura.

Leé `specs/$1/` (`spec.md`, `plan.md`, `tasks.md`), `MEMORY.md` y `git log --oneline -10`.
Respondé en este orden:

1. **Fase actual** del flujo SDD (spec / clarify / plan / tareas / implementación / validación / cierre).
2. **Aprobaciones**: qué fase está aprobada y cuál espera aprobación.
3. **Tareas**: hechas vs. pendientes, con la siguiente a ejecutar.
4. **Gates**: estado de `pnpm lint`, `pnpm build`, `pnpm test`, `pnpm test:e2e` si se puede ejecutar.
5. **Siguiente paso exacto**, con el comando a correr.
