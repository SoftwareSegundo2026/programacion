--description: SDD · Revisa la spec como QA, solo detecta (uso: /sdd-clarify 002-nombre)
agent: reviewer
--
NO escribas código ni modifiques **ningún** archivo: tu salida es únicamente un informe.

Spec a revisar: `specs/$1/spec.md`
Reglas del proyecto: `docs/constitution.md`

Revisala como QA y devolvé **solo detección**, sin proponer soluciones:
1. Ambigüedades (requisitos interpretables de más).
2. Contradicciones entre requisitos o contra la constitution.
3. Casos límite no cubiertos (ids inexistentes, duplicados, vacíos, concurrentes, no autorizado).
4. Conflictos con `docs/constitution.md`.
5. RF sin criterio de aceptación y dudas todavía marcadas `[NECESITA ACLARACIÓN]`.

Terminá con `VEREDICTO: APROBADA` o `VEREDICTO: CAMBIOS NECESARIOS`.
