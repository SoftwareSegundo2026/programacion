# Frontend Design Specification

## 1. Objetivo del frontend

El frontend debe convertir el backend de FastAPI en una aplicación web administrativa para gestión musical. La interfaz será usada para autenticar usuarios, administrar el catálogo y operar los CRUD de artistas, álbumes, géneros, tracks y usuarios.

El producto debe sentirse como un panel serio, claro y rápido de usar. La prioridad es facilitar la gestión de datos y mantener una navegación simple entre entidades relacionadas.

## 2. Rol del frontend dentro del producto

Este frontend se diseña como una capa de operación sobre la API existente. No reemplaza la lógica del backend: consume sus endpoints y organiza la experiencia para que un usuario pueda:

- Iniciar sesión con JWT.
- Registrarse si la política del proyecto lo permite.
- Recuperar su contraseña.
- Consultar, crear, editar y eliminar registros.
- Navegar entre entidades relacionadas sin perder contexto.

## 3. Perfiles de usuario

### Administrador

- Accede a todo el catálogo.
- Administra usuarios.
- Puede crear, editar y eliminar entidades.

### Editor de catálogo

- Gestiona artistas, álbumes, géneros y tracks.
- Tiene acceso de lectura a usuarios.

### Usuario lector

- Consulta información del catálogo.
- Puede quedar restringido a lectura según la regla de negocio final.

## 4. Principios de UX

- Priorizar una estructura tipo dashboard con navegación lateral.
- Reducir la fricción en formularios largos usando secciones claras y validación inmediata.
- Mostrar relación entre entidades de forma visible, especialmente artista-albún-track.
- Evitar pantallas vacías o ambiguas: cada vista debe tener estado inicial, carga, error y vacío.
- Mantener consistencia de acciones: crear, editar, eliminar, buscar y paginar deben verse iguales en todas las entidades.

## 5. Dirección visual

La interfaz debe tener una identidad moderna, editorial y ligeramente cinematográfica, relacionada con música y gestión de datos.

### Sensación general

- Profesional, sobria y contemporánea.
- Panel administrativo con personalidad.
- Evitar el look genérico de plantilla SaaS sin identidad.

### Propuesta estética

- Fondo base oscuro o neutro profundo con superficies elevadas para tarjetas y paneles.
- Acento principal en un color vivo y reconocible para acciones primarias.
- Un segundo acento para estados y etiquetas de contexto.
- Tipografía de título con presencia y cuerpo legible para listas densas.
- Bordes redondeados moderados y sombras suaves.

### Componentes visuales clave

- Header superior compacto con búsqueda global y perfil.
- Sidebar con navegación por módulos.
- Tarjetas resumen para métricas.
- Tablas densas pero aireadas.
- Formularios por panel o modal según complejidad.
- Chips o badges para relaciones, estado activo/inactivo y tipos de contenido.

## 6. Arquitectura de información

### Navegación principal

- Dashboard
- Artistas
- Álbumes
- Géneros
- Tracks
- Usuarios
- Login
- Register
- Reset Password

### Estructura de pantallas

1. Autenticación.
2. Dashboard de inicio.
3. Listado de entidades.
4. Formulario de creación.
5. Formulario de edición.
6. Vista de detalle.
7. Gestión de usuarios.
8. Flujos de recuperación de acceso.

## 7. Pantallas requeridas

### 7.1 Login

Objetivo: autenticar al usuario y obtener el token JWT.

Elementos:

- Logo o marca del sistema.
- Campo de usuario o correo.
- Campo de contraseña.
- Botón principal de acceso.
- Enlace a registro.
- Enlace a reset de contraseña.
- Mensajes de error claros para credenciales inválidas.

Estados:

- Cargando al enviar.
- Error por credenciales incorrectas.
- Error por usuario inactivo.
- Acceso exitoso con redirección al dashboard.

### 7.2 Register

Objetivo: crear una cuenta nueva si el proyecto habilita auto-registro.

Elementos:

- Nombre de usuario.
- Correo electrónico.
- Nombre completo.
- Contraseña.
- Confirmación de contraseña.
- Botón de registro.

Estados:

- Validación en tiempo real.
- Error por usuario o email existente.
- Confirmación de registro exitoso.

### 7.3 Reset Password

Objetivo: permitir recuperación de acceso.

Elementos:

- Campo de correo electrónico.
- Paso de verificación si el flujo final lo requiere.
- Campo para nueva contraseña.
- Confirmación de nueva contraseña.

Estados:

- Solicitud enviada.
- Token o código inválido.
- Contraseña actualizada correctamente.

### 7.4 Dashboard

Objetivo: mostrar una visión general del sistema.

Bloques sugeridos:

- Cantidad de artistas.
- Cantidad de álbumes.
- Cantidad de géneros.
- Cantidad de tracks.
- Accesos rápidos a creación.
- Actividad reciente o resumen operativo.

### 7.5 Artistas

#### Listado

- Tabla con ID y nombre.
- Búsqueda por nombre.
- Paginación.
- Botón de crear artista.
- Acciones por fila: ver, editar, eliminar.

#### Crear / editar

- Nombre del artista.
- Validación obligatoria.
- Confirmación antes de eliminar.

#### Detalle

- Identificador.
- Nombre.
- Relación con álbumes asociados.

### 7.6 Álbumes

#### Listado

