# Fut-API — Proyecto integrador: API de Fútbol con Flask

## Contexto

Una liga de fútbol te contrató para construir la API que va a alimentar su nueva plataforma digital. Te proporcionaron datos en formato JSON con información de clubes, equipos, jugadores, torneos, partidos y más. Tu tarea es diseñar el modelo de datos, cargarlos en una base SQLite y exponerlos a través de una API REST construida con Flask, además crear una mini web donde se puedan consultar los datos cargados.

## Objetivo

Construir una API REST funcional que permita consultar y administrar información futbolística organizada geográficamente (país → provincia → ciudad → club → equipo) y por competiciones (ligas → torneos → partidos), incluyendo datos de jugadores y mercado de pases.

## Datos proporcionados

Los archivos JSON están en `data/`. Cada uno contiene una lista de registros que deberás analizar para diseñar el esquema de la base de datos:

| Archivo | Descripción |
|---------|-------------|
| `paises.json` | Países (id, nombre, código ISO) |
| `provincias.json` | Provincias/estados (id, nombre, país al que pertenecen) |
| `ciudades.json` | Ciudades (id, nombre, provincia a la que pertenecen) |
| `clubes.json` | Clubes (id, nombre, ciudad, año de fundación, estadio, capacidad) |
| `ligas.json` | Ligas o copas (id, nombre, país, categoría, tipo) |
| `temporadas.json` | Temporadas (id, nombre) |
| `torneos.json` | Torneos — edición de una liga en una temporada (id, nombre, liga, temporada, fechas) |
| `equipos.json` | Participación de un club en un torneo (id, club, torneo, grupo) |
| `partidos.json` | Partidos jugados (id, torneo, equipos local/visitante, fecha, goles) |
| `jugadores.json` | Jugadores (id, nombre, apellido, fecha nacimiento, nacionalidad, posición) |
| `contratos.json` | Contratos / pases (id, jugador, equipo, fechas, precio de traspaso) |
| `campeonatos_ganados.json` | Títulos (id, equipo, torneo, posición obtenida) |

> **Importante:** los IDs en los JSON son las claves foráneas. Por ejemplo, `ciudades.provincia_id` referencia a `provincias.id`. Analizá todas las relaciones antes de diseñar las tablas.

## Tareas

### 1. Análisis y diseño del modelo de datos

- Examiná los 12 archivos JSON.
- Identificá todas las entidades, sus atributos y las relaciones entre ellas.
- Dibujá un diagrama entidad-relación (DER) que muestre tablas, columnas, tipos de datos, claves primarias y foráneas.
- Este DER debe entregarse como parte del proyecto (en papel o digital).

### 2. Crear la base de datos SQLite y cargar los datos

- Escribí un script en Python que:
  - Cree la base de datos SQLite con todas las tablas y sus relaciones.
  - Lea cada archivo JSON e inserte los registros respetando las claves foráneas.
  - Use `sqlite3` (módulo estándar de Python) o SQLAlchemy.

### 3. Implementar la API con Flask

Creá una aplicación Flask que exponga los siguientes endpoints.

#### Endpoints de consulta (GET)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/paises` | Lista todos los países |
| GET | `/paises/<id>` | Detalle de un país con sus provincias |
| GET | `/ligas` | Lista todas las ligas/copas. Filtro: `?pais_id=` |
| GET | `/ligas/<id>` | Detalle de una liga con sus torneos |
| GET | `/torneos` | Lista torneos. Filtros: `?liga_id=`, `?temporada_id=` |
| GET | `/torneos/<id>` | Detalle del torneo con su tabla de posiciones |
| GET | `/clubes` | Lista todos los clubes, ordenados por nombre |
| GET | `/clubes/<id>` | Detalle de un club (incluye ciudad, provincia, país y equipos asociados) |
| GET | `/equipos` | Lista equipos. Filtros: `?club_id=`, `?torneo_id=` |
| GET | `/equipos/<id>` | Detalle del equipo (club, torneo, jugadores activos) |
| GET | `/jugadores` | Lista jugadores. Filtros: `?posicion=`, `?nacionalidad_id=` |
| GET | `/jugadores/<id>` | Detalle del jugador (datos personales + historial de contratos) |
| GET | `/partidos` | Lista partidos. Filtros: `?torneo_id=`, `?equipo_id=`, `?fecha_desde=`, `?fecha_hasta=` |
| GET | `/contratos` | Lista contratos. Filtros: `?jugador_id=`, `?equipo_id=`, `?activo=` |

