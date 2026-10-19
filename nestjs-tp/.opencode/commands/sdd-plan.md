--description: SDD · Genera el plan técnico (uso: /sdd-plan 002-nombre)
agent: planner
--
NO escribas código. Leé `AGENTS.md`, `MEMORY.md` y la skill `sdd`.

Spec: `specs/$1/spec.md` — verificá que su estado sea `aprobada`; si no lo es, negá la operación.

Generá `specs/$1/plan.md` con:
- Estructura de módulos NestJS a crear (`controller` → `service` → `repository` → `dto/`).
- Archivos que se crean o modifican, uno por uno.
- Decisiones técnicas y su porqué, siempre contra `docs/constitution.md`.
- Estrategia de tests: unitarios del service con el repository mockeado + e2e con supertest,
  indicando qué RF cubre cada tanda.
- Riesgos y casos límite a tener presentes.

Mostrá el plan y **PARA** a esperar mi aprobación antes de generar tareas.
