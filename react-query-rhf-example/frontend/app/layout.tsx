// =============================================================================
// app/layout.tsx — Layout raíz de la aplicación
// -----------------------------------------------------------------------------
// Este archivo envuelve TODAS las páginas: monta el proveedor de TanStack
// Query (Providers) y el Header, y define el contenido principal. Es la única
// pieza que necesita saber que existe una caché de datos global.
//
// POR QUÉ: si cada página montara su propio QueryClient, la caché se perdería
// al navegar. Al ponerlo acá arriba, cualquier página puede usar useQuery /
// useMutation y los datos quedan compartidos entre rutas.
//
// Nota: el layout puede ser un server component; Providers (que usa hooks) es
// quien marca el límite "use client".
// =============================================================================
import type { Metadata } from "next";
import { Providers } from "@/lib/providers";
import { Header } from "@/components/Header";
import "./globals.css";

export const metadata: Metadata = {
  title: "Taller Frontend · TanStack Query + React Hook Form + Zod",
  description:
    "Ejemplo didáctico de consumo de APIs con TanStack Query, formularios con React Hook Form + Zod y estado del cliente con Zustand.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Providers>
          <Header />
          <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        </Providers>
      </body>
    </html>
  );
}