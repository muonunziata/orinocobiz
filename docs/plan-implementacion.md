# Plan de implementación: ORINOCO BUSINESS & INVESTMENT

## Fase 0: hecho (28/10/2026)

- Módulos Wakoo **Territorio** (16 widgets) e **Inmersivo** (Globo 3D y fondo topográfico), en Wakoo alpha69.
- Paquete `orinoco-wakoo.zip`: 34 páginas en español, cabecera, pie, 3 plantillas de ficha, menú, 10 sectores, 3 municipios, 5 escuelas, 8 proyectos, 11 indicadores y 11 cursos (10 en diseño y 1 de demostración).
- Probado en el WordPress de prueba: importación, escritorio, tablet, móvil, editor de Elementor, y el flujo completo de registro → solicitud ORI-SOL → inscripción → lección → examen → certificado → verificación.

## Fase 1: puesta en línea (1 a 2 semanas)

1. Hosting con WordPress 6.x, PHP 8.1 o superior, HTTPS, copias diarias y correo SMTP.
2. Instalar Elementor (gratis) y Wakoo alpha69 o superior. Importar `orinoco-wakoo.zip` en Wakoo → Exportar / importar.
3. Crear las cuentas del equipo con sus roles. No usar la cuenta de administrador para el trabajo diario.
4. Configurar en Wakoo → Territorio: estados de tramitación, requisitos y emisor de certificados. En la página Contacto, abrir el widget Formulario y poner el correo que recibe los mensajes.
5. Revisar con el equipo legal Privacidad, Términos y Accesibilidad.
6. Confirmar los permisos de las fotos del PDF.

## Fase 2: validaciones de la ponencia (lo hace el cliente)

| Validación | Qué desbloquea en el portal |
|---|---|
| Territorial: cartografía, superficie, población, terrenos | Capas del mapa (importar GeoJSON/CSV con fuente), coordenadas de proyectos con «ubicación verificada», cifras de la portada sin la marca «pendiente» |
| Empresarial: demanda, proyectos activos, contactos | Necesidades de compra reales, primeras empresas verificadas |
| Jurídica y tributaria | Página de incentivos con lo que sí es procedente |
| Financiera | Montos de inversión en las fichas, como «estimación» con su fuente o como «verificado» |

Además hay que decidir si existe un cuarto municipio (ver el análisis documental).

## Fase 3: inglés

Wakoo → Idiomas → Clonar al inglés, luego Wakoo → Traductor (prompt → JSON → vista previa → aplicar), y por último el selector de idioma en la cabecera. El español sigue siendo el maestro, y sus cambios se propagan solos.

## Fase 4: operación

- La ventanilla recibe solicitudes. El personal asigna, responde y cambia estados, y todo queda en la auditoría.
- El directorio modera las empresas y sube su nivel solo con evidencia.
- El observatorio carga las series manuales cuando haya línea base. Los indicadores automáticos se calculan solos.
- La academia abre los cursos en diseño cuando tengan docente, fechas y costo. Los cursos grandes pueden ir a Moodle con el enlace del curso.

## Riesgos

- Publicar cifras sin validar: el portal ya las marca, pero el equipo no debe quitar la marca sin fuente.
- Expectativas sobre la ventanilla: hay que repetir que orienta y no concede permisos.
- Datos personales: los archivos de expedientes y empresas son privados, y conviene una política de conservación.
