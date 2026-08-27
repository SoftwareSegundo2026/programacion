"use client";

import Link from "next/link";
import { useCarrito } from "@/lib/store";

// Header con estado del cliente (Zustand): el contador del carrito es
// estado local del navegador y no depende de la API.
export function Header() {
  const cantidad = useCarrito((s) => s.items.length);

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
          <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-semibold">
            Carrito: {cantidad}
          </span>
        </nav>
      </div>
    </header>
  );
}