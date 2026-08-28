// =============================================================================
// src/main.ts — Punto de entrada de la aplicación NestJS
// -----------------------------------------------------------------------------
// Crea la app, aplica configuraciones globales y la deja escuchando en el
// puerto 8000 (o en PORT si se define por variable de entorno):
//   - setGlobalPrefix('api'): todas las rutas quedan bajo /api, igual que en
//     el backend FastAPI (que usaba /api/productos, /api/salud).
//   - enableCors: permite que el frontend (Next.js) llame directo si se
//     desactiva el rewrite; igual patrón que el CORS del backend FastAPI.
//   - ValidationPipe: valida los DTO con class-validator en cada request y
//     descarta campos que no estén declarados (whitelist).
// =============================================================================
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api');
  app.enableCors({
    origin: '*', // solo para desarrollo / demo (igual que el backend FastAPI)
    credentials: true,
  });
  app.useGlobalPipes(
    new ValidationPipe({ whitelist: true, transform: true }),
  );

  const port = Number(process.env.PORT ?? 8000);
  await app.listen(port);
}
bootstrap();