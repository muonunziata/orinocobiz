# Análisis documental: ORINOCO BUSINESS & INVESTMENT

Fuente única del contenido: la ponencia **ORINOCO BUSINESS & INVESTMENT FORUM** (PDF del 21/10/2026). Ella se basa en la *caracterización económica de la Subregión Orinoco* (20/10/2026). El PDF va dentro del paquete (`pack/images/ponencia-orinoco-business-2026-10-21.pdf`) y se publica en la página Documentos.

Regla aplicada en todo el portal: **no se inventa nada**. Ni estadísticas, ni empresas, ni terrenos, ni montos, ni permisos, ni contactos oficiales, ni coordenadas, ni resultados. Cuando la ponencia no da un dato, el portal dice «Por definir» o «Pendiente de validación oficial».

## 1. Qué se tomó del PDF y dónde está

Todo el texto vive en `generador/content.py`, que cita el apartado de la ponencia.

| Tema | Dónde aparece en el portal | Variable de `content.py` |
|---|---|---|
| Marca, subtítulo, lema y cierre | Cabecera, portada y pie | `BRAND`, `SUB`, `MOTTO`, `CLOSING` |
| Propósito, visión, posicionamiento, objetivos y 7 principios | Presentación y visión | `PURPOSE`, `VISION`, `POSITIONING`, `OBJECTIVES`, `PRINCIPLES` |
| Escalas (local, regional, nacional e internacional) | Presentación | `SCALES` |
| Territorio, límites y superficie de referencia (≈ 8.000 km²) | Territorio y municipios | `TERRITORY`, `AREA_NOTE` |
| 3 municipios y su especialización propuesta | Territorio | `MUNICIPIOS`, `MUN_NOTE` |
| Corredores viales, rutas internas y déficit vial | Territorio y Mapa | `CORRIDORS`, `RUTAS`, `ROAD_WARNING` |
| Río Orinoco, Caribe y Macapaima | Territorio y sector forestal | `RIVER`, `CARIBE`, `MACAPAIMA` |
| 10 sectores (relevancia, oportunidades, tipos de inversión, infraestructura, riesgos) | Sectores y sus 10 páginas | `SECTORS` |
| Cadena de proveeduría petrolera y energética, programa de proveedores y niveles | Proveedores | `CPPH`, `GRADUAL`, `SUPPLIER_PROGRAM`, `LEVELS` |
| Cartera inicial de 8 proyectos (ORI-P01 a P08) | Proyectos y sus fichas | `PROJECTS`, `PROJECT_NOTE` |
| Ficha estandarizada de 10 puntos y 7 estados | Proyectos | `SHEET_10`, `STAGES` |
| Ventanilla única: pasos y límites | Ventanilla única | `WINDOW_STEPS`, `WINDOW_NOTE`, `LOCATION_SERVICES` |
| Mesa de coordinación, contratos, indicadores institucionales | Gobernanza e inversión | `MESA_*`, `CONTRACT`, `INST_INDICATORS` |
| Fases, incentivos (como opciones de análisis) y matriz de servicios | Gobernanza | `PHASES`, `INCENTIVES`, `SERVICES_MATRIX` |
| Seguridad y sostenibilidad | Desarrollo sostenible | `SECURITY`, `SUSTAIN` |
| Formación: líneas, 5 escuelas | Academia | `TRAINING_LINES`, `SCHOOLS`, `ACADEMY_INTRO` |
| Las 4 validaciones pendientes | Portada y Documentos | `VALIDATIONS` |
| Indicadores de impacto (10.2) y de eficiencia (6.6) | Observatorio | `INDICATORS` |

## 2. Cifras que se publican (todas con su fuente y la marca «Pendiente de validación oficial»)

- 3 municipios: Independencia, José Gregorio Monagas y Francisco de Miranda.
- ≈ 8.000 km² de territorio de referencia.
- 631 km² potencialmente aprovechables para la agricultura.
- 10 sectores de oportunidad y 8 proyectos en la cartera inicial.
- 2 puentes sobre el Orinoco: Angostura y Orinoquia.

No se publica ningún monto de inversión, empleo, población ni producción. La ponencia no los da como dato verificado.

## 3. Lo que el portal NO afirma

- Que la ventanilla conceda permisos o apruebe proyectos. Solo orienta y hace seguimiento, y así se dice en la ventanilla, en las fichas y en el pie.
- Que los incentivos estén vigentes o sean jurídicamente procedentes (`INCENTIVES_NOTE`).
- Que exista ya una plataforma portuaria internacional (`RIVER`).
- Que la mesa de coordinación o los compromisos institucionales estén en marcha (`NOT_IN_FORCE`).
- Que ningún nivel del directorio garantice contratos (`SUPPLIER_NOTE`).
- Ubicaciones: ningún proyecto sale en el mapa hasta que alguien cargue coordenadas con fuente y marque «ubicación verificada».

## 4. Diferencias y dudas para validar con el cliente

1. **Municipios: 3 o 4.** El encargo hablaba de un cuarto municipio («Anzoátegui»). La ponencia solo nombra tres, y el portal sigue a la ponencia. Si hay un cuarto, se añade como término en Territorio → Municipios y en `MUNICIPIOS`.
2. **Contactos oficiales:** la ponencia no trae teléfonos, correos ni direcciones. La página Contacto usa solo el formulario de Wakoo, cuyo destinatario se configura en el panel.
3. **Logotipos y escudos:** no se usan. La marca es un logotipo tipográfico (ORINOCO / BUSINESS & INVESTMENT) hecho con texto.
4. **Imágenes:** las 10 fotos salen del PDF (ver sección 5). Una lleva el crédito visible «@miguelsayeghd» (puente Orinoquia), que se mantiene. Hay que confirmar con el cliente el permiso de uso de todas.
5. **Textos legales** (Privacidad, Términos, Accesibilidad): son borradores marcados «pendiente de revisión legal».

## 5. Imágenes extraídas del PDF

| Archivo | Contenido | Uso |
|---|---|---|
| `puente-angostura.webp` | Puente Angostura | Territorio, corredor El Tigre – Ciudad Bolívar |
| `puente-orinoquia.webp` | Puente Orinoquia (crédito @miguelsayeghd) | Corredor El Tigre – Puerto Ordaz |
| `embarcadero-flotante.webp` | Embarcadero artesanal | Accesos fluviales y logística |
| `cultivos-yuca-maiz.webp` | Cultivos | Agricultura |
| `pesca-acuicultura.webp` | Pesca artesanal | Pesca y acuicultura |
| `plantacion-forestal-uverito.webp` | Plantación forestal | Forestal y sostenibilidad |
| `taller-metalmecanico.webp` | Taller metalmecánico | Industria, Directorio B2B |
| `operaciones-planta-energia.webp` | Planta energética | Petróleo, energía y servicios |
| `rio-curiaras.webp` | Río | Turismo y naturaleza |
| `franja-territorio.webp` | Ilustración de portada recortada, sin los logotipos | Fondo de la banda de visión |
