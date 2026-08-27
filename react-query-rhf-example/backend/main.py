"""
Backend mínimo de ejemplo para el taller "TanStack Query + React Hook Form + Zod".

Expone un CRUD de "productos" para que el frontend demuestre:
- fetching con useQuery
- mutaciones con useMutation (crear / actualizar / eliminar)
- actualización optimista e invalidación de caché

Ejecutar:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Docs: http://localhost:8000/docs
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Base de datos en memoria (SQLite de ejemplo, sin SQLAlchemy) ---

PRODUCTOS: dict[int, dict] = {
    1: {
        "id": 1,
        "nombre": "Café torrado 500g",
        "categoria": "Bebidas",
        "precio": 4500.0,
        "stock": 24,
        "disponible": True,
        "creado_en": "2026-08-20T10:00:00",
    },
    2: {
        "id": 2,
        "nombre": "Medialunas de manteca (x6)",
        "categoria": "Panificados",
        "precio": 3200.0,
        "stock": 12,
        "disponible": True,
        "creado_en": "2026-08-20T10:05:00",
    },
    3: {
        "id": 3,
        "nombre": "Torta de chocolate",
        "categoria": "Repostería",
        "precio": 15000.0,
        "stock": 0,
        "disponible": False,
        "creado_en": "2026-08-20T10:10:00",
    },
}
_PROXIMO_ID = 4


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    categoria: str = Field(default="General", max_length=60)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=100)
    categoria: Optional[str] = Field(default=None, max_length=60)
    precio: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None


class Producto(ProductoBase):
    id: int
    creado_en: str


app = FastAPI(
    title="API de Productos (taller frontend)",
    description="Backend mínimo para el ejemplo de TanStack Query + RHF + Zod.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # solo para desarrollo / demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ahora() -> str:
    return datetime.now().isoformat(timespec="seconds")


@app.get("/api/salud")
def salud():
    return {"estado": "ok"}


@app.get("/api/productos", response_model=list[Producto])
def listar_productos(buscar: Optional[str] = None):
    """Lista productos. `buscar` filtra por nombre/categoría (case-insensitive)."""
    items = list(PRODUCTOS.values())
    if buscar:
        q = buscar.lower()
        items = [
            p
            for p in items
            if q in p["nombre"].lower() or q in p["categoria"].lower()
        ]
    return items


@app.get("/api/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    producto = PRODUCTOS.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.post("/api/productos", response_model=Producto, status_code=201)
def crear_producto(payload: ProductoCreate):
    global _PROXIMO_ID
    producto = payload.model_dump()
    producto["id"] = _PROXIMO_ID
    producto["creado_en"] = _ahora()
    PRODUCTOS[_PROXIMO_ID] = producto
    _PROXIMO_ID += 1
    return producto


@app.put("/api/productos/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, payload: ProductoUpdate):
    producto = PRODUCTOS.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cambios = payload.model_dump(exclude_unset=True)
    producto.update(cambios)
    return producto


@app.delete("/api/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    if producto_id not in PRODUCTOS:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del PRODUCTOS[producto_id]