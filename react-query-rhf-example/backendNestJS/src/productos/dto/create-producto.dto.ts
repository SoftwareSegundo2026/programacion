// =============================================================================
// src/productos/dto/create-producto.dto.ts — DTO de alta
// -----------------------------------------------------------------------------
// Define y valida los campos que se aceptan al crear un producto (POST).
// Usa class-validator con los mismos mensajes en español que el esquema Zod
// del frontend, de modo que los errores por campo coincidan.
//
// POR QUÉ: los DTO son el contrato de entrada de la API, el equivalente a los
// modelos Pydantic del backend FastAPI y al productoFormSchema del frontend.
// Con ValidationPipe (whitelist + transform) los campos no declarados se
// descartan y los strings numéricos se convierten automáticamente.
// =============================================================================
import {
  IsBoolean,
  IsNumber,
  IsString,
  MaxLength,
  Min,
  MinLength,
} from 'class-validator';

export class CreateProductoDto {
  @IsString()
  @MinLength(3, { message: 'El nombre debe tener al menos 3 caracteres' })
  @MaxLength(100, { message: 'El nombre no puede superar los 100 caracteres' })
  nombre!: string;

  @IsString()
  @MaxLength(60, { message: 'La categoría no puede superar los 60 caracteres' })
  categoria!: string;

  @IsNumber({ maxDecimalPlaces: 2 })
  @Min(0.01, { message: 'El precio debe ser mayor a 0' })
  precio!: number;

  @IsNumber({ maxDecimalPlaces: 0 })
  @Min(0, { message: 'El stock no puede ser negativo' })
  stock!: number;

  @IsBoolean()
  disponible!: boolean;
}