# Taller: Consumo de APIs en Next.js — TanStack Query · React Hook Form · Zod

Ejemplo didáctico para aplicar los conceptos de **datos (server state)**, **formularios con validación tipada** y **estado del cliente** en un frontend Next.js conectado a un backend. El proyecto incluye **dos backends equivalentes** (mismas rutas y datos) para que se elija el que prefiera cada alumno:

- **FastAPI** → `backend/` (Python)
- **NestJS** → `backendNestJS/` (TypeScript)

> ⚠️ **Ambos backends usan el puerto 8000 y no deben estar corriendo al mismo tiempo.** Elegí uno y levantá solo ese.

Este material acompaña la presentación `presentacion/tanstack-query-rhf.pptx` (y `.pdf`).

---

## ¿Qué se demuestra?

| Concepto                                            | Librería                                  | Dónde en el código                                          |
| --------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------- |
| Fetching con caché y estados (loading/error/empty) | TanStack Query                             | `frontend/queries/productos.ts`, `app/productos/page.tsx` |
| Mutaciones (crear / actualizar / eliminar)          | TanStack Query`useMutation`              | `queries/productos.ts`                                      |
| Actualización optimista + rollback                 | `onMutate` / `onError` / `onSettled` | `useEliminarProducto` en `queries/productos.ts`           |
| Invalidación de caché tras escribir               | `invalidateQueries`                      | `queries/productos.ts`                                      |
| Formularios gestionados                             | React Hook Form                            | `components/ProductoForm.tsx`                               |
| Validación tipada compartida                       | Zod +`zodResolver`                       | `schemas/producto.ts`                                       |
| Estado del cliente (UI) con cantidades | Zustand | `lib/store.ts`, `components/Header.tsx`, `app/carrito/page.tsx` |
| Cliente HTTP tipado                                 | —                                         | `lib/api.ts`                                                |

---

## Estructura

```
react-query-rhf-example/
├── backend/                    # API de productos en FastAPI (Python, datos en memoria)
│   └── main.py
├── backendNestJS/              # Misma API de productos en NestJS (TypeScript, datos en memoria)
│   └── src/                    # main.ts, app.module.ts, productos/{controller,service,dto,entities}
├── frontend/                   # App Next.js 16 + TS + Tailwind v4
│   ├── app/
│   │   ├── page.tsx            # Portada explicativa
│   │   ├── carrito/            # Vista del carrito (Zustand + TanStack Query)
│   │   ├── productos/          # Listado (useQuery + delete optimista)
│   │   ├── productos/nuevo/    # Alta (RHF + Zod + useMutation)
│   │   └── productos/[id]/editar/  # Edición (detalle + actualización)
│   ├── components/
│   │   ├── ProductoForm.tsx    # Formulario compartido (RHF + Zod)
│   │   ├── ProductoCard.tsx
│   │   └── ui/                 # Button, Badge, Skeleton, Estado (error/empty)
│   ├── lib/                    # api.ts, providers.tsx, store.ts, cn.ts
│   ├── queries/productos.ts    # Hooks de TanStack Query
│   └── schemas/producto.ts     # Esquema Zod + tipos inferidos
└── presentacion/               # PPTX y PDF con los conceptos
```

---

## Puesta en marcha

### 1. Backend (puerto 8000) — elegí UNO solo

El proyecto trae **dos backends equivalentes** (mismas rutas `/api/productos` y `/api/salud`, mismos datos iniciales). **Elegí uno** y levantá solo ese:

> ⚠️ Ambos usan el puerto 8000. **No pueden estar corriendo al mismo tiempo**; si el otro quedó levantado, detenelo antes de arrancar el elegido.

**Opción A — FastAPI (Python):**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

**Opción B — NestJS (TypeScript):**

```bash
cd backendNestJS
pnpm install        # o npm install
pnpm run start:dev  # o npm run start:dev
```

Como ambos exponen la misma API, **el frontend funciona sin cambios** con cualquiera de los dos.

### 2. Frontend (puerto 3000)

El proyecto funciona con **npm** o **pnpm** (elegí uno solo):

```bash
cd frontend
cp .env.example .env.local   # configurá API_BASE_URL si tu backend corre en otro puerto
```

```bash
# Con npm
npm install
npm run dev

# Con pnpm
pnpm install
pnpm run dev
```

Para levantar la versión de producción (en la que no corren las
herramientas de desarrollo de Next):

```bash
npm run build && npm run start      # con npm
pnpm build && pnpm start            # con pnpm
```

> Nota sobre el lockfile: si usás **pnpm**, eliminá el `package-lock.json` que
> genera npm y dejá que pnpm cree su propio `pnpm-lock.yaml`. Usá un solo
> gestor para evitar conflictos.

Abrir http://localhost:3000. El frontend consume la API a través del `rewrites`
de `next.config.ts` (mismo origen `/api` → `API_BASE_URL/api`). La URL del
backend se define en `.env.local` como variable **server-side**
(`API_BASE_URL`, sin prefijo `NEXT_PUBLIC_`), por lo que no se expone en el
navegador y no hay problemas de CORS en desarrollo.

### Nota sobre la API

