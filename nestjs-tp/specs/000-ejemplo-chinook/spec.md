# Spec 000 — API de catálogo musical (Chinook)

> **Archivo de REFERENCIA para el alumno y para el docente.**
> Es el nivel de detalle que se espera en una spec. Muestra además el paso de
> "QUÉ" a "CÓMO": la spec no menciona NestJS, TypeScript ni ningún archivo.

Estado: **aprobada**

## Contexto y objetivo

Se necesita una API REST que exponga el catálogo musical de la base Chinook
(artistas, álbumes, géneros y pistas) para que una aplicación web pueda
consultarlo y administrarlo. Hoy la información está solo en la base y no hay
forma de consumirla desde otro programa.

## Usuarios

| Rol | Qué hace |
|---|---|
| Visitante | Consulta el catálogo sin autenticarse |
| Administrador | Crea, modifica y elimina recursos del catálogo |

## Historias de usuario

- **HU-1.** Como visitante, quiero listar y buscar artistas, álbumes, géneros y
  pistas, para explorar el catálogo sin necesidad de cuenta.
- **HU-2.** Como administrador, quiero crear, editar y eliminar recursos, para
  mantener el catálogo actualizado.
- **HU-3.** Como visitante, quiero que las respuestas ya traigan los nombres
  relacionados (por ejemplo el título del álbum de una pista), para no tener que
  hacer una petición por cada relación.
- **HU-4.** Como administrador, quiero que la API me avise qué dato está mal al
  crear o editar, para corregirlo sin adivinar.

## Requisitos funcionales (en EARS)

- **RF-1:** CUANDO se solicita `GET /albums`, EL SISTEMA devuelve una lista
  paginada de álbumes con su artista incluido.
- **RF-2:** CUANDO se solicita `GET /albums/:id` de un álbum existente, EL
  SISTEMA devuelve el álbum con su artista; SI el id no existe, ENTONCES EL
  SISTEMA responde con un código 404.
- **RF-3:** CUANDO un administrador envía `POST /albums` con datos válidos, EL
  SISTEMA persiste el álbum y responde 201 con el recurso creado.
- **RF-4:** SI `POST /albums` llega sin título o con un `artistId` inexistente,
  ENTONCES EL SISTEMA responde 400 y no persiste nada.
- **RF-5:** CUANDO un administrador envía `PATCH /albums/:id`, EL SISTEMA
  actualiza **solo** los campos enviados y conserva el resto.
- **RF-6:** CUANDO un administrador envía `DELETE /albums/:id`, EL SISTEMA
  elimina el recurso y responde 204.
- **RF-7:** MIENTRAS la petición no incluya credenciales válidas, EL SISTEMA
  permite **solo** operaciones de lectura; toda escritura responde 401.
- **RF-8:** CUANDO se lista un recurso, EL SISTEMA acepta `skip` y `limit` para
  paginar y limita `limit` a un máximo razonable.
- **RF-9:** CUANDO se elimina un artista que tiene álbumes, EL SISTEMA rechaza
  la operación con 409 y no deja huérfanos.

## Requisitos no funcionales

- **RNF-1:** La API expone su documentación interactiva auto-generada.
- **RNF-2:** Todas las respuestas son JSON con la estructura uniforme.
- **RNF-3:** Ninguna respuesta incluye datos internos de la base (claves,
  hashes, marcas de tiempo internas).
- **RNF-4:** El tiempo de respuesta de listado debe mantenerse acotado ante un
  catálogo grande (no debe cargar todas las filas de una).

## Casos límite

- Id que no existe / id no numérico.
- Listado sin registros (respuesta vacía, 200, no 404).
- `skip` o `limit` fuera de rango o negativos.
- Crear un recurso duplicado.
- Borrar un recurso referenciado por otro (integridad referencial).
- Dos escrituras simultáneas sobre el mismo recurso.

## Fuera de alcance

- Autenticación con roles y permisos finos (va en una spec posterior).
- Búsqueda full-text y filtros complejos (spec de motor de búsqueda).
- Carga de imágenes de portadas.

## Criterios de finalización

- Todos los RF anteriores cubiertos por al menos un test automatizado.
- La documentación de la API refleja los endpoints reales.
- Ningún RF queda sin comprobación automatizada.

## Dudas abiertas

- [NECESITA ACLARACIÓN] ¿El listado de pistas debe poder filtrarse por género
  desde el día uno, o eso entra en la spec de búsqueda?
