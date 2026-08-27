"use client";

import { useParams, useRouter } from "next/navigation";
import { ProductoForm } from "@/components/ProductoForm";
import { ErrorState, EmptyState } from "@/components/ui/Estado";
import { LoadingSkeleton } from "@/components/ui/Skeleton";
import { useActualizarProducto, useProducto } from "@/queries/productos";
import type { ProductoFormValues } from "@/schemas/producto";

// Edición: useQuery carga el detalle y la mutación actualiza.
export default function EditarProductoPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const router = useRouter();

  const { data: producto, isLoading, isError, error } = useProducto(id);
  const actualizar = useActualizarProducto(id);

  const onSubmit = (values: ProductoFormValues) => {
    actualizar.mutate(values, {
      onSuccess: () => router.push("/productos"),
    });
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Editar producto</h1>
        <p className="text-sm text-slate-500">
          Los valores se precargan desde la API y el mismo esquema Zod valida la edición.
        </p>
      </div>

      {!Number.isFinite(id) && (
        <EmptyState mensaje="ID de producto inválido." />
      )}

      {isLoading && <LoadingSkeleton />}

      {isError && <ErrorState mensaje={error?.message ?? "Error desconocido"} />}

      {producto && Number.isFinite(id) && (
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <ProductoForm
            defaultValues={{
              nombre: producto.nombre,
              categoria: producto.categoria,
              precio: producto.precio,
              stock: producto.stock,
              disponible: producto.disponible,
            }}
            onSubmit={onSubmit}
            isSubmitting={actualizar.isPending}
            textoBoton="Guardar cambios"
          />
        </div>
      )}
    </div>
  );
}