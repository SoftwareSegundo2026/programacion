// =============================================================================
// components/ProductoCard.tsx — Tarjeta de producto
// -----------------------------------------------------------------------------
// Muestra un producto de la lista con sus datos, el estado de disponibilidad
// y las acciones: sumar/quitar unidades al carrito (Zustand, con control +/−
// que permite comprar más de una unidad), Editar (link a la pantalla de
// edición) y Eliminar con confirmación en dos pasos.
//
// POR QUÉ: separa la presentación del listado. La página /productos decide
// QUÉ datos pedir (useQuery) y este componente decide CÓMO se ven y actúan.
// La confirmación antes de eliminar evita acciones destructivas accidentales.
// =============================================================================
"use client";

import Link from "next/link";
import { useState } from "react";
import type { Producto } from "@/schemas/producto";
import { useCarrito } from "@/lib/store";
import { DisponibilidadBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface Props {
  producto: Producto;
  onEliminar: (id: number) => void;
  eliminando?: boolean;
}

// Tarjeta de producto: muestra los datos y las acciones (editar / eliminar).
export function ProductoCard({ producto, onEliminar, eliminando }: Props) {
  const [confirmando, setConfirmando] = useState(false);
  const agregar = useCarrito((s) => s.agregar);
  const restar = useCarrito((s) => s.restar);
  const cantidad = useCarrito((s) => s.items[producto.id] ?? 0);

  return (
    <div className="flex flex-col gap-3 rounded-2xl bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="font-semibold text-slate-900">{producto.nombre}</h3>
          <p className="text-sm text-slate-500">{producto.categoria}</p>
        </div>
        <DisponibilidadBadge disponible={producto.disponible} />
      </div>

      <div className="flex items-baseline justify-between">
        <p className="text-lg font-bold text-slate-900">
          ${producto.precio.toLocaleString("es-AR")}
        </p>
        <p className="text-sm text-slate-500">
          Stock: <span className="font-semibold">{producto.stock}</span>
        </p>
      </div>

      <div className="mt-auto flex items-center gap-2">
        {cantidad === 0 ? (
          <Button variant="secondary" className="flex-1" onClick={() => agregar(producto.id)}>
            Agregar
          </Button>
        ) : (
          <div className="flex flex-1 items-center justify-between rounded-full border border-slate-300 bg-white px-2 py-1">
            <button
              type="button"
              onClick={() => restar(producto.id)}
              aria-label="Quitar una unidad"
              className="px-2 text-lg font-bold text-slate-600 hover:text-slate-900"
            >
              −
            </button>
            <span className="text-sm font-semibold text-slate-900">{cantidad}</span>
            <button
              type="button"
              onClick={() => agregar(producto.id)}
              aria-label="Agregar una unidad"
              className="px-2 text-lg font-bold text-slate-600 hover:text-slate-900"
            >
              +
            </button>
          </div>
        )}
        <Link href={`/productos/${producto.id}/editar`}>
          <Button variant="secondary">Editar</Button>
        </Link>

        {confirmando ? (
          <div className="flex gap-2">
            <Button
              variant="danger"
              disabled={eliminando}
              onClick={() => onEliminar(producto.id)}
            >
              {eliminando ? "…" : "Confirmar"}
            </Button>
            <Button variant="ghost" onClick={() => setConfirmando(false)}>
              No
            </Button>
          </div>
        ) : (
          <Button variant="ghost" onClick={() => setConfirmando(true)}>
            Eliminar
          </Button>
        )}
      </div>
    </div>
  );
}