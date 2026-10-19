--description: SDD · Nuevo requisito: primero spec, después código (uso: /sdd-change 002-nombre requisito)
agent: planner
--
NO escribas código. Este es el único camino válido para cambiar lo que se implementa.

Spec: `specs/$1/spec.md`
Requisito nuevo o modificado: `$ARGUMENTS`

1. Agregá o modificá el/los RF correspondiente(s) en EARS, su criterio de aceptación
   y su caso límite. Marcaste como `borrador` hasta mi aprobación.
2. Regenerá el impacto: actualizá `plan.md` y agregá/ajustá las tareas en `tasks.md`
   (las tareas ya hechas que el cambio toque vuelven a `[ ]`).
3. Actualizá `MEMORY.md` con la decisión y su porqué.
4. **PARA**: no se toca código hasta que la spec esté `aprobada`.
