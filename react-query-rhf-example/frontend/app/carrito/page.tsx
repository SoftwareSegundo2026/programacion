// =============================================================================
// app/carrito/page.tsx — Vista del carrito
// -----------------------------------------------------------------------------
// Muestra los productos agregados al carrito con sus cantidades (se pueden
// comprar varias unidades de un mismo producto). Es el ejemplo más claro de
// cómo se combinan los DOS tipos de estado:
//   - Zustand (lib/store.ts) guarda { idProducto: cantidad } ("client state"):
//     lo que el usuario eligió en el navegador, sin peticiones a la API.
//   - TanStack Query (useProductos) provee los datos de esos productos
//     ("server state"): nombre, precio, disponibilidad, con caché.
// La vista une ambas fuentes: productos?.filter((p) => (items[p.id] ?? 0) > 0).
//
// POR QUÉ: si el carrito guardara el producto completo, quedaría desactualizado
// cuando el precio cambie en el servidor. Guardar ids con cantidad y resolver
// contra la API mantiene siempre la información fresca.
// =============================================================================
"use client";

import { useMemo } from "react";
import Link from "next/link";
import { useCarrito } from "@/lib/store";
import { useProductos } from "@/queries/productos";
import { DisponibilidadBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { EmptyState, ErrorState } from "@/components/ui/Estado";
import { LoadingSkeleton } from "@/components/ui/Skeleton";

export default function CarritoPage() {
  const items = useCarrito((s) => s.items);
  const agregar = useCarrito((s) => s.agregar);
  const restar = useCarrito((s) => s.restar);
  const quitar = useCarrito((s) => s.quitar);
  const limpiar = useCarrito((s) => s.limpiar);

  const { data: productos, isLoading, isError, error } = useProductos();

  const unidades = Object.values(items).reduce((a, b) => a + b, 0);

  // Resolvemos los ids con cantidad del carrito contra la lista de la API.
  const enCarrito = useMemo(
    () => productos?.filter((p) => (items[p.id] ?? 0) > 0) ?? [],
    [productos, items]
  );

  // Total ponderado por cantidad (precio × unidades de cada producto).
  const total = enCarrito.reduce(
    (acc, p) => acc + p.precio * (items[p.id] ?? 0),
    0
  );

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Carrito</h1>
          <p className="text-sm text-slate-500">
            {unidades} unidad{unidades !== 1 && "es"} en total (Zustand +
            TanStack Query).
          </p>
        </div>
        {unidades > 0 && (
          <Button variant="ghost" onClick={limpiar}>
            Vaciar carrito
          </Button>
        )}
      </div>

      {isLoading && <LoadingSkeleton />}

      {isError && <ErrorState mensaje={error?.message ?? "Error desconocido"} />}

      {!isLoading && !isError && unidades === 0 && (
        <EmptyState mensaje="Todavía no agregaste productos al carrito." />
      )}

      {unidades > 0 && enCarrito.length === 0 && !isLoading && (
        <EmptyState mensaje="Los productos del carrito ya no existen en la API." />
      )}

      {enCarrito.length > 0 && (
        <div className="space-y-3">
          {enCarrito.map((p) => {
            const cantidad = items[p.id] ?? 0;
            return (
              <div
                key={p.id}
                className="flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-white p-4 shadow-sm"
              >
                <div>
                  <p className="font-semibold text-slate-900">{p.nombre}</p>
                  <p className="text-sm text-slate-500">
                    {p.categoria} · ${p.precio.toLocaleString("es-AR")} c/u
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <DisponibilidadBadge disponible={p.disponible} />

                  {/* Control de cantidad: permite comprar más de una unidad */}
                  <div className="flex items-center gap-2 rounded-full border border-slate-300 px-2 py-1">
                    <button
                      type="button"
                      onClick={() => restar(p.id)}
                      aria-label="Quitar una unidad"
                      className="px-1 text-lg font-bold text-slate-600 hover:text-slate-900"
                    >
                      −
                    </button>
                    <span className="min-w-6 text-center text-sm font-semibold">
                      {cantidad}
                    </span>
                    <button
                      type="button"
                      onClick={() => agregar(p.id)}
                      aria-label="Agregar una unidad"
                      className="px-1 text-lg font-bold text-slate-600 hover:text-slate-900"
                    >
                      +
                    </button>
                  </div>

                  <p className="w-24 text-right text-sm font-semibold text-slate-900">
                    ${(p.precio * cantidad).toLocaleString("es-AR")}
                  </p>

                  <Button variant="ghost" onClick={() => quitar(p.id)}>
                    Quitar
                  </Button>
                </div>
              </div>
            );
          })}

          <div className="flex items-center justify-between rounded-2xl bg-slate-900 p-5 text-white">
            <p className="text-sm font-semibold">Total</p>
            <p className="text-lg font-bold">${total.toLocaleString("es-AR")}</p>
          </div>

          <p className="text-center text-sm text-slate-500">
            ¿Listo?{" "}
            <Link href="/productos" className="font-semibold text-slate-700 underline">
              Seguir comprando
            </Link>
          </p>
        </div>
      )}
    </div>
  );
}