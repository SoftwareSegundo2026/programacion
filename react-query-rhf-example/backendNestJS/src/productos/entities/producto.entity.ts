// =============================================================================
// src/productos/entities/producto.entity.ts — Entidad Producto
// -----------------------------------------------------------------------------
// Define la forma de un producto tal como se guarda y se devuelve.
// En este ejemplo la "persistencia" es en memoria (igual que el backend
// FastAPI), por eso la entidad es una clase simple sin ORM.
//
// POR QUÉ: separar la entidad (cómo se ve el dato) de los DTO (qué se acepta
// al crear/editar) evita que la validación de entrada contamine la salida.
// =============================================================================
export class Producto {
  id!: number;
  nombre!: string;
  categoria!: string;
  precio!: number;
  stock!: number;
  disponible!: boolean;
  creado_en!: string;
}