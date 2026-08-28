// =============================================================================
// src/productos/productos.service.ts — Servicio de productos
// -----------------------------------------------------------------------------
// Contiene la lógica de negocio y el "almacenamiento" (en memoria, con los
// mismos datos de ejemplo que el backend FastAPI). Los métodos implementan el
// CRUD y lanzan HttpException(404) cuando el producto no existe.
//
// POR QUÉ: el controlador solo se encarga de recibir la petición HTTP; la
// lógica vive en el servicio. Así se puede reutilizar, testear de forma
// aislada y, si más adelante se quiere una base de datos real, se cambia acá
// sin tocar el controlador.
// =============================================================================
import { HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { CreateProductoDto } from './dto/create-producto.dto';
import { UpdateProductoDto } from './dto/update-producto.dto';
import { Producto } from './entities/producto.entity';

@Injectable()
export class ProductosService {
  // Mismos datos de ejemplo que backend/main.py (FastAPI).
  private productos: Record<number, Producto> = {
    1: {
      id: 1,
      nombre: 'Café torrado 500g',
      categoria: 'Bebidas',
      precio: 4500,
      stock: 24,
      disponible: true,
      creado_en: '2026-08-20T10:00:00',
    },
    2: {
      id: 2,
      nombre: 'Medialunas de manteca (x6)',
      categoria: 'Panificados',
      precio: 3200,
      stock: 12,
      disponible: true,
      creado_en: '2026-08-20T10:05:00',
    },
    3: {
      id: 3,
      nombre: 'Torta de chocolate',
      categoria: 'Repostería',
      precio: 15000,
      stock: 0,
      disponible: false,
      creado_en: '2026-08-20T10:10:00',
    },
  };
  private proximoId = 4;

  findAll(buscar?: string): Producto[] {
    let items = Object.values(this.productos);
    if (buscar) {
      const q = buscar.toLowerCase();
      items = items.filter(
        (p) =>
          p.nombre.toLowerCase().includes(q) ||
          p.categoria.toLowerCase().includes(q),
      );
    }
    return items;
  }

  findOne(id: number): Producto {
    const producto = this.productos[id];
    if (!producto) {
      throw new HttpException('Producto no encontrado', HttpStatus.NOT_FOUND);
    }
    return producto;
  }

  create(dto: CreateProductoDto): Producto {
    const producto: Producto = {
      id: this.proximoId++,
      ...dto,
      creado_en: new Date().toISOString().slice(0, 19),
    };
    this.productos[producto.id] = producto;
    return producto;
  }

  update(id: number, dto: UpdateProductoDto): Producto {
    this.findOne(id);
    this.productos[id] = { ...this.productos[id], ...dto };
    return this.productos[id];
  }

  remove(id: number): void {
    this.findOne(id);
    delete this.productos[id];
  }
}