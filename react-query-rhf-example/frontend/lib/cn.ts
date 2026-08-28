// =============================================================================
// lib/cn.ts — Utilidad de clases condicionales
// -----------------------------------------------------------------------------
// Junta nombres de clases CSS filtrando los valores falsos. Es una mini
// versión de la librería clsx + tailwind-merge que se usa en muchos proyectos.
//
// POR QUÉ: permite escribir componentes con estilos condicionales legibles,
// por ejemplo: cn("rounded-full", esRiesgo && "bg-rose-600"). Así el código
// de estilos no se llena de ternarios ilegibles.
// =============================================================================

export function cn(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
}