# TP-4 · Sistema de reservas con transacciones (NestJS)

**Asignatura:** Programación · **Modalidad:** individual o binaria
**Cronograma:** Clase 13 (24/08) — *Proyecto 4: Sistema de Reservas, transacciones y atomicidad*
**Requisito previo:** TP-1 (CRUD y capas) y TP-2 (auth) recomendados
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Implementar reservas con **pago simulado** aplicando el principio de
**atomicidad (todo o nada)**: o se registra la reserva y su pago juntos, o no
queda nada. El objetivo real es demostrar que la concurrencia se resuelve con
transacciones y reglas de dominio, no con esperanza.

## Alcance

1. **Spec aprobada** en `specs/004-reservas/spec.md` — los RF de concurrencia se
   escriben en EARS (`CUANDO dos solicitudes compiten… EL SISTEMA…`).
2. **Recurso con cupo limitado** (mesa, turno, habitación, butaca): la
   disponibilidad se calcula, nunca se incrementa a mano.
3. **Flujo transaccional:** crear reserva + registrar pago en **una** transacción;
   si el pago falla, se hace rollback y no queda reserva huérfana.
4. **Máquina de estados** de la reserva: `PENDIENTE → PAGADA → (CANCELADA | COMPLETADA)`,
   con transiciones inválidas rechazadas (409).
5. **Cancelación** que libera cupo, idempotente (dos veces, misma respuesta).
6. **Pago simulado** con fallo inyectable por el test (no por flag de producción).
7. **Suite en verde** con los 4 gates.

## Casos límite con test obligatorio

| # | Situación | Esperado |
|---|---|---|
| 1 | Dos reservas simultáneas por el último cupo | una 201, la otra 409 — **nunca ambas** |
| 2 | Pago que falla a mitad de la transacción | rollback: sin reserva y sin pago |
| 3 | Reintentar el mismo pago (retry del cliente) | idempotente: no cobra ni reserva dos veces |
| 4 | Cancelar dos veces | segunda cancelación no duplica el cupo |
| 5 | Reserva para una fecha/hora en el pasado | 400 |
| 6 | Reservar más cupos que los disponibles | 409 con el detalle del cupo restante |
| 7 | Cambiar estado inválido (PAGADA → PENDIENTE) | 409 |
| 8 | Consultar disponibilidad durante una transacción abierta | no ve el estado intermedio |

## Fuera de alcance

- Pasarela de pago real (MercadoPago, tarjetas).
- Reservas recurrentes y calendarios de agenda.
- Notificaciones por email.

## Flujo esperado

```bash
/sdd-spec 004-reservas → /sdd-clarify  ← el reviewer revisa los 8 casos límite
/sdd-plan 004-reservas → /sdd-tasks 004-reservas
/sdd-implement 004-reservas T1 … Tn
/sdd-validate 004-reservas
```

## Lo que el reviewer va a buscar específicamente

- El `INSERT` de reserva y el de pago **fuera** de la misma transacción (rollback inútil).
- `disponibilidad` leída y escrita sin bloqueo/condición (classic *race condition*).
- Test de concurrencia ausente o "resuelto" con un `sleep`.
- Estado cambiado por el cliente en el body (`estado=PAGADA` aceptado en el PUT).
- La cancelación que libera cupo sin verificar que la reserva estuviera pagada.
