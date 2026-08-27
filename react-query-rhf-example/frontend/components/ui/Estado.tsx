import { Button } from "@/components/ui/Button";

// Estado de ERROR: feedback claro cuando la query falla (red, 404, 500, etc.).
export function ErrorState({
  mensaje,
  onReintentar,
}: {
  mensaje: string;
  onReintentar?: () => void;
}) {
  return (
    <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-center">
      <p className="text-sm font-semibold text-rose-700">No se pudo cargar la información</p>
      <p className="mt-1 text-sm text-rose-600">{mensaje}</p>
      {onReintentar && (
        <Button variant="secondary" className="mt-4" onClick={onReintentar}>
          Reintentar
        </Button>
      )}
    </div>
  );
}

// Estado VACÍO: qué mostrar cuando la API responde con cero resultados.
export function EmptyState({ mensaje }: { mensaje: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
      <p className="text-sm font-medium text-slate-500">{mensaje}</p>
    </div>
  );
}