"""Cursos de la Academia Orinoco (widgets «Wakoo · Academia», Wakoo alpha79+).

Fuente única del contenido de los 10 cursos de las cinco escuelas. El español es el maestro: build.py lo traduce con
traducciones.json como el resto del sitio (lo que falte queda en español y se anota en faltan-traducciones.json).

Cada curso: clave, escuela (slug de C.SCHOOLS), título, lema, nivel, horas, insignia, a quién va dirigido, requisitos,
objetivos y competencias (para la ficha del curso), 6 lecciones y una evaluación con casos.
Cada lección: título, resumen (HTML sencillo: <p>, <ul>, <li>, <strong>), práctica aplicada y duración estimada de lectura.

Tipos de pregunta (widget Evaluación interactiva): one, many, tf, order, match, scale, reflect.
Respuestas: una por línea, las correctas con * delante; order = líneas en el orden correcto; match = «a = b».

Reglas de contenido: formación general y práctica. No se inventan cifras, plazos ni requisitos oficiales: cuando un
trámite depende de un organismo, se nombra el organismo y se pide confirmar el requisito vigente con él.
"""
from .base import L, Q, AVISO  # noqa: F401
from .cursos_a import CURSOS_A
from .cursos_b import CURSOS_B


def cursos():
    out = CURSOS_A + CURSOS_B
    for c in out:
        assert len(c['lecciones']) == 6, c['clave']
        assert len(c['evaluacion']) >= 8, c['clave']
    return out
