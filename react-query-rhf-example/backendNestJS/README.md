# Backend NestJS (alternativa a FastAPI)

Backend de ejemplo en **NestJS** que replica la API de productos del backend
FastAPI (`backend/main.py`): mismas rutas, mismos datos iniciales y las mismas
validaciones (mensajes en español) para que el frontend del taller funcione
sin cambios.

## ¿Por qué NestJS?

- **Arquitectura modular** (módulos, controladores, servicios) con **inyección
  de dependencias** — el equivalente estructurado de los "routers + services"
  de FastAPI.
- **DTO + ValidationPipe**: validación de entrada con `class-validator`, el
  análogo de los modelos Pydantic.
- TypeScript de punta a punta, ideal para equipos que ya usan Next.js/React.

## Endpoints (idénticos a los de FastAPI)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/salud` | Estado del servidor |
| `GET` | `/api/productos` | Lista productos (filtro opcional `?buscar=`) |
| `GET` | `/api/productos/:id` | Detalle por id (404 si no existe) |
| `POST` | `/api/productos` | Alta (201) |
| `PUT` | `/api/productos/:id` | Edición |
| `DELETE` | `/api/productos/:id` | Baja (204) |

## Puesta en marcha

```bash
cd backendNestJS
pnpm install        # o npm install
pnpm run start:dev  # o npm run start:dev  -> http://localhost:8000
```

## Comparación con el backend FastAPI

| FastAPI | NestJS |
|---|---|
| `app/main.py` (FastAPI + CORS) | `src/main.ts` (`NestFactory` + CORS + prefijo global `api`) |
| `@app.get("/api/productos")` | `@Controller('productos')` + `@Get()` |
| Modelos Pydantic (`ProductoCreate`) | DTOs con `class-validator` (`CreateProductoDto`) |
| `PRODUCTOS` en memoria | `ProductosService` con `Record<number, Producto>` en memoria |
| `HTTPException(404)` | `HttpException(..., HttpStatus.NOT_FOUND)` |

## Estructura

```
backendNestJS/
├── src/
│   ├── main.ts                    # bootstrap + CORS + ValidationPipe
│   ├── app.module.ts              # módulo raíz
│   ├── salud.controller.ts        # GET /api/salud
│   └── productos/
│       ├── productos.module.ts    # módulo del dominio
│       ├── productos.controller.ts# rutas HTTP
│       ├── productos.service.ts   # lógica de negocio + datos en memoria
│       ├── dto/                   # create-producto.dto.ts, update-producto.dto.ts
│       └── entities/              # producto.entity.ts
├── nest-cli.json
├── package.json
└── tsconfig.json
```

> Nota: al igual que el backend FastAPI, los datos se guardan **en memoria**:
> al reiniciar el servidor los cambios se pierden. Es intencional para
> mantener el ejemplo enfocado en el frontend.