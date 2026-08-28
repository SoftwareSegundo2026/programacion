// =============================================================================
// src/salud.controller.ts — Endpoint de salud
// -----------------------------------------------------------------------------
// Responde GET /api/salud con {"estado": "ok"}, igual que el backend FastAPI.
// Sirve para verificar rápido que el servidor está corriendo.
// =============================================================================
import { Controller, Get } from '@nestjs/common';

@Controller('salud')
export class SaludController {
  @Get()
  salud() {
    return { estado: 'ok' };
  }
}