- Tabla con título, artista y acciones.
- Acceso a detalle por álbum.

#### Crear / editar

- Título del álbum.
- Selector de artista con búsqueda.
- Vista del nombre del artista seleccionado.

#### Detalle

- Título.
- Artista asociado.
- Lista de tracks vinculados.

### 7.7 Géneros

#### Listado

- Tabla simple con nombre y acciones.

#### Crear / editar

- Campo único de nombre.

#### Detalle

- Nombre.
- Tracks asociados.

### 7.8 Tracks

#### Listado

- Tabla con nombre, álbum, género, media type, duración y precio.
- Filtros opcionales por álbum, género o media type.
- Paginación.

#### Crear / editar

- Nombre.
- Álbum opcional.
- Media type obligatorio.
- Género opcional.
- Compositor.
- Milisegundos.
- Bytes.
- Precio unitario.

#### Detalle

- Datos principales.
- Nombres relacionados: álbum, género y media type.

### 7.9 Usuarios

#### Listado

- Username.
- Email.
- Nombre completo.
- Estado activo o inactivo.

#### Crear

- Username.
- Email.
- Nombre completo.
- Contraseña.
- Estado de activación.

## 8. Jerarquía de navegación

### Navegación propuesta

- Pantalla inicial luego de login: Dashboard.
- Desde Dashboard se accede a cualquier módulo.
- Cada módulo tiene listado, detalle y formulario.
- Los formularios de edición deben conservar la navegación de regreso al listado o detalle.

### Relaciones de navegación

- Desde un artista se puede ir a sus álbumes.
- Desde un álbum se puede ir a sus tracks.
- Desde un track se puede consultar su álbum, género y media type.
- Desde un usuario se puede consultar su estado y rol visual si aplica.

## 9. Tareas a asignar al equipo frontend

Estas tareas están ordenadas como un plan de trabajo para construcción del frontend.

### Fase 1: Base del proyecto

- Definir layout global con sidebar, header y área de contenido.
- Configurar router y protección de rutas privadas.
- Crear cliente HTTP para consumir la API.
- Implementar manejo de tokens en almacenamiento seguro acorde a la arquitectura elegida.
- Establecer sistema de notificaciones y manejo centralizado de errores.

### Fase 2: Autenticación

- Construir pantalla de login.
- Construir pantalla de registro.
- Construir flujo de reset password.
- Implementar guardas de sesión y logout.
- Redireccionar correctamente según autenticación.

### Fase 3: Dashboard

- Diseñar la pantalla principal.
- Mostrar métricas de catálogo.
- Agregar accesos rápidos a altas frecuentes.
- Crear estados vacíos y de carga.

### Fase 4: CRUD de catálogo

- Implementar CRUD de artistas.
- Implementar CRUD de álbumes.
- Implementar CRUD de géneros.
- Implementar CRUD de tracks.
- Reutilizar patrones de tabla, formulario y detalle.

### Fase 5: Usuarios y administración

- Implementar listado de usuarios.
- Implementar creación de usuarios.
- Mostrar estados de activación.

### Fase 6: Pulido

- Validaciones y mensajes de formulario.
- Responsive design para tablet y móvil.
- Estados de error, vacío y loading.
- Accesibilidad básica y foco visible.
- QA visual final.

## 10. Componentes reutilizables

El frontend debe construirse con componentes compartidos para evitar duplicación.

### Componentes base

- Button
- Input
- Select
- TextArea
- Modal
- Drawer o panel lateral
- Badge
- Table
- Pagination
- SearchBar
- Breadcrumb
- Toast o alert
- EmptyState
- LoadingSkeleton

### Componentes de dominio

- EntityTable
- EntityForm
- EntityDetailHeader
- RelationChip
- DeleteConfirmDialog
- AuthCard

## 11. Estados de interfaz

Cada pantalla CRUD debe contemplar estos estados:

- Cargando datos.
- Datos disponibles.
- Sin resultados.
- Error de red o API.
- Acciones en progreso.
- Eliminación confirmada.

## 12. Reglas de formularios

- Validar campos obligatorios antes de enviar.
- Resaltar errores por campo, no solo a nivel global.
- Mantener el botón principal deshabilitado mientras se procesa la petición.
- Confirmar acciones destructivas como eliminar.
- Al editar, precargar valores actuales del registro.

## 13. Criterios de aceptación visual

- La app debe verse consistente en todas las entidades.
- Login, register y reset password deben sentirse parte del mismo producto.
- Las listas deben ser fáciles de escanear.
- Las relaciones entre entidades deben ser visibles en álbumes y tracks.
- El usuario debe entender rápidamente dónde está y qué puede hacer.

## 14. Entregable esperado para Stitch

Este archivo debe servir como entrada para generar el sistema visual y las pantallas base en Stitch. La prioridad es que Stitch entienda:

- Qué producto se está diseñando.
- Qué pantallas deben existir.
- Qué componentes deben reutilizarse.
- Qué jerarquía visual y navegación necesita la app.
- Qué flujo de autenticación y CRUD debe soportar.

## 15. Resumen ejecutivo para el equipo

El frontend debe construirse como un panel de administración musical con autenticación, registro, recuperación de contraseña y CRUD completo para las entidades del backend. El diseño debe transmitir orden, densidad de información y facilidad operativa. La implementación debe priorizar reutilización de componentes, claridad de navegación y consistencia en formularios, tablas y estados.