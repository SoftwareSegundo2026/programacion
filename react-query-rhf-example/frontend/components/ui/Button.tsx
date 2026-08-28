// =============================================================================
// components/ui/Button.tsx — Botón reutilizable
// -----------------------------------------------------------------------------
// Botón con variantes de estilo (primary, secondary, danger, ghost) que se
// usa en todas las pantallas para mantener la UI consistente.
//
// POR QUÉ: un componente base evita repetir clases de Tailwind en cada botón y
// asegura que el sistema de acciones (crear, editar, eliminar, reintentar)
// se vea igual en todo el proyecto. El estado disabled evita doble envío
// mientras una mutación está en curso.
// =============================================================================
import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/cn";

type Variant = "primary" | "secondary" | "danger" | "ghost" | "light";

const styles: Record<Variant, string> = {
  primary:
    "bg-slate-900 text-white hover:bg-slate-700 disabled:bg-slate-400",
  secondary:
    "bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 disabled:text-slate-400",
  danger: "bg-rose-600 text-white hover:bg-rose-500 disabled:bg-rose-300",
  ghost: "text-slate-500 hover:text-slate-900 hover:bg-slate-100",
  // Para usarse sobre fondos oscuros (ej. el hero de la portada).
  light: "bg-white text-slate-900 hover:bg-slate-200 disabled:bg-slate-400",
};

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: ReactNode;
}

export function Button({ variant = "primary", className, children, ...props }: Props) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed",
        styles[variant],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}