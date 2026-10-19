# Consignas de TPs — índice completo

Todos los TPs usan el mismo arnés SDD (`../README.md`) y la misma rúbrica
(`../rubrica/rubrica-entrega.md`). Lo que cambia es el dominio, el requisito del
cronograma que toca y el requisito previo.

## Publicados

| TP | Archivo | Cronograma | Requisito previo | Entrega clave |
|---|---|---|---|---|
| **TP-1** · De FastAPI a NestJS (Chinook) | [`TP1-traduccion-fastapi-nestjs.md`](TP1-traduccion-fastapi-nestjs.md) | Clase 3 (01/06) + 14 (31/08) | — | Spec + plan + tareas + CRUD + gates en verde |
| **TP-2** · Autenticación y roles | [`TP2-autenticacion-y-roles.md`](TP2-autenticacion-y-roles.md) | Clase 7 (29/06) + 21 (26/10) | TP-1 | JWT + guards + **10 casos límite** con test |
| **TP-3** · Motor de búsqueda y paginación | [`TP3-motor-busqueda.md`](TP3-motor-busqueda.md) | Clase 5 (15/06) + 6 (22/06) | TP-1 | Filtros combinados, JOINs, metadatos, decisión 200/400/404 |
| **TP-4** · Reservas con transacciones | [`TP4-reservas-transacciones.md`](TP4-reservas-transacciones.md) | Clase 13 (24/08) | TP-1 (TP-2 recomendado) | Atomicidad, rollback, **8 casos de concurrencia** |
| **TP-5** · Suite de calidad (TDD + contrato) | [`TP5-suite-calidad.md`](TP5-suite-calidad.md) | Clase 11 (10/08) + 12 (17/08) | TP-1 | Gate de cobertura + 3 bugs con TDD + colección de contrato |
| **TP-6** · CI con GitHub Actions | [`TP6-ci-github-actions.md`](TP6-ci-github-actions.md) | Clase 15 (07/09) + 16 (14/09) + 17 (21/09) | TP-1, TP-5 | Pipeline que bloquea el merge de un PR rojo |
| **TP-7** · Docker, CD y observabilidad | [`TP7-docker-cd-observabilidad.md`](TP7-docker-cd-observabilidad.md) | Clase 23 (09/11) + 24 (16/11) | TP-6 | Imagen multi-stage, healthcheck, CD y logs estructurados |
| **TP-8** · Tablero de tareas con permisos | [`TP8-tablero-permisos.md`](TP8-tablero-permisos.md) | Optativo · consolidación o Proyecto Integrador | TP-1, TP-2 | 4 specs encadenadas (dominio, tarjetas, permisos, auditoría) |

## Recorrido sugerido

```
TP-1  ──►  TP-2  ──┬──►  TP-3        (búsqueda)
                    ├──►  TP-4        (transacciones)
                    └──►  TP-5        (calidad)
                              │
                              ├──►  TP-6  ──►  TP-7
                              │
                              └──►  TP-8    (integrador optativo)
```

- **Camino mínimo** (para cerrar la cursada): TP-1 → TP-2 → TP-5 → TP-6.
- **Camino completo**: suma TP-3, TP-4 y TP-7.
- **TP-8** reemplaza al Proyecto Integrador si el grupo lo elige, o lo prepara.

## Proyecto Integrador (Clases 19-25)

El Proyecto Integrador **no es un TP aparte**: es el flujo SDD completo sobre el
dominio del grupo (cafetería, vehículos, restaurante, agro), con los sprints
mapeados a fases:

| Sprint | Clase | Fase SDD |
|---|---|---|
| Planning | 19 · 19/10 | `constitution.md` + spec inicial |
| 1 · Backend | 20 · 19/10 | `plan` + `tasks` + T1…Tn |
| 2 · Auth | 21 · 26/10 | spec de auth → implementación |
| 3 · Testing | 22 · 02/11 | `sdd-validate` RF por RF + cobertura |
| 4 · Docker/CI | 23 · 09/11 | gates como workflow de CI |
| 5 · CD | 24 · 16/11 | despliegue + observabilidad |
| Demo | 25 · 30/11 | Sprint Review sobre `MEMORY.md` y las specs |
