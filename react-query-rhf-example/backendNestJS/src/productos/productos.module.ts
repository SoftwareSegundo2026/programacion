// =============================================================================
// src/productos/productos.module.ts — Módulo de productos
// -----------------------------------------------------------------------------
// Agrupa el controlador y el servicio del dominio "productos". NestJS usa el
// módulo como contenedor: acá se declara qué controladores exponen rutas y qué
// servicios se inyectan (la inyección de dependencias la resuelve el framework).
// =============================================================================
import { Module } from '@nestjs/common';
import { ProductosController } from './productos.controller';
import { ProductosService } from './productos.service';

@Module({
  controllers: [ProductosController],
  providers: [ProductosService],
})
export class ProductosModule {}