// =============================================================================
// next.config.ts — Configuración de Next.js
// -----------------------------------------------------------------------------
// Cumple un rol clave en este taller: el "rewrites". Con él, el frontend puede
// llamar a la API con rutas relativas (por ejemplo fetch("/api/productos"))
// y Next.js reenvía la petición al backend real.
//
// La URL del backend NO está escrita acá: se lee de la variable de entorno
// API_BASE_URL definida en el archivo .env.local (ver .env.example). Es una
// variable "server-side" (sin prefijo NEXT_PUBLIC_), así que nunca se expone
// en el bundle que recibe el navegador.
//
// POR QUÉ: así evitamos problemas de CORS en desarrollo, el frontend no
// necesita saber en qué puerto corre el backend, y cada alumno puede apuntar
// a su propio servidor sin tocar código.
// =============================================================================
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    const apiBase = process.env.API_BASE_URL ?? "http://localhost:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${apiBase}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;