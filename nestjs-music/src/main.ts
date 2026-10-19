import { Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { NestFactory } from '@nestjs/core';
import { AppModule, ObserveInstrument, observeEnabled } from './app.module.js';

async function bootstrap() {
  if (!observeEnabled) {
    new Logger('Bootstrap').log(
      'Observe desactivado: agregá OBSERVE_APP_KEY y OBSERVE_APP_SECRET en .env para enviar telemetría (https://observe.nestjs.com).',
    );
  }

  const app = await NestFactory.create(AppModule, {
    // El hook de instrumentación solo tiene sentido con el módulo de Observe
    // registrado: sin ese módulo no hay agente que consuma los spans.
    instrument: observeEnabled ? ObserveInstrument : undefined,
  });

  const config = app.get(ConfigService);
  const port = Number(config.get<string>('PORT') || 3000);

  await app.listen(port);
}
await bootstrap();
