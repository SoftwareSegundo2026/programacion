// =============================================================================
// components/ui/Skeleton.tsx — Estado de carga (loading)
// -----------------------------------------------------------------------------
// Placeholder animado que se muestra MIENTRAS una query no resolvió aún.
// LoadingSkeleton arma una grilla de tarjetas grises para que la pantalla no
// "salte" cuando llegan los datos.
//
// POR QUÉ: junto con ErrorState y EmptyState conforma los tres estados de UI
// que pide design.md (carga, error, vacío). Con TanStack Query basta mirar
// isLoading / isError / data.length para decidir cuál mostrar.
// =============================================================================
import { cn } from "@/lib/cn";

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("animate-pulse rounded-xl bg-slate-200", className)} />;
}

// Estado de CARGA: lo que el usuario ve mientras la query resuelve.
export function LoadingSkeleton() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="space-y-3 rounded-2xl bg-white p-5 shadow-sm">
          <Skeleton className="h-5 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-4 w-1/3" />
        </div>
      ))}
    </div>
  );
}