# TP-7 · Docker, CD y observabilidad (NestJS)

**Asignatura:** Programación · **Modalidad:** individual o binaria
**Cronograma:** Clase 23 (09/11) — *dockerización + workflow de CI/CD* · Clase 24 (16/11) — *continuous deployment y observabilidad*
**Requisito previo:** TP-6 (ya existe el pipeline de CI)
**Metodología:** Spec-Driven Development con multiagentes (ver `../README.md`)

---

## Objetivo

Llevar el TP-1 de "corre en mi máquina" a **"se despliega solo y se puede
observar"**: imagen reproducible, despliegue automatizado y logs que permitan
diagnosticar un problema sin adivinar.

## Alcance

1. **Spec aprobada** en `specs/007-docker-cd/spec.md`.
2. **Dockerfile multi-stage** (build → runtime): imagen final sin toolchain,
   **usuario no root**, `.dockerignore` que excluye `node_modules`, `.env`, `dist` viejo.
3. **`docker-compose.yml`:** API + base de datos, con `healthcheck` y `depends_on`
   condicionado; la app **no queda "ready"** si la base no responde.
4. **Variables por entorno:** el mismo artefacto corre en dev y prod solo con
   `.env` distinto; ningún secreto dentro de la imagen.
5. **Pipeline de CD:** en push a la rama principal → build de la imagen →
   push al registry → despliegue en el servidor (SSH) → reinicio del servicio.
   Los secretos van en *repository secrets*.
6. **Observabilidad:**
   - logs **estructurados** (nivel, mensaje, `requestId`, timestamp) en lugar de `console.log` sueltos,
   - un `GET /health` que responda el estado real de la app y de la conexión,
   - (opcional) telemetría con NestJS Observe solo si hay credenciales en `.env`.
7. **Suite en verde** con los 4 gates (corren también dentro del build de la imagen).

## Casos límite con test o evidencia

- Levantar el `compose` **con la base apagada** → healthcheck falla, app no ready.
- La imagen construida dos veces produce resultados equivalentes (reproducibilidad).
- Un log de error contiene `requestId` y **ningún dato sensible** (contraseña, token, DNI).
- Variables mal seteadas → falla al arrancar con un mensaje claro, no a mitad de la primera request.
- El servidor se reinicia → el servicio vuelve solo (systemd/PM2/compose `restart: always`).

## Fuera de alcance

- Orquestación con Kubernetes.
- Múltiples entornos (staging/prod) con infraestructura como código.
- Alertas y notificaciones (opcional).

## Flujo esperado

```bash
/sdd-spec 007-docker-cd → /sdd-plan → /sdd-tasks
/sdd-implement 007-docker-cd T1 … Tn
/sdd-validate 007-docker-cd
```

## Criterios de evaluación

- La imagen arranca con un solo comando en una máquina limpia (evidencia en el README).
- El CD despliega sin intervención manual y el rollback está documentado.
- Se puede responder la pregunta "¿qué pasó en producción a las 3 AM?" con los logs del sistema.
- Ningún secreto embebido en la imagen ni en el historial de git (`docker history` limpio).
