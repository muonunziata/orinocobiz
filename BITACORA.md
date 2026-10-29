# Bitácora: ORINOCO BUSINESS & INVESTMENT

Portal institucional de la Subregión Orinoco (sur de Anzoátegui, Venezuela), construido en Wakoo como paquete importable. Lema: «Donde el potencial se convierte en inversión y la inversión en prosperidad».

## Estado actual (29/10/2026)

- Paquete `orinoco-wakoo.zip` (≈2,1 MB, 381 elementos). Requiere Wakoo **alpha70**.
  - Contenido: 36 páginas por idioma en es (maestro), fr, en, zh-tw e it, con plantillas, menús, proyectos, indicadores, cursos y lecciones en cada idioma.
  - Además, 6 empresas públicas de referencia y los límites de referencia del mapa.
- Selector de idioma en la barra superior. Las traducciones son un **borrador de trabajo**: falta la revisión de una persona nativa. Las empresas y las capas del mapa solo están en español; en los listados de los otros idiomas, el resumen de cada empresa sale traducido.
- Hub administrativo en `/hub-administrativo/` (y su versión en cada idioma), solo para el equipo.
- Probado en el WordPress de prueba:
  - 200 páginas en 390, 820 y 1440 px;
  - el editor de Elementor;
  - los flujos de la ventanilla, la academia y el hub.

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
| `generador/traducciones.json` | Traducciones {español: {fr, en, it, zh-tw}} de todos los textos. `build.py` escribe `faltan-traducciones.json` si queda alguno sin traducir. |
| `generador/datos/interfaz-territorio.json` | Textos de la interfaz de los widgets Territorio que se traducen (van al paquete como `i18n`). |
| `generador/datos/limites-subregion.json` | Límites de referencia del globo y del mapa (Natural Earth, dominio público; municipios de C. E. Porto Tapiquén 2015 vía geoBoundaries, ODbL 1.0). |
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
- Revisión nativa de las traducciones fr, en, zh-tw e it (están en `generador/traducciones.json`).
- En el sitio real: entrar al hub y pulsar «Crear acceso para todas las empresas sin cuenta». Las claves se muestran una sola vez y se entregan por un canal seguro. Después hay que cambiar los correos provisionales `@correo-pendiente.invalid` por los oficiales.
- Las 6 empresas públicas son perfiles de referencia con fuentes públicas (sitios oficiales y Wikipedia): conviene que cada empresa los confirme.
- Capas del mapa y coordenadas de proyectos (solo con fuente).
- Repositorio aparte `muonunziata/orinocobiz`: se sube cuando exista.

## Historial

### 29/10/2026: idiomas, hub, empresas públicas, cursos en iconos (Wakoo alpha70)
- **Pedidos de michele:**
  1. Arreglar el header. La barra superior estaba recortada; ahora la cabecera es flotante con el efecto «Compactar» y una barra de progreso.
  2. Traducir a los idiomas del proyecto.
  3. Que al pasar el ratón el globo haga zoom al mapa de Anzoátegui.
  4. El mapa de la subregión salía vacío.
  5. Registrar 6 empresas públicas de la zona.
  6. Cursos en iconos con ventana emergente, y un sitio responsive.
  7. Un hub administrativo con usuarios de WordPress, con alta de usuarios y acceso para las empresas con clave temporal.
- **Hecho:**
  - Cabecera: `wakoo_sticky_fx = condense` y una barra de progreso dorada; la barra superior lleva enlaces y el selector de idioma.
  - Globo: «Zoom al mapa» con el estado y los 3 municipios (límites de referencia, con su fuente).
  - Mapa SIG: capas de referencia «Límite del estado» y «Municipios», y el río Orinoco.
  - Empresas: PDVSA, Petropiar, Petrocedeño, Maderas del Orinoco, Corpoelec e Hidrocaribe.
    - Tienen el nivel «Perfil de referencia» y sus fuentes públicas.
    - Solo se pusieron los datos que dan esas fuentes; la web solo donde es oficial (pdvsa.com, corpoelec.gob.ve).
    - El formulario de contacto queda cerrado hasta que cada empresa tenga su cuenta.
  - Academia: escuelas en cajas de icono (5 columnas) y cursos en iconos con ventana emergente. El bloque pasó de unos 2.400 px a 552 px en escritorio.
  - Responsive: en la portada en móvil, los sectores van a 2 columnas y la cartera es un carrusel horizontal; la página pasó de 24.579 a 19.017 px. Las etapas de los proyectos van en vertical. Se revisaron 60 páginas en 3 anchos.
  - Hub: página «Hub administrativo» con el widget nuevo. Las claves **no** están en el paquete ni en el repositorio: se generan en el sitio al pulsar «Crear acceso».
  - Idiomas:
    - `build.py` genera cada página, plantilla, menú, proyecto, indicador, curso y lección en fr, en, zh-tw e it a partir de `traducciones.json` (1.458 textos);
    - el slug es traducido en fr, en e it; zh-tw mantiene el slug español;
    - la interfaz de los widgets va en `i18n`.
  - Arreglo de Wakoo: el error de consola para los administradores conectados (script de instantánea).
- **Probado:**
  - importación (381 elementos);
  - 140 páginas traducidas y las fichas: idioma, selector, sin errores ni desbordes;
  - el editor en inglés;
  - el hub completo con cuentas de prueba locales.
- **Archivos:**
  - `generador/build.py`, `generador/content.py`, `generador/traducciones.json`;
  - `generador/datos/interfaz-territorio.json`, `generador/datos/limites-subregion.json`;
  - `generador/pack/styles/orinoco.css`, `docs/modelo-datos.md`, `orinoco-wakoo.zip`.

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
- **Archivos:** `proyectos/orinocobiz/` completo, `wakoo/modules/territorio/`, `wakoo/modules/immersive/`, `wakoo/modules/responsive/assets/responsive.css`, `wakoo/classes/dashboard.php` y `wakoo/modules/portable/module.php`.