#### Endpoints de administración (CRUD)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/clubes` | Crear un nuevo club |
| PUT | `/clubes/<id>` | Actualizar datos de un club |
| DELETE | `/clubes/<id>` | Eliminar un club (solo si no tiene equipos asociados) |
| POST | `/jugadores` | Crear un nuevo jugador |
| PUT | `/jugadores/<id>` | Actualizar datos de un jugador |
| DELETE | `/jugadores/<id>` | Eliminar un jugador |
| POST | `/partidos` | Cargar un resultado de partido |
| PUT | `/partidos/<id>` | Actualizar resultado de un partido |
| DELETE | `/partidos/<id>` | Eliminar un partido |
| POST | `/torneos` | Crear un nuevo torneo |
| PUT | `/torneos/<id>` | Actualizar datos de un torneo |
| DELETE | `/torneos/<id>` | Eliminar un torneo |

#### Endpoints adicionales (opcionales, suman punto)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/torneos/<id>/tabla` | Tabla de posiciones calculada (puntos, PJ, PG, PE, PP, GF, GC, DG) |
| GET | `/equipos/<id>/partidos` | Todos los partidos de un equipo (local y visitante) |
| GET | `/jugadores/<id>/trayectoria` | Todos los contratos del jugador con clubes y fechas |
| GET | `/mercado-pases` | Todos los traspasos con precio, ordenados por monto descendente |
| GET | `/estadisticas` | Estadísticas generales (ej: goleador por torneo, equipo con más títulos, etc.) |
| POST | `/equipos` | Inscribir un club en un torneo |
| PUT | `/equipos/<id>` | Actualizar inscripción (ej: cambiar grupo) |
| DELETE | `/equipos/<id>` | Dar de baja un equipo de un torneo |
| POST | `/contratos` | Registrar un nuevo contrato o pase |
| PUT | `/contratos/<id>` | Actualizar contrato |
| DELETE | `/contratos/<id>` | Cancelar un contrato |
| GET | `/provincias` | Lista todas las provincias. Filtro: `?pais_id=` |
| GET | `/ciudades` | Lista todas las ciudades. Filtro: `?provincia_id=` |

## Requisitos técnicos

- Usar **Python 3.11+**
- Usar **Flask** como framework web
- Usar **SQLite** como base de datos (no PostgreSQL, no MySQL)
- Los endpoints deben devolver **JSON**
- Manejar errores con códigos HTTP apropiados (404, 400, 500, 201)
- El proyecto debe poder ejecutarse con `python main.py`
- No usar bases de datos externas ni servicios en la nube
- El script `load_data.py` debe ser ejecutable de forma independiente para recargar los datos si es necesario

## Tips

- Empezá por el DER en papel. Es más fácil corregir relaciones antes de escribir código.
- Usá `flask run --debug` para recarga automática.
- Las relaciones muchos-a-muchos pueden necesitar tablas intermedias.
- Pensá en cómo vas a calcular la tabla de posiciones a partir de los partidos.
- Los precios de traspaso están en números enteros (sin decimales).
- El campo `fecha_fin` en `contratos.json` puede ser `null` → el jugador sigue activo en ese club.
- No modifiques los archivos JSON originales en `data/`. Si necesitás más datos, crealos aparte.
