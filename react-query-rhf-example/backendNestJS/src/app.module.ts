// =============================================================================
// src/app.module.ts — Módulo raíz de la aplicación
// -----------------------------------------------------------------------------
// NestJS organiza todo en "módulos". Este módulo raíz importa los módulos de
// cada dominio; por ahora solo el de productos (y el controlador de salud).
//
// POR QUÉ: cada dominio (productos, usuarios, vehículos…) vive en su propio
// módulo con su controlador y servicio. Es el equivalente a las "apps" o
// "routers" de FastAPI, pero con inyección de dependencias.
// =============================================================================
import { Module } from '@nestjs/common';
import { ProductosModule } from './productos/productos.module';
import { SaludController } from './salud.controller';

@Module({
  imports: [ProductosModule],
  controllers: [SaludController],
})
export class AppModule {}