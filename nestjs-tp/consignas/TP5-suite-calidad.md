# TP-5 · Suite de calidad: TDD y contrato sobre un TP existente

**Asignatura:** Programación · **Modalidad:** individual
**Cronograma:** Clase 11 (10/08) — *Calidad y unit testing (TDD)* · Clase 12 (17/08) — *API testing y automatización*
**Requisito previo:** TP-1 funcional (es el código sobre el que se trabaja)
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

No se escribe funcionalidad nueva: se **endurece** el TP-1. El entregable es una suite que
demuestre que el sistema se puede cambiar sin miedo: cobertura medible, TDD
aplicado a bugs reales y un contrato de API verificado de punta a punta.

## Alcance

1. **Spec aprobada** en `specs/005-calidad/spec.md` — acá la spec documenta la
   **calidad exigida** como requisitos no funcionales verificables:
   - `RF: SI la cobertura de líneas baja de X%, ENTONCES el gate falla`.
   - `RF: CUANDO un endpoint cambia su respuesta, EL contrato lo detecta`.
2. **Gate de cobertura** configurado (`pnpm test:cov` con umbral declarado y
   que efectivamente interrumpe el proceso si baja).
3. **TDD aplicado a 3 bugs reales:** primero el test que reproduce el bug (rojo),
   después el fix (verde), después el commit. Cada bug con su nota en `MEMORY.md`.
4. **Refactor con red de seguridad:** una pieza de lógica refactorizada donde la
   cobertura **no baja** y los tests no se tocaron.
5. **Colección de contrato** ejecutable desde CI (`pnpm test:e2e` o CLI):
   happy path + errores de cada endpoint, con códigos de estado esperados.
6. **Suite en verde** con los 4 gates.

## Bugs candidatos (buscar en el propio TP-1)

Los que suelen aparecer: respuesta `null` con 200 en vez de 404, `PATCH` que borra
campos no enviados, paginación que devuelve `total` inconsistente, delete que deja
huérfanos, validación que acepta string vacío.

## Fuera de alcance

- Tests de carga/rendimiento (k6, Artillery).
- Tests E2E de frontend.
- Mutación testing (opcional, extra).

## Flujo esperado

```bash
/sdd-spec 005-calidad → /sdd-plan 005-calidad → /sdd-tasks 005-calidad
/sdd-implement 005-calidad T1 … Tn     # cada bug = una tarea
/sdd-validate 005-calidad
```

## Criterios de evaluación

Los de la rúbrica estándar, más:

- El umbral de cobertura está declarado **en la constitution o en la spec**, no en un archivo olvidado.
- Los 3 bugs tienen evidencia: test que falla antes del fix y pasa después
  (verificable con `git log -p`, no con palabras).
- Ninguna tarea de este TP bajó la cobertura.
- La colección de contrato se puede correr en una máquina limpia con un comando.
