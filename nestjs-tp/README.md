# nestjs-tp — Starter de Spec-Driven Development para los TPs de NestJS

Material de la asignatura **Programación** para desarrollar los Trabajos Prácticos de
backend con NestJS siguiendo la metodología **SDD + multiagentes** de
`/home/dcazabat/Documentos/Cursos/DevelopAI/` (guías `GUIA-OPENCODE.md` y `GUIA-HERMES.md`).

> **Regla de oro:** la IA ejecuta, pero el responsable del proyecto sos vos.
> La spec manda: nada se implementa si no está en la spec aprobada.

---

## Cómo arrancar

Este repo es un **arnés**, no una app. Se superpone sobre un proyecto NestJS:

```bash
# 1. Base de código (o crear desde cero con `nest new`)
cp -r ../nestjs-music ~/mi-tp

# 2. Copiar el arnés SDD encima
cp -r nestjs-tp/. ~/mi-tp/          # AGENTS.md, MEMORY.md, docs/, .opencode/, .agents/

# 3. Abrir OpenCode dentro del proyecto
cd ~/mi-tp && opencode
```

Verificación mínima de que el arnés quedó bien: `/skills` muestra `sdd` y
`nestjs-esm`, `/agents` muestra `coordinator`, `planner`, `implementer` y
`reviewer`, y `pnpm test` corre.

---

## Qué hay en esta carpeta

| Ruta | Qué es | Quién lo usa |
|---|---|---|
| `AGENTS.md` | Instrucciones del proyecto (stack, comandos, límites). Máx. 40 líneas. | Agente (siempre) |
| `MEMORY.md` | Memoria entre sesiones: estado, decisiones, próximos pasos. | Agente, tras cada tarea |
| `docs/constitution.md` | 6 principios innegociables. Toda spec/plan/tarea debe cumplirlos. | Planner y reviewer |
| `.opencode/agents/` | Los 4 agentes: `coordinator`, `planner`, `implementer`, `reviewer`. | Coordinación |
| `.opencode/commands/` | Comandos `/sdd-*` que automatizan el flujo. | Alumno / docente |
| `.agents/skills/` | Skills `sdd` (el flujo) y `nestjs-esm` (trampas del stack). | Agente, al cargarlas |
| `specs/000-ejemplo-chinook/` | Spec, plan y tareas **de referencia** ya resueltos. | Modelo a imitar |
| `consignas/` | Consignas TP-1 a TP-8 + índice con recorrido sugerido. | Alumno |
| `rubrica/` | Rúbrica de entrega + comando de validación para el docente. | Docente |

---

## El flujo, en una línea

```
/sdd-constitution → /sdd-spec → /sdd-clarify → /sdd-plan → /sdd-tasks
                                                            ↓
              /sdd-validate ← /sdd-implement T1, T2, T3… (una tarea por vez)
```

**Nunca** se pasa a la fase siguiente sin la aprobación explícita del usuario.
Cada fase deja un artefacto en disco (`specs/NNN-*`), que es lo que se evalúa.

---

## Adaptaciones a NestJS (importante)

La guía DevelopAI de referencia está pensada en JS puro con `node --test`. En este
TP se reemplaza el gate por el del repo:

| En la guía | Acá |
|---|---|
| `node --test` | `pnpm test` (unit) + `pnpm test:e2e` (e2e con supertest) |
| Sin linter | `pnpm lint` (oxlint type-aware) + `pnpm format` (prettier) |
| Sin build | `pnpm build` debe pasar antes de cerrar una tarea |

Todo eso ya está reflejado en `AGENTS.md`, `docs/constitution.md`, la skill `sdd`
y los comandos `/sdd-implement` y `/sdd-validate`.

---

## Entregables por TP

1. `specs/NNN-<nombre>/spec.md` — QUÉ y POR QUÉ (HU + requisitos en EARS), aprobada.
2. `specs/NNN-<nombre>/plan.md` — CÓMO (archivos, capas, estrategia de tests).
3. `specs/NNN-<nombre>/tasks.md` — tareas de 20-30 min con **"Hecho cuando:"**.
4. Historial git: **un commit por tarea** marcada en `tasks.md`.
5. `MEMORY.md` actualizado al cierre de cada tarea.
6. Suite en verde: `pnpm lint && pnpm build && pnpm test && pnpm test:e2e`.

Ver detalles y pesos en [`rubrica/rubrica-entrega.md`](rubrica/rubrica-entrega.md).
