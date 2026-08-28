// =============================================================================
// postcss.config.mjs — Configuración de PostCSS para Tailwind v4
// -----------------------------------------------------------------------------
// Indica que PostCSS debe procesar el CSS con el plugin oficial de Tailwind.
// Es parte de la cadena de estilos: sin él, las clases de Tailwind del
// proyecto no se compilan.
// =============================================================================
const config = {
  plugins: ["@tailwindcss/postcss"],
};

export default config;