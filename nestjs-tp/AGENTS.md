# AGENTS.md — TP NestJS (Asignatura Programación)

API REST con NestJS desarrollada con Spec-Driven Development. La spec manda.

## Stack y estructura
- NestJS 12 + TypeScript **ESM**: `"type": "module"`, los imports de archivos locales llevan `.js` (`./albums.service.js`).
- Gestor de paquetes: **pnpm**. Tests con **Vitest** (`vitest.config.ts` y `vitest.config.e2e.ts`).
- Un módulo por recurso en `src/<recurso>/`: `<recurso>.controller.ts`, `<recurso>.service.ts`, `<recurso>.module.ts`, `dto/` y `entities/`.
- Capas: `controller` (solo HTTP) → `service` (lógica de negocio) → `repository` (acceso a datos).

## Comandos
- Tests unit: `pnpm test`
- Tests e2e: `pnpm test:e2e`
- Lint y formato: `pnpm lint` y `pnpm format`
- Build: `pnpm build`
- Desarrollo: `pnpm start:dev`

## Convenciones
- Código en inglés; documentación, comentarios y textos visibles en español.
- Nombres descriptivos, sin siglas. Un archivo por clase principal.
- Cada endpoint se declara con su DTO de entrada y su DTO de salida.

## Reglas de dominio / trampas conocidas
- `nest start` NO carga el `.env`: solo lo hace `ConfigModule.forRoot()`. Nunca leas `process.env` antes de esa línea.
- `id` llega como `string`: convertir con `+id` o `ParseIntPipe`. Devolver 404 ante un id inexistente.
- Validación global con `ValidationPipe` en `main.ts`; un DTO sin decoradores no valida nada.
- Nunca devuelvas `hashedPassword`, tokens ni datos internos de la entidad.

## Forma de trabajar
- Flujo SDD completo con la skill `sdd`: una fase por vez y **para** a esperar aprobación.
- Implementa **una sola tarea** por llamada, tests primero, y no empieces la siguiente.
- Cambios pequeños y enfocados: nada de funcionalidades que no estén en la spec.

## Límites
- Siempre: respetar la constitution, mantener los tests en verde, dejar `MEMORY.md` actualizado.
- Pregunta antes: cambiar la estructura de carpetas, añadir una dependencia, renombrar un endpoint ya aprobado.
- Nunca: tocar `docs/constitution.md`, borrar tests para que pasen, commitear `.env`.

## Verificación
- Tarea cerrada solo con `pnpm lint && pnpm build && pnpm test && pnpm test:e2e` en verde.
