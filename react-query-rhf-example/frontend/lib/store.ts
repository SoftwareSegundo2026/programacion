"use client";

import { create } from "zustand";

// Estado del CLIENTE (UI) con Zustand.
// A diferencia del estado de servidor (TanStack Query), esto es local del
// navegador y no necesita sincronizarse con la API: acá un "carrito" de
// demostración que guarda ids de productos seleccionados.
interface CarritoState {
  items: number[];
  agregar: (id: number) => void;
  quitar: (id: number) => void;
  limpiar: () => void;
}

export const useCarrito = create<CarritoState>((set) => ({
  items: [],
  agregar: (id) =>
    set((state) => ({
      items: state.items.includes(id) ? state.items : [...state.items, id],
    })),
  quitar: (id) =>
    set((state) => ({ items: state.items.filter((i) => i !== id) })),
  limpiar: () => set({ items: [] }),
}));