--description: SDD · Entrevista y genera la spec (uso: /sdd-spec 002-nombre idea)
agent: planner
--
NO escribas código en ningún momento. Leé `docs/constitution.md`, `MEMORY.md` y usá la skill `sdd`.

Carpeta de la spec: `specs/$1/`
Idea inicial: `$ARGUMENTS`

Tu trabajo:
1. Haceme preguntas de **UNA en UNA** para eliminar ambigüedades. Máximo 5 preguntas.
2. Con mis respuestas, generá `specs/$1/spec.md` con la plantilla de la skill `sdd`:
   contexto, usuarios, historias de usuario, requisitos funcionales **en EARS**,
   requisitos no funcionales, casos límite, fuera de alcance, criterios de finalización
   y dudas abiertas marcadas `[NECESITA ACLARACIÓN]`.
3. **Solo QUÉ y POR QUÉ**: nada de stack, arquitectura, librerías ni nombres de archivos.
4. Estado: `borrador`. PARA y esperá mi aprobación para pasarla a `aprobada`.
