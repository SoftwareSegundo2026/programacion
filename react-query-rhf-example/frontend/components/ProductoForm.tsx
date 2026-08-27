"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  CATEGORIAS,
  productoFormSchema,
  type ProductoFormValues,
} from "@/schemas/producto";
import { Button } from "@/components/ui/Button";

const inputClass =
  "w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200";

interface Props {
  defaultValues?: ProductoFormValues;
  onSubmit: (values: ProductoFormValues) => void;
  isSubmitting: boolean;
  textoBoton?: string;
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="mb-1 block text-sm font-semibold text-slate-700">{label}</label>
      {children}
      {error && <p className="mt-1 text-xs font-medium text-rose-600">{error}</p>}
    </div>
  );
}

// Formulario compartido por alta y edición.
// La validación vive en el esquema Zod y se integra con React Hook Form
// a través de zodResolver: tipado + errores por campo en un solo lugar.
export function ProductoForm({
  defaultValues,
  onSubmit,
  isSubmitting,
  textoBoton = "Guardar",
}: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProductoFormValues>({
    resolver: zodResolver(productoFormSchema),
    defaultValues: defaultValues ?? {
      nombre: "",
      categoria: CATEGORIAS[0],
      precio: 0,
      stock: 0,
      disponible: true,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <Field label="Nombre" error={errors.nombre?.message}>
        <input
          className={inputClass}
          placeholder="Ej: Café torrado 500g"
          {...register("nombre")}
        />
      </Field>

      <Field label="Categoría" error={errors.categoria?.message}>
        <select className={inputClass} {...register("categoria")}>
          {CATEGORIAS.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </Field>

      <div className="grid grid-cols-2 gap-4">
        <Field label="Precio ($)" error={errors.precio?.message}>
          <input
            className={inputClass}
            type="number"
            step="0.01"
            min="0"
            {...register("precio", { valueAsNumber: true })}
          />
        </Field>

        <Field label="Stock" error={errors.stock?.message}>
          <input
            className={inputClass}
            type="number"
            step="1"
            min="0"
            {...register("stock", { valueAsNumber: true })}
          />
        </Field>
      </div>

      <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
        <input
          type="checkbox"
          className="h-4 w-4 rounded border-slate-300"
          {...register("disponible")}
        />
        Disponible para la venta
      </label>

      <div className="flex items-center justify-end gap-3 pt-2">
        <Button type="button" variant="ghost" onClick={() => history.back()}>
          Cancelar
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Guardando…" : textoBoton}
        </Button>
      </div>
    </form>
  );
}