--description: Planifica una nueva funcionalidad antes de tocar código
agent: planner
--
Quiero añadir esta funcionalidad: `$ARGUMENTS`

Antes de escribir código, prepará un plan con:
1. Cómo se implementa, respetando `docs/constitution.md` y `AGENTS.md`.
2. Qué archivos se modifican y qué cambia en cada uno.
3. Los casos límite y las dudas que tengo que decidir **yo** antes de empezar.
4. Qué tocaría actualizar en `AGENTS.md` y `MEMORY.md`.

Tené en cuenta el estado actual del proyecto: `MEMORY.md`
y la spec activa en `specs/`.

**No modifiques ningún archivo** hasta que apruebe el plan.
Si la funcionalidad no está cubierta por ninguna spec aprobada, avisámelo y
proponé correr `/sdd-change`.
