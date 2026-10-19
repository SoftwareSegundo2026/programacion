# Rúbrica de entrega — TP de NestJS (SDD)

**Total: 100 puntos.** Escala 0-10 en cada ítem, multiplicada por su peso.
Se evalúan **artefactos en disco + gates ejecutados**, no la demo.

| # | Ítem | Peso | Qué se verifica | Cómo se verifica |
|---|---|:---:|---|---|
| 1 | **Spec** | 15 | HU completas; RF en EARS comprobables; casos límite; "fuera de alcance"; dudas resueltas; sin menciones de stack | Lectura de `specs/NNN/spec.md` + veredicto de `/sdd-clarify` |
| 2 | **Plan y tareas** | 10 | Mapeo RF ↔ tareas; "Hecho cuando:" con comando; ≤ 10 tareas; 20-30 min c/u; tests antes que el código | Lectura de `plan.md` y `tasks.md` |
| 3 | **Implementación** | 35 | Un commit por tarea; código en el orden de las tareas; capas respetadas; TS estricto; sin código fuera de la spec | `git log`, `git diff`, inspección de código |
| 4 | **Tests y gates** | 20 | Cada RF cubierto por ≥ 1 test; unit + e2e; los 4 gates en verde | Ejecución en el repo del docente |
| 5 | **Proceso SDD** | 10 | Fases aprobadas en orden (nada saltado); `MEMORY.md` actualizado por tarea; `/sdd-validate` con `VEREDICTO: APROBADO` | Historial de specs + `MEMORY.md` |
| 6 | **Demo y defensa** | 10 | Explica QUÉ vs CÓMO, justifica decisiones contra la constitution, responde un cambio de requisito con `/sdd-change` | Defensa oral (~10 min) |

## Gates (condición necesaria, no puntaje)

Ninguna entrega se corrige si alguno falla:

```bash
pnpm lint
pnpm build
pnpm test
pnpm test:e2e
```

## Puntos que restan

| Situación | Penalización |
|---|---|
| Tarea marcada `[x]` con un gate en rojo | −10 por tarea |
| Test borrado o comentado para que pase | −15 (y se anula el ítem 4) |
| Fase saltada sin aprobación | −10 por fase |
| Código que no está en la spec (`/sdd-change` no usado) | −10 por requisito |
| `.env` o secretos commiteados | ítem 4 = 0 |
| Uso de `any` / `@ts-ignore` sin justificación | −3 por ocurrencia |
| `MEMORY.md` sin actualizar al cierre | −5 |

## Escala de participación individual (proyectos de grupo)

Para el Proyecto Integrador se aplica la misma rúbrica sobre el **artefacto del
grupo** y se pondera con la contribución individual:

- Commits propios con mensaje de tarea → visibility de quién hizo qué.
- Specs/planes/tareas editados por el alumno → aporte de requisitos, no solo código.
- Un alumno sin commits **ni** sin aportes a specs queda con el ítem 3 en 0.

Esta regla existe porque los informes de la materia detectaron alumnos con
**0 commits** en repositorios grupales.
