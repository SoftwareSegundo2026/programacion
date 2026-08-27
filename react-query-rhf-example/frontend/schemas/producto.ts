import { z } from "zod";

// Esquema del formulario (validación tipada, compartida entre crear y editar).
export const productoFormSchema = z.object({
  nombre: z
    .string()
    .min(3, "El nombre debe tener al menos 3 caracteres")
    .max(100, "El nombre no puede superar los 100 caracteres"),
  categoria: z
    .string()
    .min(1, "La categoría es obligatoria")
    .max(60, "La categoría no puede superar los 60 caracteres"),
  // Los inputs number se registran con valueAsNumber (ver ProductoForm),
  // por eso acá se valida directamente con z.number().
  precio: z
    .number({ message: "Ingresá un precio válido" })
    .positive("El precio debe ser mayor a 0"),
  stock: z
    .number({ message: "Ingresá un stock válido" })
    .int("El stock debe ser un número entero")
    .nonnegative("El stock no puede ser negativo"),
  disponible: z.boolean(),
});

// Valores tipados que el formulario produce.
export type ProductoFormValues = z.infer<typeof productoFormSchema>;

// Esquema del producto tal como lo devuelve la API.
export const productoApiSchema = productoFormSchema.extend({
  id: z.number(),
  creado_en: z.string(),
});

export type Producto = z.infer<typeof productoApiSchema>;

// Tipo que espera la API al crear.
export type ProductoInput = Omit<Producto, "id" | "creado_en">;

// Categorías de ejemplo para el selector.
export const CATEGORIAS = ["Bebidas", "Panificados", "Repostería", "Salados", "General"] as const;