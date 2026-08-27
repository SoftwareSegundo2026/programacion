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