// =============================================================================
// lib/api.ts — Cliente HTTP tipado
// -----------------------------------------------------------------------------
// Único punto por donde pasan TODAS las llamadas a la API. Centraliza:
//   1) la URL base (con el rewrites de next.config, "/api" apunta al backend),
//   2) el manejo de errores (respuestas no OK -> ApiError con detalle),
//   3) la serialización JSON de entrada y salida.
//
// POR QUÉ: si cada componente hiciera su propio fetch() la lógica de datos
// quedaría dispersa, sin tipar y con errores manejados distinto en cada
// pantalla. Con este cliente, los hooks de TanStack Query solo describen QUÉ
// piden; el CÓMO (red, headers, errores) vive en un solo lugar.
// =============================================================================

// Cliente HTTP tipado. Un solo punto que centraliza fetch, errores y JSON.

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

// La API se consume a través del rewrites de next.config (mismo origen).
const API_BASE = "/api";

export async function apiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let detail = `Error ${res.status}`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      // respuesta sin JSON
    }
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}