--description: SDD · Divide el plan en tareas (uso: /sdd-tasks 002-nombre)
agent: planner
--
NO escribas código. Leé `MEMORY.md` y la skill `sdd`.

Plan: `specs/$1/plan.md` — verificá que exista y que `spec.md` esté aprobada.

Generá `specs/$1/tasks.md` con:
- **Máximo 10 tareas**, en orden de dependencia.
- Formato: `- [ ] **Tn. <Descripción>.** RF-x, RF-y` + una línea `Hecho cuando: <comprobación verificable con un comando>`.
- Duración estimada de **20-30 min** por tarea. Si una tarea es más grande, partila.
- Los tests de una tarea van **antes** (o junto) al código que los necesita.
- Cada tarea mapea al menos un RF de la spec.

Mostrá las tareas y **PARA** a esperar mi aprobación para entrar en implementación.
