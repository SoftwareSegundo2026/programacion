"use client";

import Link from "next/link";
import { useState } from "react";
import { useEliminarProducto, useProductos } from "@/queries/productos";
import { ProductoCard } from "@/components/ProductoCard";
import { Button } from "@/components/ui/Button";
import { ErrorState, EmptyState } from "@/components/ui/Estado";
import { LoadingSkeleton } from "@/components/ui/Skeleton";

// Listado de productos.
// TanStack Query resuelve por nosotros: isLoading (primera carga),
// isError + refetch, y data con la lista (en caché tras el primer pedido).
export default function ProductosPage() {
  const { data, isLoading, isError, error, refetch } = useProductos();
  const eliminar = useEliminarProducto();
  const [eliminandoId, setEliminandoId] = useState<number | null>(null);

  const onEliminar = (id: number) => {
    setEliminandoId(id);
    eliminar.mutate(id, {
      onSettled: () => setEliminandoId(null),
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Productos</h1>
          <p className="text-sm text-slate-500">
            Listado con TanStack Query · caché, loading, error y empty state.
          </p>
        </div>
        <Link href="/productos/nuevo">
          <Button>+ Nuevo producto</Button>
        </Link>
      </div>

      {isLoading && <LoadingSkeleton />}

      {isError && (
        <ErrorState
          mensaje={error?.message ?? "Error desconocido"}
          onReintentar={() => refetch()}
        />
      )}

      {data && data.length === 0 && (
        <EmptyState mensaje="Todavía no hay productos. Creá el primero." />
      )}

      {data && data.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.map((producto) => (
            <ProductoCard
              key={producto.id}
              producto={producto}
              onEliminar={onEliminar}
              eliminando={eliminandoId === producto.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}