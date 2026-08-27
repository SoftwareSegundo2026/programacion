"use client";

import { useRouter } from "next/navigation";
import { ProductoForm } from "@/components/ProductoForm";
import { useCrearProducto } from "@/queries/productos";
import type { ProductoFormValues } from "@/schemas/producto";

// Alta de producto: el formulario valida con Zod y la mutación crea en la API.
export default function NuevoProductoPage() {
  const router = useRouter();
  const crear = useCrearProducto();

  const onSubmit = (values: ProductoFormValues) => {
    crear.mutate(values, {
      onSuccess: () => router.push("/productos"),
    });
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Nuevo producto</h1>
        <p className="text-sm text-slate-500">
          React Hook Form + Zod: validación tipada con errores por campo.
        </p>
      </div>

      <div className="rounded-2xl bg-white p-6 shadow-sm">
        <ProductoForm
          onSubmit={onSubmit}
          isSubmitting={crear.isPending}
          textoBoton="Crear producto"
        />
      </div>
    </div>
  );
}