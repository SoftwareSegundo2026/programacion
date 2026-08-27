import Link from "next/link";
import { Button } from "@/components/ui/Button";

const conceptos = [
  {
    titulo: "TanStack Query",
    texto:
      "Fetching, caché y sincronización de datos con el backend. useQuery para leer y useMutation para escribir, con estados de loading/error/vacío resueltos.",
  },
  {
    titulo: "React Hook Form + Zod",
    texto:
      "Formularios con validación tipada. El esquema Zod define reglas y tipos en un solo lugar y el resolver las conecta con el formulario.",
  },
  {
    titulo: "Zustand",
    texto:
      "Estado del cliente (UI) sin fricción: carrito, filtros, preferencias. Se separa del estado de servidor que maneja TanStack Query.",
  },
];

export default function Home() {
  return (
    <div className="space-y-10">
      <section className="rounded-3xl bg-slate-900 p-10 text-white">
        <h1 className="text-3xl font-bold">
          Consumo de APIs en Next.js: datos, formularios y estado
        </h1>
        <p className="mt-3 max-w-2xl text-slate-300">
          Ejemplo didáctico que muestra cómo conectar el frontend a una API
          FastAPI aplicando tres piezas: TanStack Query para los datos,
          React Hook Form + Zod para los formularios y Zustand para el estado
          del cliente.
        </p>
        <div className="mt-6 flex gap-3">
          <Link href="/productos">
            <Button variant="secondary">Ver productos</Button>
          </Link>
          <Link href="/productos/nuevo">
            <Button className="bg-white text-slate-900 hover:bg-slate-200">
              Crear producto
            </Button>
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {conceptos.map((c) => (
          <div key={c.titulo} className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="font-bold text-slate-900">{c.titulo}</h2>
            <p className="mt-2 text-sm text-slate-600">{c.texto}</p>
          </div>
        ))}
      </section>
    </div>
  );
}