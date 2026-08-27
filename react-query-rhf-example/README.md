# Taller: Consumo de APIs en Next.js — TanStack Query · React Hook Form · Zod

Ejemplo didáctico para aplicar los conceptos de **datos (server state)**, **formularios con validación tipada** y **estado del cliente** en un frontend Next.js conectado a un backend FastAPI.

Este material acompaña la presentación `presentacion/tanstack-query-rhf.pptx` (y `.pdf`).

---

## ¿Qué se demuestra?

| Concepto | Librería | Dónde en el código |
|---|---|---|
| Fetching con caché y estados (loading/error/empty) | TanStack Query | `frontend/queries/productos.ts`, `app/productos/page.tsx` |
| Mutaciones (crear / actualizar / eliminar) | TanStack Query `useMutation` | `queries/productos.ts` |
| Actualización optimista + rollback | `onMutate` / `onError` / `onSettled` | `useEliminarProducto` en `queries/productos.ts` |
| Invalidación de caché tras escribir | `invalidateQueries` | `queries/productos.ts` |
| Formularios gestionados | React Hook Form | `components/ProductoForm.tsx` |
| Validación tipada compartida | Zod + `zodResolver` | `schemas/producto.ts` |
| Estado del cliente (UI) | Zustand | `lib/store.ts`, `components/Header.tsx` |
| Cliente HTTP tipado | — | `lib/api.ts` |

---

## Estructura

```
react-query-rhf-example/
├── backend/                    # API mínima de productos (FastAPI + SQLite en memoria)
│   └── main.py
├── frontend/                   # App Next.js 16 + TS + Tailwind v4
│   ├── app/
│   │   ├── page.tsx            # Portada explicativa
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

### 1. Backend (puerto 8000)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

### 2. Frontend (puerto 3000)

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:3000. El frontend consume la API a través del `rewrites` de `next.config.ts` (mismo origen `/api` → `localhost:8000/api`).

### Nota sobre la API

El backend guarda los datos **en memoria**: al reiniciar `uvicorn` los cambios se pierden. Es intencional, para mantener el ejemplo enfocado en el frontend.

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