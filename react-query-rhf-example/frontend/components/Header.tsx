// =============================================================================
// components/Header.tsx — Barra de navegación superior
// -----------------------------------------------------------------------------
// Cabecera global con los accesos principales y el contador del carrito.
// El contador se lee del store de Zustand (client state): es un dato que solo
// existe en el navegador y no viaja a la API.
//
// POR QUÉ: es el ejemplo vivo de la separación de estados: el contador se
// actualiza al instante con useCarrito sin ninguna petición HTTP, mientras
// que los productos que muestra la página sí vienen de TanStack Query.
// =============================================================================
"use client";

import Link from "next/link";
import { useCarrito } from "@/lib/store";

// Header con estado del cliente (Zustand): el contador del carrito es
// estado local del navegador y no depende de la API.
export function Header() {
  // Total de unidades (suma las cantidades de cada producto en el carrito).
  const cantidad = useCarrito((s) =>
    Object.values(s.items).reduce((total, n) => total + n, 0)
  );

  return (
    <header className="bg-slate-900 text-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-bold">
          Taller Frontend
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link href="/productos" className="text-slate-100 hover:text-white">
            Productos
          </Link>
          <Link href="/productos/nuevo" className="text-slate-100 hover:text-white">
            + Nuevo
          </Link>
          <Link
            href="/carrito"
            className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold hover:bg-white/20"
            aria-label={`Carrito con ${cantidad} productos`}
          >
            Carrito: {cantidad}
          </Link>
        </nav>
      </div>
    </header>
  );
}