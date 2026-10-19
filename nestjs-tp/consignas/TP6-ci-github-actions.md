# TP-6 · CI con GitHub Actions (NestJS)

**Asignatura:** Programación · **Modalidad:** individual (en el repo del TP-1)
**Cronograma:** Clase 15 (07/09) — *cultura DevOps y CI* · Clase 16 (14/09) — *workflows, jobs y steps* · Clase 17 (21/09) — *pipelines de CI reales*
**Requisito previo:** TP-1 y TP-5 (sin suite en verde no hay CI que valga)
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Convertir los gates de la constitution (`lint · build · test · test:e2e`) en
**condiciones de merge automáticas**: que sea físicamente imposible integrar
código que no pase la verificación.

## Alcance

1. **Spec aprobada** en `specs/006-ci/spec.md` — los requisitos son de proceso,
   no de código: `CUANDO se abre un pull request, EL SISTEMA ejecuta… SI falla,
   ENTONCES el merge queda bloqueado`.
2. **Workflow de CI** (`.github/workflows/ci.yml`) con, como mínimo:
   - *trigger* `on: pull_request` y `on: push` a la rama principal,
   - instalación de dependencias con **cacheo** de pnpm,
   - los 4 gates como pasos separados (que se vea cuál falló),
   - reporter de cobertura o artefacto de log.
3. **Rama principal protegida** con *required status checks* (configuración del repo).
4. **Protección de secretos:** ninguna credencial real en el workflow ni en el repo;
   las que se usan van en *repository secrets* con nombres claros.
5. **Evidencia de bloqueo:** un PR deliberadamente rojo que **no** pudo mergear,
   adjunto como captura o link en la documentación.
6. La suite sigue en verde: `pnpm lint && pnpm build && pnpm test && pnpm test:e2e`.

## Casos límite / situaciones con test o evidencia

- Test rojo → el check queda rojo y el merge está bloqueado.
- PR que solo toca docs → igual corre el pipeline (o se muestra la condición opt-in).
- Dependencias con cache → segunda corrida más rápida (log como evidencia).
- Workflow sin permisos de escritura innecesarios (`permissions:` explícito).
- Fork de un PR externo → los secretos **no** se exponen.

## Fuera de alcance

- Deploy a producción (TP-7).
- Matriz de múltiples versiones de Node (extra, opcional).
- SonarQube / análisis estático de pago.

## Flujo esperado

```bash
/sdd-spec 006-ci → /sdd-plan 006-ci → /sdd-tasks 006-ci
/sdd-implement 006-ci T1 … Tn
/sdd-validate 006-ci
```

## Criterios de evaluación

- El pipeline corre los **mismos comandos** que la constitution (no comandos distintos).
- El PR rojo bloqueado es verificable por cualquiera, no solo por quien lo hizo.
- El YAML está comentado en español: cada *job* y cada *step* explica qué valida.
- Ningún archivo contiene tokens, contraseñas o `.env` real.
