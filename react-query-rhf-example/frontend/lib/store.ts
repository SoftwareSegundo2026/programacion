// =============================================================================
// lib/store.ts — Estado del cliente (client state) con Zustand
// -----------------------------------------------------------------------------
// Guarda información que vive SOLO en el navegador y no tiene por qué viajar a
// la API: acá, un "carrito" de demostración que acumula, por producto, la
// cantidad elegida (permite comprar más de una unidad del mismo producto).
// Se modela como un objeto { idProducto: cantidad }.
//
// POR QUÉ: este es el contraste didáctico con TanStack Query. Mientras Query
// se encarga del "server state" (datos que vienen del backend, compartidos y
// que pueden quedar desactualizados), Zustand maneja lo que es puramente de la
// UI (carrito, filtro activo, tema). Mezclarlos es fuente de bugs clásicos.
//
// Se usa con un hook selectivo: useCarrito((s) => s.items[id]) re-renderiza
// solo a los componentes que lean esa porción del estado.
// =============================================================================
"use client";

import { create } from "zustand";

// Estado del CLIENTE (UI) con Zustand.
// A diferencia del estado de servidor (TanStack Query), esto es local del
// navegador y no necesita sincronizarse con la API: acá un "carrito" que
// guarda { idProducto: cantidad } para permitir varias unidades por producto.
interface CarritoState {
  items: Record<number, number>;
  agregar: (id: number) => void; // +1 a la cantidad del producto
  restar: (id: number) => void;  // -1; si llega a 0, se elimina del carrito
  quitar: (id: number) => void;  // elimina el producto del carrito
  limpiar: () => void;
}

export const useCarrito = create<CarritoState>((set) => ({
  items: {},
  agregar: (id) =>
    set((state) => ({
      items: { ...state.items, [id]: (state.items[id] ?? 0) + 1 },
    })),
  restar: (id) =>
    set((state) => {
      const actual = state.items[id] ?? 0;
      const items = { ...state.items };
      if (actual <= 1) {
        delete items[id];
      } else {
        items[id] = actual - 1;
      }
      return { items };
    }),
  quitar: (id) =>
    set((state) => {
      const items = { ...state.items };
      delete items[id];
      return { items };
    }),
  limpiar: () => set({ items: {} }),
}));