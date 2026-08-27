import { cn } from "@/lib/cn";

export function Badge({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
        className
      )}
    >
      {children}
    </span>
  );
}

export function DisponibilidadBadge({ disponible }: { disponible: boolean }) {
  return disponible ? (
    <Badge className="bg-emerald-100 text-emerald-700">Disponible</Badge>
  ) : (
    <Badge className="bg-rose-100 text-rose-700">Agotado</Badge>
  );
}