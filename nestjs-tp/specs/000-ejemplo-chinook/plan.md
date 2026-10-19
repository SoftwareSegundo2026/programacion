# Plan 000 — API de catálogo musical (Chinook)

> Archivo de **referencia**. Muestra el paso de QUÉ (spec) a CÓMO (plan): acá sí
> aparecen NestJS, los archivos y la estrategia de tests.

Estado: aprobado · Spec: `specs/000-ejemplo-chinook/spec.md`

## Estructura de módulos

```
src/
├── main.ts                      ← ValidationPipe global, CORS, puerto desde ConfigService
├── app.module.ts                ← ConfigModule + módulos del dominio
├── common/
│   └── repositories/in-memory.repository.ts   ← DAO genérico (patrón DAO)
├── albums/
│   ├── albums.module.ts
│   ├── albums.controller.ts     ← Facade: solo HTTP y códigos de estado
│   ├── albums.service.ts        ← lógica de negocio
│   ├── albums.repository.ts     ← acceso a datos
│   ├── dto/create-album.dto.ts  ← validación de entrada (class-validator)
│   ├── dto/update-album.dto.ts  ← PartialType
│   └── entities/album.entity.ts ← entidad de salida
├── artists/ … genres/ … tracks/  ← mismo patrón
└── auth/                         ← fuera de esta spec
```

## Archivos y responsabilidad

| Archivo | Qué hace | RF |
|---|---|---|
| `src/main.ts` | `ValidationPipe({ whitelist, transform })`, puerto desde `.env` | RF-4 |
| `src/albums/albums.controller.ts` | Rutas `GET/POST/PATCH/DELETE`, `ParseIntPipe`, códigos 201/204 | RF-1, RF-2, RF-3, RF-5, RF-6 |
| `src/albums/albums.service.ts` | Regla de negocio: no borrar artista con álbumes, paginación acotada | RF-8, RF-9 |
| `src/albums/albums.repository.ts` | Persistencia y búsquedas por id | RF-1, RF-2 |
| `src/albums/dto/create-album.dto.ts` | `@IsString`, `@IsInt` sobre `artistId` | RF-4 |
| `test/albums.e2e-spec.ts` | Ciclo completo sobre la app levantada | RF-1…RF-6 |

## Decisiones (y por qué), contra la constitution

1. **Repository propio y reemplazable** — principio 3 (capas) y para poder
   mockearlo en los tests unitarios sin tocar la base.
2. **DTOs con `class-validator` + `ValidationPipe` global** — principio 4 y RF-4:
   la validación no se escribe a mano en el controller.
3. **Excepciones nativas de Nest** (`NotFoundException`, `ConflictException`)
   — RF-2 y RF-9: la API nunca devuelve 200 con un error adentro.
4. **Paginación acotada** (`limit` con máximo) — RNF-4: evitar que un listado
   traiga el catálogo entero.
5. **Sin auth todavía** — la spec lo pone en "fuera de alcance"; RF-7 se cubre
   con un guard genérico que responde 401, sin roles.

## Estrategia de tests

| Tanda | Tipo | Qué cubre |
|---|---|---|
| A | unit (`albums.service.spec.ts`) | RF-8, RF-9 con el repository mockeado |
| B | unit (validación de DTO) | RF-4 |
| C | e2e (`albums.e2e-spec.ts`) | RF-1, RF-2, RF-3, RF-5, RF-6, RF-7 |

- Unit: `Test.createTestingModule` con `{ provide: AlbumsRepository, useValue: mock }`.
- e2e: `supertest` contra la app completa, ciclo listar → crear → leer → patch → delete.
- **Ningún RF queda sin test.** Si un RF no tiene tanda, la spec no se puede validar.

## Riesgos

- Devolver `null` en vez de 404 → el reviewer lo marca como RF-2 no implementado.
- Olvidar el `.js` en los imports locales: el build pasa y el e2e no arranca.
- Que el service haga `try/catch` y convierta un 404 en 200.
