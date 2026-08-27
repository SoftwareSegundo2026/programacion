import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { apiRequest } from "@/lib/api";
import type { Producto, ProductoInput } from "@/schemas/producto";

// La "query key" identifica la consulta en la caché. Invalidarla fuerza refetch.
export const productosKey = ["productos"] as const;

// GET /api/productos — lista con caché, loading, error y empty state.
export function useProductos() {
  return useQuery({
    queryKey: productosKey,
    queryFn: () => apiRequest<Producto[]>("/productos"),
  });
}

// GET /api/productos/{id} — detalle para el formulario de edición.
export function useProducto(id: number) {
  return useQuery({
    queryKey: [...productosKey, id],
    queryFn: () => apiRequest<Producto>(`/productos/${id}`),
    enabled: Number.isFinite(id),
  });
}

// POST /api/productos
export function useCrearProducto() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: (data: ProductoInput) =>
      apiRequest<Producto>("/productos", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      // La lista quedó desactualizada: se invalida y TanStack la vuelve a pedir.
      client.invalidateQueries({ queryKey: productosKey });
    },
  });
}

// PUT /api/productos/{id}
export function useActualizarProducto(id: number) {
  const client = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Producto>) =>
      apiRequest<Producto>(`/productos/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      client.invalidateQueries({ queryKey: productosKey });
      client.invalidateQueries({ queryKey: [...productosKey, id] });
    },
  });
}

// DELETE /api/productos/{id} — con ACTUALIZACIÓN OPTIMISTA.
export function useEliminarProducto() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiRequest<void>(`/productos/${id}`, { method: "DELETE" }),
    onMutate: async (id) => {
      // Cancelamos cualquier refetch en curso para no pisar la caché.
      await client.cancelQueries({ queryKey: productosKey });
      // Guardamos el estado previo para poder revertir si falla.
      const anterior = client.getQueryData<Producto[]>(productosKey);
      // Optimismo: el producto desaparece de la UI de inmediato.
      client.setQueryData<Producto[]>(productosKey, (prev) =>
        prev?.filter((p) => p.id !== id)
      );
      return { anterior };
    },
    onError: (_error, _id, contexto) => {
      // Si la API rechaza, restauramos el listado anterior.
      if (contexto?.anterior) {
        client.setQueryData(productosKey, contexto.anterior);
      }
    },
    onSettled: () => {
      // Siempre reconciliamos contra el servidor al final.
      client.invalidateQueries({ queryKey: productosKey });
    },
  });
}