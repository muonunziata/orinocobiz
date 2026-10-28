# Prompt para trabajar en el portal Orinoco (copiar y pegar en Claude)

```
Vamos a trabajar en el portal ORINOCO BUSINESS & INVESTMENT, hecho con Wakoo/Elementor.

1. El repositorio es github.com/muonunziata/wakoo (rama main). Todo el portal está en .
2. Antes de hacer nada, lee entera BITACORA.md (qué es, cómo está hecho, pendientes e historial),
   el CLAUDE.md de la raíz (reglas de Wakoo) y los documentos de docs/.
3. Regla fija: TODO cambio se anota en BITACORA.md en el mismo commit: una entrada nueva arriba del
   «Historial» con la fecha, qué se pidió, qué se cambió, en qué archivos y qué falta. Si se resuelve un pendiente,
   actualiza también esa sección.
4. Cómo se trabaja:
   - Los textos están en generador/content.py y salen de la ponencia del 21/10/2026. No inventes cifras, empresas,
     contactos, permisos ni coordenadas. Si algo no tiene fuente, se queda «Por definir» o «Pendiente de validación oficial».
   - Las páginas se cambian en generador/build.py y el diseño en generador/pack/styles/orinoco.css. Luego se rehace
     el paquete con generador/make.sh → orinoco-wakoo.zip y se prueba con generador/importar.mjs en el WordPress de prueba.
   - Los widgets del portal son del módulo Wakoo «Territorio» (wakoo/modules/territorio). Si cambian: nueva alpha,
     línea en CHANGELOG.md y en la BITACORA.md de la raíz, e instaladores.
   - El español es el maestro. El inglés se crea con Wakoo → Idiomas + Traductor.
   - Prueba en escritorio, tablet y móvil antes de subir.
5. Al terminar cada cambio: actualiza la bitácora, haz commit en español y súbelo a main.

Empieza leyendo la bitácora y dime en pocas líneas en qué estado está el portal y qué hay pendiente.
```
