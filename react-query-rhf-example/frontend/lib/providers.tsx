// =============================================================================
// lib/providers.tsx — Proveedor global de TanStack Query
// -----------------------------------------------------------------------------
// Crea el QueryClient (la "caché" de datos del servidor) y lo pone a
// disposición de toda la aplicación. Se monta una sola vez en el layout raíz.
//
// POR QUÉ: TanStack Query necesita un QueryClient arriba en el árbol para que
// cualquier componente pueda usar useQuery / useMutation. Las opciones por
// defecto que definimos acá (staleTime, retry, refetchOnWindowFocus) aplican a
// todas las consultas y evitan pedir la misma lista a la API en cada clic.
//
// Nota: el archivo es un componente de cliente ("use client") porque usa hooks
// de React; los layout pueden seguir siendo server components que lo importan.
// =============================================================================
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

// Proveedor global de TanStack Query.
// staleTime controla cuánto tiempo la caché se considera "fresca"
// (evita refetchear la lista en cada navegación).
export function Providers({ children }: { children: ReactNode }) {
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 10_000,
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}