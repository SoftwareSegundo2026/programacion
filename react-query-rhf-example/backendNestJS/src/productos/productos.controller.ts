// =============================================================================
// src/productos/productos.controller.ts — Controlador de productos
// -----------------------------------------------------------------------------
// Expone las rutas HTTP del CRUD, todas bajo /api/productos (por el prefijo
// global 'api' definido en main.ts). Cada método delega en el servicio:
//
//   GET    /api/productos          -> lista (con filtro ?buscar=)
//   GET    /api/productos/:id      -> detalle (404 si no existe)
//   POST   /api/productos          -> alta (201)
//   PUT    /api/productos/:id      -> edición
//   DELETE /api/productos/:id      -> baja (204)
//
// POR QUÉ: el controlador es la "capa HTTP" (análoga a las rutas de FastAPI);
// ParseIntPipe valida que :id sea numérico y el ValidationPipe global valida
// el cuerpo contra los DTO.
// =============================================================================
import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  HttpStatus,
  Param,
  ParseIntPipe,
  Post,
  Put,
  Query,
} from '@nestjs/common';
import { CreateProductoDto } from './dto/create-producto.dto';
import { UpdateProductoDto } from './dto/update-producto.dto';
import { Producto } from './entities/producto.entity';
import { ProductosService } from './productos.service';

@Controller('productos')
export class ProductosController {
  constructor(private readonly productosService: ProductosService) {}

  @Get()
  findAll(@Query('buscar') buscar?: string): Producto[] {
    return this.productosService.findAll(buscar);
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number): Producto {
    return this.productosService.findOne(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: CreateProductoDto): Producto {
    return this.productosService.create(dto);
  }

  @Put(':id')
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateProductoDto,
  ): Producto {
    return this.productosService.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id', ParseIntPipe) id: number): void {
    return this.productosService.remove(id);
  }
}