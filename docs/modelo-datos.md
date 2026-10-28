# Modelo de datos: ORINOCO BUSINESS & INVESTMENT

Todo se guarda en WordPress, en tipos de contenido propios del módulo Wakoo **Territorio**, campos meta con el prefijo `_wakoo_t_`, taxonomías y una tabla de bitácora. Ningún dato vive fuera del sitio.

## Tipos de contenido

| Tipo | Qué es | Público | Campos principales |
|---|---|---|---|
| `wakoo_project` | Proyecto de la cartera | Sí (publicado) | code (ORI-Pxx), stage (7 estados), scale, objective, location, lat/lng + geo_ok + geo_source, amount + currency + amount_kind (estimación / verificado) + amount_src + amount_date, infra, market, permits, studies, jobs, risks, timeline, precond, responsible, docs, source, pending |
| `wakoo_case` | Expediente de la ventanilla | No (privado) | código ORI-SOL, estado configurable, solicitante, persona asignada, sector, municipio, archivos privados, mensajes |
| `wakoo_company` | Empresa del directorio | Solo tras moderación | level (registrada / verificada / homologada), homologated, legal_name, rif (privado), products, capabilities, equipment, certs, web/email/phone/address (se publican solo si el titular lo autoriza) |
| `wakoo_need` | Necesidad de compra | Sí | company, qty, deadline, closed |
| `wakoo_rfq` | Solicitud de cotización | No | empresa, necesidad, mensaje |
| `wakoo_geo` | Elemento del mapa | Según `public` | lat/lng, geojson, public, verified, source, date, url |
| `wakoo_indicator` | Indicador del observatorio | Según `public` | auto (automático o manual), group, unit, source, updated, period, owner, method, check (verificado / pendiente), chart, demo, series («periodo;valor;si/no») |
| `wakoo_course` | Curso de la academia | Sí | estado (en diseño / abierto…), mode, duración, cost, certify, moodle, demo |
| `wakoo_lesson` | Lección | Para inscritos | course, video, material, quiz (JSON), pass |
| `wakoo_cert` | Certificado | Verificable por código | course, alumno, código, fecha |

## Taxonomías

| Taxonomía | Se usa en | Términos que trae el paquete |
|---|---|---|
| `wakoo_sector` | proyectos, expedientes, empresas, necesidades, mapa, indicadores | los 10 sectores de la ponencia |
| `wakoo_municipio` | lo mismo | Independencia, José Gregorio Monagas, Francisco de Miranda |
| `wakoo_company_cat` | empresas | — |
| `wakoo_geo_layer` | mapa (meta wk_order, wk_color, wk_public) | capas vacías (se llenan al importar GeoJSON/CSV con fuente) |
| `wakoo_school` | cursos | las 5 escuelas |

## Bitácora y auditoría

Tabla `wp_wakoo_tlog`: `id, obj_type, obj_id, kind, vis, user_id, message, who, created`.
- `vis = public`: la ven el solicitante y el personal (mensajes, cambios de estado).
- `vis = internal`: solo el personal (notas internas).
- `vis = audit`: solo la pantalla de auditoría (quién cambió qué y cuándo).

## Datos de usuario

- `_wakoo_t_courses` (user meta): cursos en los que está inscrito.
- `_wakoo_t_prog_<curso>` (user meta): lecciones completadas y notas.

## Ajustes

Opción `wakoo_territorio`: prefijo de códigos (ORI), estados de tramitación (`clave|Nombre|cerrado`), requisitos, centro y zoom del mapa (8.4, -64.3, zoom 8, una referencia aproximada de la subregión y no un dato), plantillas de ficha, páginas clave y emisor de certificados.

## Datos de prueba

El paquete trae una sola serie de prueba en el observatorio («Serie de prueba del observatorio»), marcada `demo`. No aparece en el sitio salvo que se active «Mostrar datos de prueba» en el widget, y en ese caso sale gris, punteada y rotulada como prueba. El curso de demostración está marcado como tal. Todo lo demás es contenido de la ponencia o queda vacío.
