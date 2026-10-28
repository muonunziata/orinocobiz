# Arquitectura: ORINOCO BUSINESS & INVESTMENT

## Piezas

```
WordPress + Elementor (gratis) + Wakoo (alpha69 o superior)
 ├─ Páginas (34): contenido de Elementor, editable con arrastrar y soltar
 ├─ Plantillas: cabecera, pie, ficha de proyecto, ficha de empresa, ficha de curso
 ├─ Módulo Wakoo «Territorio»  (wakoo/modules/territorio)
 │    proyectos · ventanilla · directorio B2B y marketplace · mapa SIG · observatorio · academia
 ├─ Módulo Wakoo «Inmersivo»   (wakoo/modules/immersive)
 │    Globo 3D (COBE, MIT) y fondo topográfico animado para contenedores
 └─ Otros módulos Wakoo: formularios (wakoo-form), menú, SEO, idiomas, portable (importar/exportar)
```

El sitio se entrega como **paquete Wakoo** (`orinoco-wakoo.zip`). Se importa en Wakoo → Exportar / importar, y el importador crea las páginas, las plantillas, el menú, los términos (sectores, municipios, capas, escuelas), los proyectos, los indicadores y los cursos, y aplica los ajustes del módulo Territorio.

## Páginas

| Grupo | Páginas |
|---|---|
| Institución | Inicio, Presentación y visión, Territorio y municipios, Desarrollo sostenible, Gobernanza e inversión, Documentos, Noticias, Contacto |
| Sectores | Sectores + 10 páginas hijas (una por sector) |
| Herramientas | Proyectos, Ventanilla única, Mapa del territorio, Directorio B2B, Proveedores, Observatorio, Academia |
| Cuenta | Acceso, Mis solicitudes, Mi empresa, Mi aprendizaje, Verificar certificado |
| Legales | Privacidad, Términos de uso, Accesibilidad |

## Widgets nuevos de Wakoo (categoría «Territorio»)

| Widget | Para qué |
|---|---|
| Cartera de proyectos (`wakoo-t-projects`) | Catálogo con buscador, filtros, columnas y paginación opcional |
| Ficha de proyecto (`wakoo-t-project`) | Ficha estandarizada: etapa, inversión estimada o verificada, datos pendientes |
| Etapas de la cartera (`wakoo-t-stages`) | Cuántos proyectos hay en cada uno de los 7 estados |
| Formulario de ventanilla (`wakoo-t-caseform`) | Registrar una iniciativa, con código único ORI-SOL |
| Mis solicitudes (`wakoo-t-cases`) | Panel del solicitante: estado, mensajes y archivos privados |
| Acceso (`wakoo-t-access`) | Entrar o registrarse sin pasar por wp-admin |
| Directorio B2B (`wakoo-t-companies`) | Empresas publicadas, con nivel de verificación |
| Ficha de empresa (`wakoo-t-company`) | Perfil público con los datos que el titular autorizó |
| Mi empresa (`wakoo-t-companypanel`) | Alta y edición de la empresa, documentos privados |
| Necesidades de compra (`wakoo-t-needs`) | Necesidades publicadas y solicitudes de cotización |
| Mapa SIG (`wakoo-t-gis`) | Leaflet + OpenStreetMap, capas públicas y proyectos con ubicación verificada |
| Observatorio (`wakoo-t-observatory`) | Indicadores con ficha técnica, gráfico y tabla de datos |
| Cursos (`wakoo-t-courses`) | Oferta de la academia agrupada por escuela |
| Curso (`wakoo-t-course`) | Ficha, inscripción, lecciones, examen, progreso y certificado |
| Mi aprendizaje (`wakoo-t-student`) | Cursos y certificados del alumno |
| Verificar certificado (`wakoo-t-verify`) | Consulta pública por código |

Módulo Inmersivo: **Globo 3D** (`wakoo-globe`) y el ajuste **Fondo topográfico** en la pestaña Avanzado de cualquier contenedor.

## Roles

Editor institucional, Gestor de proyectos, Gestor de proveedores, Coordinador académico, Docente y Analista del observatorio. Cada uno ve solo sus tipos de contenido. El administrador lo ve todo, incluida la auditoría.

## Seguridad

- Sin contraseñas por defecto ni claves en el código. El registro público crea usuarios con rol «suscriptor».
- Los formularios usan nonce, saneado, límite de intentos (verificación de certificados) y tipos de archivo permitidos (PDF, imágenes, ofimática, CSV, ZIP).
- Los archivos privados de expedientes y empresas se sirven solo a su titular y al personal autorizado.
- Bitácora de auditoría en la tabla `wp_wakoo_tlog`, con visibilidad pública, interna o de auditoría.
- Las notas internas del personal nunca se muestran al solicitante.

## Accesibilidad (WCAG 2.2 AA)

- Contraste AA: el dorado #C5A15B solo se usa como acento sobre fondo oscuro. Sobre blanco, el texto dorado usa #7E5F22.
- Foco visible, avisos con `role="status"` que reciben el foco, campos obligatorios con mensaje accesible.
- El gráfico del observatorio trae siempre su tabla de datos. Los puntos sin verificar se distinguen por la forma, no solo por el color.
- `prefers-reduced-motion` desactiva el globo, el fondo topográfico y las animaciones de entrada.

## Idiomas

El español es el maestro. El inglés está declarado en el paquete (`languages: [es, en]`), y sus páginas se crean después con Wakoo → Idiomas → Clonar, más el flujo Traductor. Luego se añade el selector de idioma a la cabecera.

## Moodle

Cada curso admite un enlace a un aula Moodle externa. El LMS de Wakoo es el MVP (producto mínimo viable), y Moodle es la opción para cursos más grandes.