El backend elegido (FastAPI o NestJS) guarda los datos **en memoria**: al reiniciar el servidor los cambios se pierden. Es intencional, para mantener el ejemplo enfocado en el frontend.

---

## Secuencia de ejecución (en qué orden corren los archivos)

### Estadio 1 — Carga de la aplicación

1. `.env.local` define `API_BASE_URL` (URL del backend). Se lee en `next.config.ts`.
2. `next.config.ts` registra el **rewrite**: toda ruta `/api/*` del frontend se reenvía a `API_BASE_URL/api/*`.
3. `app/layout.tsx` (layout raíz) monta `lib/providers.tsx` y `components/Header.tsx`.
4. `lib/providers.tsx` crea el `QueryClient` (la caché de TanStack Query) con sus opciones por defecto (`staleTime`, `retry`) y envuelve toda la app.
5. `components/Header.tsx` lee `lib/store.ts` (Zustand) para mostrar el contador del carrito.
6. `postcss.config.mjs` + `app/globals.css` procesan los estilos de Tailwind.
7. La ruta de inicio (`app/page.tsx`) se renderiza como portada explicativa.

### Estadio 2 — Consulta de un producto (GET)

1. El usuario entra a `/productos` → se ejecuta `app/productos/page.tsx`.
2. La página llama a `useProductos()` definido en `queries/productos.ts`.
3. TanStack Query revisa la **caché** por la key `['productos']`:
   - si está fresca (`staleTime`), **no** vuelve a pedir nada a la red;
   - si no, ejecuta el `queryFn`.
4. El `queryFn` invoca a `lib/api.ts` → `apiRequest('/productos')`, que hace `fetch('/api/productos')`.
5. El rewrite de `next.config.ts` reenvía la petición a `API_BASE_URL/api/productos` — el backend elegido (`backend/main.py` en FastAPI o `backendNestJS/src` en NestJS).
6. El backend responde con el JSON de los productos.
7. La respuesta se guarda en la caché y la página muestra el estado que corresponda:
   - `isLoading` → `components/ui/Skeleton.tsx`;
   - `isError` → `components/ui/Estado.tsx` (mensaje + botón "Reintentar");
   - datos vacíos → `EmptyState`;
   - con datos → `components/ProductoCard.tsx` (+ `components/ui/Badge.tsx` para disponibilidad).
8. Cada producto llega tipado gracias a `schemas/producto.ts` (`Producto`).

### Estadio 3 — Alta o modificación de un producto (POST / PUT)

1. Alta: `/productos/nuevo` (`app/productos/nuevo/page.tsx`). Modificación: `/productos/[id]/editar` (`app/productos/[id]/editar/page.tsx`).
2. En edición, antes se ejecuta el flujo del **estadio 2** para ese id (`useProducto(id)`); el detalle llega por `defaultValues`.
3. Ambas pantallas renderizan `components/ProductoForm.tsx` (React Hook Form + Zod).
4. Al enviar, `schemas/producto.ts` valida con `zodResolver`:
   - si hay errores, se muestran **por campo** y **no** sale ninguna petición a la red;
   - si pasa, el `onSubmit` dispara la mutación (`useCrearProducto()` o `useActualizarProducto(id)` en `queries/productos.ts`).
5. La mutación usa `lib/api.ts` → `apiRequest('/productos', { method: 'POST', body })` o `PUT /productos/{id}`.
6. El rewrite reenvía al backend; el payload se valida antes de responder (Pydantic en FastAPI, DTOs con `class-validator` en NestJS).
7. `onSuccess` → `invalidateQueries(['productos'])`: la lista queda marcada como vieja y se vuelve a pedir (estadio 2), ahora con el dato nuevo.
8. `router.push('/productos')` redirige al listado, que ya muestra el cambio.

> Resumen del patrón: **página → hook de query/mutation (`queries/`) → cliente HTTP (`lib/api.ts`) → rewrite (`next.config.ts`) → backend (`backend/` o `backendNestJS/`) → caché actualizada → UI con estados (`components/ui/`).**

---

## Los tres conceptos en 30 segundos

1. **TanStack Query** = los datos que vienen del servidor tienen caché, se pueden invalidar y tienen estados (`isLoading`, `isError`, `isEmpty`, `isPending`).
2. **React Hook Form + Zod** = el formulario se gestiona sin estado manual y la validación se define **una sola vez** en un esquema tipado (que además tipa el `submit`).
3. **Zustand** = lo que es solo del navegador (carrito, filtros, preferencias) vive en un store local y no debe mezclarse con el estado de servidor.

---

## Por qué estos conceptos (resumen para la clase)

- **G2 usa `MOCK_VEHICLES` con filtros locales**: TanStack Query es la forma estándar de conectar el frontend a la API y deja de esconder la integración detrás de un mock.
- **Los estados de `design.md`** (carga, error, vacío) se resuelven con `useQuery` en vez de `useEffect` + `useState` manual.
- **Un solo esquema Zod** tipa el formulario y el contrato con la API: menos bugs y mejor DX.
- **Zustand separa el estado de la UI** del estado de servidor, que ya maneja Query.
