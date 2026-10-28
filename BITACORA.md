# Bitácora: ORINOCO BUSINESS & INVESTMENT

Portal institucional de la Subregión Orinoco (sur de Anzoátegui, Venezuela), construido en Wakoo como paquete importable. Lema: «Donde el potencial se convierte en inversión y la inversión en prosperidad».

## Estado actual (28/10/2026)

- Paquete `orinoco-wakoo.zip` (≈1,6 MB): 34 páginas en español, plantillas, menú, proyectos, indicadores y cursos. Requiere Wakoo alpha69.
- Probado en el WordPress de prueba: importación, escritorio, tablet, móvil, editor y el flujo completo de la ventanilla y la academia.
- Idioma maestro: español. El inglés está declarado y se crea con Wakoo → Idiomas + Traductor (pendiente).

## Cómo está hecho

| Archivo | Qué contiene |
|---|---|
| `generador/content.py` | Todos los textos, tomados de la ponencia (fuente única). Si cambia un texto, se cambia aquí. |
| `generador/build.py` | Las páginas, las plantillas, el menú, los términos y el contenido (proyectos, indicadores, cursos y lecciones). |
| `generador/el.py` | Ayudantes que generan el JSON de Elementor (contenedores, títulos, botones, iconos…). Prefijo de clases `orn-`. |
| `generador/pack/styles/orinoco.css` | Sistema de diseño: tokens de color (#10355B, #174A7E, #C5A15B solo de acento, #F4F6F8, #465363), Inter, cabecera de cristal oscuro, tarjetas, paneles y la parte responsive. |
| `generador/pack/images/` | 10 imágenes sacadas del PDF (.webp) y el propio PDF de la ponencia. |
| `generador/pack/fonts/` | Inter 400/600/700 (OFL), con su licencia. |
| `generador/make.sh` | Genera `../orinoco-wakoo.zip`. |
| `generador/importar.mjs` | Importa el zip en el WordPress de prueba con Playwright. |
| `docs/` | Análisis documental, arquitectura, modelo de datos y plan de implementación. |

Widgets usados: los nativos de Elementor (Título, Editor de texto, Botón, Imagen, Icono, Lista de iconos, Caja de icono, Contador) y los de Wakoo (Menú, Formulario, Plantilla, Globo 3D, Eventos, Lista de entradas y los 16 de «Territorio»). No hay widgets HTML.

## Reglas de este proyecto

- No inventar estadísticas, empresas, terrenos, inversiones, permisos, contactos oficiales, coordenadas ni resultados.
- Toda cifra lleva su fuente y la marca «Pendiente de validación oficial» hasta que el cliente la valide.
- La ventanilla orienta y hace seguimiento: nunca se dice que concede permisos.
- No se usan logotipos ni escudos inventados (la marca es tipográfica) ni emojis como iconos (se usa Font Awesome 5).
- WCAG 2.2 AA: sobre blanco, el texto dorado usa #7E5F22.

## Pendientes

- Validaciones de la ponencia: territorial, empresarial, jurídica y financiera (ver `docs/plan-implementacion.md`).
- ¿3 o 4 municipios? La ponencia nombra 3. Falta confirmar si hay un cuarto.
- Permisos de las fotos del PDF y revisión legal de Privacidad, Términos y Accesibilidad.
- Versión en inglés y selector de idioma.
- Capas del mapa y coordenadas de proyectos (solo con fuente).
- Repositorio aparte `muonunziata/orinocobiz`: se sube cuando exista.

## Historial

### 28/10/2026: primera entrega (Wakoo alpha69)
- **Pedido:** crear en Wakoo el portal descrito en el «prompt maestro», con las imágenes del PDF y un diseño tecnológico e inmersivo pero institucional.
- **Hecho:**
  - Módulo Wakoo **Territorio**: proyectos, ventanilla, directorio B2B, necesidades, mapa SIG, observatorio, academia, acceso y verificación (16 widgets, 6 roles y auditoría).
  - Módulo Wakoo **Inmersivo**: Globo 3D y fondo topográfico.
  - Generador y paquete de 34 páginas.
  - Revisión visual: la cartera de la portada pasó a ancho completo con 4 columnas y sin paginación, y se corrigieron el hueco bajo la cabecera, el sufijo «km²» de los contadores, el borde doble de las fuentes y la alineación de la barra superior.
  - En móvil, los botones del hero van a todo el ancho.
- **Arreglos en Wakoo hechos por el camino:**
  - El control «Columnas» de la cartera no se aplicaba.
  - La redirección de activación rompía los formularios públicos.
  - El optimizador responsive sumaba relleno lateral en contenedores anidados en móvil.
- **Probado:** importación (73 elementos y 11 medios), consola sin errores, capturas en 1440, 820 y 390 px, editor de Elementor, y el flujo registro → ORI-SOL → curso → examen → certificado → verificación.
- **Archivos:** todo el repositorio orinocobiz (copia en la carpeta proyectos/orinocobiz de muonunziata/wakoo), `wakoo/modules/territorio/`, `wakoo/modules/immersive/`, `wakoo/modules/responsive/assets/responsive.css`, `wakoo/classes/dashboard.php` y `wakoo/modules/portable/module.php`.
