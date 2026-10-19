# Constitución — TP NestJS

Principios innegociables del proyecto. **Toda spec, plan y tarea debe cumplirlos.**
No se modifica este archivo sin acuerdo docente–alumno.

1. **La spec manda.** Nada se implementa si no está en la spec activa aprobada.
   Si aparece un requisito nuevo, primero `/sdd-change`, después código.

2. **Los tests son la puerta.** Ninguna tarea se da por hecha con
   `pnpm lint`, `pnpm build`, `pnpm test` o `pnpm test:e2e` en rojo.
   Prohibido borrar o comentar un test para que la suite pase.

3. **Arquitectura por capas.** El `controller` solo traduce HTTP; la lógica vive
   en el `service`; el acceso a datos, en el `repository`. Nunca SQL ni
   reglas de negocio en el controller. La entrada y la salida pasan por DTOs.

4. **TypeScript estricto.** Sin `any`, sin `@ts-ignore`, sin casts forzados
   para "que compile". Si el tipo no cierra, el modelo está mal y se corrige
   el modelo, no el compilador.

5. **La seguridad no se negocia.** Secretos solo en `.env` (nunca en el repo);
   la contraseña jamás viaja en una respuesta; las contraseñas se guardan
   hasheadas; todo endpoint de escritura está protegido por defecto.

6. **Idioma.** Identificadores y código en inglés; documentación, comentarios
   y textos visibles al usuario en español.

---

## Gates de verificación

| Gate | Comando | Cuándo |
|---|---|---|
| Lint | `pnpm lint` | Cada tarea |
| Build | `pnpm build` | Cada tarea |
| Unit | `pnpm test` | Cada tarea (tests primero) |
| e2e | `pnpm test:e2e` | Al cerrar cada tarea que toque un endpoint |
