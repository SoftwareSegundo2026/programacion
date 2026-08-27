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
  const enCarrito = useCarrito((s) => s.items.includes(producto.id));

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
        <Button variant="secondary" className="flex-1" onClick={() => agregar(producto.id)}>
          {enCarrito ? "Agregado ✓" : "Agregar"}
        </Button>
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