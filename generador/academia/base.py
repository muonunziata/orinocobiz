"""Ayudantes de los cursos (ver __init__.py)."""


def L(t, r, p, dur='12 min'):
    return {'t': t, 'r': r, 'p': p, 'dur': dur}


def Q(tipo, q, o=None, sc=None, w=None, h=None, tf=None):
    return {'type': tipo, 'q': q, 'o': o, 'sc': sc, 'w': w, 'h': h, 'tf': tf}


AVISO = ('Contenido formativo general de la Academia Orinoco. Los requisitos legales, tributarios y sanitarios cambian: '
         'confírmelos siempre con el organismo competente antes de presentar un trámite.')
