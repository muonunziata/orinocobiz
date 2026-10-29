# ORINOCO BUSINESS & INVESTMENT: portal en Wakoo

Portal institucional de la Subregión Orinoco (sur de Anzoátegui), hecho a partir de la ponencia del 21/10/2026. Todo se edita con arrastrar y soltar en Elementor (gratis) más Wakoo.

| Qué | Dónde |
|---|---|
| Paquete listo para importar | `orinoco-wakoo.zip` |
| Generador (textos, páginas, estilos) | `generador/` (`content.py`, `build.py`, `pack/styles/orinoco.css`) |
| Documentación | `docs/` (análisis documental, arquitectura, modelo de datos y plan de implementación) |
| Historial de cambios | `BITACORA.md` |
| Prompt para el socio | `PROMPT-SOCIO.md` |

## Instalar

1. WordPress + Elementor (gratis) + Wakoo **alpha71 o superior** (`instaladores/` en la raíz del repositorio).
2. Wakoo → Exportar / importar → subir `orinoco-wakoo.zip`.
3. Ajustes → Lectura ya queda con «Inicio» como portada. Revisa Wakoo → Territorio (estados, requisitos y emisor de certificados).

## Rehacer el paquete

```bash
cd proyectos/orinocobiz/generador
./make.sh                                   # → ../orinoco-wakoo.zip
node importar.mjs ../orinoco-wakoo.zip      # lo importa en el WordPress de prueba (localhost:8080)
```

Los textos salen de la ponencia: no se añaden cifras, empresas, contactos ni coordenadas que no tengan fuente.
