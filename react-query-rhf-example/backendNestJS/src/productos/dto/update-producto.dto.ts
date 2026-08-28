// =============================================================================
// src/productos/dto/update-producto.dto.ts — DTO de edición
// -----------------------------------------------------------------------------
// Igual que CreateProductoDto pero con todos los campos opcionales, porque en
// una edición (PUT) el cliente puede enviar solo los campos que cambió.
// PartialType genera ese "todo opcional" a partir del DTO de creación,
// reutilizando las mismas validaciones (no se duplican las reglas).
// =============================================================================
import { PartialType } from '@nestjs/mapped-types';
import { CreateProductoDto } from './create-producto.dto';

export class UpdateProductoDto extends PartialType(CreateProductoDto) {}