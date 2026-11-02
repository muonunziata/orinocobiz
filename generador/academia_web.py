"""Academia Orinoco con el módulo «Wakoo · Academia» (Wakoo alpha81+): portada, una página por curso, Mi aprendizaje y el certificado.

Cada página de curso lleva la Cabecera del curso (que la convierte en curso, con su guía en PDF), una ficha hecha con widgets
nativos (objetivos, a quién va dirigido, requisitos, modalidad, certificado y competencias), el Temario, el Aula (6 lecciones
con práctica) y la Evaluación interactiva con casos. El contenido sale de academia/*.py; las portadas, de portadas_academia.py.

Los textos de los widgets de la Academia se dejan con su valor por defecto (en español): en las páginas de otros idiomas los
traduce Wakoo con el diccionario de la interfaz (site.territorio.i18n, que build.py llena con datos/interfaz-territorio.json).
build.py llama a bind(globals()) para prestar sus ayudantes (L, pagehead, section, panel…).
"""
import academia
from academia.palabras import words
import content as C
from el import w, h, p, col, row, grid, eyebrow, btn, btns, iconlist, iconbox, img, lnk, eid, con

B = None
ACCENT = {'accent': '#10355B', 'radius': {'unit': 'px', 'size': 12}}
CURSOS = academia.cursos()
SCHOOL = {sc['slug']: sc for sc in C.SCHOOLS}
MODALIDAD = 'En línea y a su ritmo, con guía en PDF para estudiar sin conexión'
CERT = 'Certificado con código verificable al aprobar la evaluación final (70 % o más)'


def bind(ns):
    global B

    class _B:
        pass
    B = _B()
    B.__dict__.update(ns)


def school(c):
    return SCHOOL[c['escuela']]


def cover(c):
    return 'academia/' + c['clave'] + '.webp'


def cert_link():
    return lnk(B.L('verificar'), False)


def cabecera(c):
    return w('wakoo-ac-cabecera', {
        'clave': c['clave'], 'titulo': c['titulo'], 'lema': c['lema'], 'cat': school(c)['name'], 'nivel': c['nivel'],
        'autora': 'Academia Orinoco', 'insignia': c['insignia'], 'img': {'url': img(cover(c)), 'id': ''},
        'horas': f"{c['horas']} horas", 'guia': 'yes', 'guia_nota': academia.AVISO,
        'orden': c['orden'], 'target': '#aula', 'layout': 'split', **words('cabecera'), **ACCENT}, 'orn-ac-head')


def ficha(c):
    """Ficha del curso con widgets nativos: todo editable con el ratón."""
    sc = school(c)
    left = col([
        B.panel([iconlist([(o, 'fas fa-check-circle', None) for o in c['objetivos']], 'orn-bullets orn-ac-obj')], 'Al terminar el curso podrá', 'fas fa-bullseye'),
        B.panel([iconlist([(x, 'fas fa-award', None) for x in c['competencias']], 'orn-ac-skills', inline=True)], 'Competencias que trabaja', 'fas fa-medal'),
    ], 'orn-ac-ficha__main', gap=20)
    right = B.panel([B.defs([('A quién va dirigido', c['dirigido']), ('Requisitos', c['requisitos']), ('Duración', f"{c['horas']} horas de estudio y práctica · 6 lecciones"),
                             ('Nivel', c['nivel']), ('Modalidad', MODALIDAD), ('Certificado', CERT), ('Escuela', sc['name'])])],
                    'Ficha del curso', 'fas fa-clipboard-list', 'orn-ac-ficha__side')
    return B.section([grid([left, right], 2, tablet=1, mobile=1, gap=24, cls='orn-ac-ficha')], cls='orn-sec orn-sec--tight orn-ac-sec')


def aula(c):
    lessons = [{'_id': eid(), 'title': l['t'], 'dur': l['dur'], 'video': {'url': ''}, 'file': {'url': '', 'id': ''}, 'poster': {'url': '', 'id': ''},
                'summary': l['r'], 'practice': l['p'], 'res_label': '', 'res_link': {'url': ''}, 'free': 'yes' if i == 0 else ''}
               for i, l in enumerate(c['lecciones'])]
    return con([w('wakoo-ac-aula', {'lessons': lessons, 'auto_next': 'yes', 'quiz_anchor': '#evaluacion', **words('aula'), **ACCENT}, 'orn-ac-room')],
               cls='orn-sec orn-ac-sec orn-soft', boxed=True, css_id='aula')


def evaluacion(c):
    qs = []
    for q in c['evaluacion']:
        it = {'_id': eid(), 'type': q['type'], 'q': q['q'], 'scene': q['sc'] or '', 'why': q['w'] or '', 'hint': q['h'] or '', 'media_type': '', 'opts': q['o'] or ''}
        if q['tf']:
            it['tf'] = q['tf']
        qs.append(it)
    intro = ('Casos reales de la región y preguntas sobre lo que vio en las lecciones. Necesita un 70 % para recibir la insignia '
             f"«{c['insignia']}» y el certificado con código verificable. Puede repetirla las veces que quiera.")
    return con([w('wakoo-ac-evaluacion', {'title': 'Evaluación final', 'intro': intro, 'pass': {'unit': 'px', 'size': 70}, 'gate': 'yes', 'immersive': 'yes',
                                          'shuffle': 'yes', 'timer': 0, 'sound': '', 'cert_url': cert_link(), 'questions': qs, **words('evaluacion'), **ACCENT}, 'orn-ac-quiz')],
               cls='orn-sec orn-ac-sec', boxed=True, css_id='evaluacion')


def page_curso(c):
    sc = school(c)
    crumbs = B.section([iconlist([('Inicio', None, B.L('inicio')), ('Academia', None, B.L('academia')), (sc['name'], None, B.L('academia', 'cursos'))], 'orn-crumbs orn-crumbs--light', inline=True),
                        cabecera(c)], cls='orn-sec orn-ac-top', css_id='contenido')
    syl = B.section([w('wakoo-ac-temario', {**words('temario'), **ACCENT}, 'orn-ac-syl')], cls='orn-sec orn-sec--tight orn-ac-sec')
    otros = [o for o in CURSOS if o['escuela'] == c['escuela'] and o['clave'] != c['clave']]
    more = B.section([B.head('Siga aprendiendo', 'Otros cursos de la escuela'),
                      w('wakoo-ac-catalogo', {'filters': '', 'only_cat': sc['name'], 'limit': 3, 'exclude_self': 'yes', 'cols': '3', 'cols_tablet': '2', 'cols_mobile': '1', **words('catalogo'), **ACCENT}, 'orn-ac-cat')],
                     cls='orn-sec orn-soft') if otros else None
    note = B.section([B.callout('Antes de presentar un trámite', academia.AVISO, 'fas fa-balance-scale'),
                      btns([btn('Toda la academia', B.L('academia', 'cursos'), 'outline', icon='fas fa-th-large'), btn('Mi aprendizaje', B.L('mi-aprendizaje'), 'primary', icon='fas fa-user-graduate')])],
                     cls='orn-sec orn-sec--tight')
    return [x for x in [crumbs, ficha(c), syl, aula(c), evaluacion(c), more, note] if x]


HOW = [
    ('fas fa-book-open', 'Seis lecciones por curso', 'Textos claros con ejemplos de la región. Los vídeos se añadirán a cada lección cuando estén grabados.'),
    ('fas fa-tools', 'Una práctica en cada lección', 'Ejercicios para aplicar en su negocio o en su puesto de trabajo, y un espacio para sus notas.'),
    ('fas fa-tasks', 'Evaluación con casos', 'Situaciones reales: elegir, ordenar, emparejar y razonar. A pantalla completa y sin límite de tiempo.'),
    ('fas fa-certificate', 'Certificado verificable', 'Al aprobar recibe la insignia del curso y un certificado con un código que cualquier empleador puede comprobar.'),
]


def page_academia():
    schools = [B.reveal(iconbox(sc['icon'], sc['name'], sc['desc'], B.L('academia', 'cursos'), cls='orn-iconbox orn-school', position='top'), delay=i * 50) for i, sc in enumerate(C.SCHOOLS)]
    how = [B.reveal(iconbox(ic, t, d, cls='orn-iconbox orn-ac-how', position='top'), delay=i * 50) for i, (ic, t, d) in enumerate(HOW)]
    hours = sum(c['horas'] for c in CURSOS)
    return [
        B.pagehead('Academia Orinoco de Nuevos Negocios', 'Formación profesional para el empleo productivo y los nuevos negocios', C.ACADEMY_INTRO),
        B.section([B.head('Cómo se estudia', f'{len(CURSOS)} cursos, {hours} horas de formación, gratis y a su ritmo',
                          'Cada curso tiene ficha, temario, aula, guía en PDF para estudiar sin conexión, evaluación y certificado. Su progreso se guarda en su cuenta.'),
                   grid(how, 4, tablet=2, mobile=1, gap=18)], cls='orn-sec'),
        B.section([B.head('Cursos', 'Elija su curso', 'Busque por tema o filtre por escuela. Puede empezar sin cuenta; para guardar el progreso y recibir el certificado, inicie sesión.'),
                   w('wakoo-ac-catalogo', {'filters': 'yes', 'limit': 0, 'exclude_self': 'yes', 'cols': '3', 'cols_tablet': '2', 'cols_mobile': '1', **words('catalogo'), **ACCENT}, 'orn-ac-cat')],
                  cls='orn-sec orn-soft', css_id='cursos'),
        B.section([B.head('Escuelas', 'Cinco escuelas'), grid(schools, 5, tablet=3, mobile=1, gap=18)], cls='orn-sec'),
        B.section([grid([col([B.head('Líneas del programa', 'Programa Regional de Formación para el Empleo Productivo'),
                              *[iconbox('fas fa-check-circle', t, d, cls='orn-iconbox') for t, d in C.TRAINING_LINES]], 'orn-stack'),
                         col([B.head('Certificados verificables', 'Cada certificado tiene un código'),
                              p('Al aprobar la evaluación final, la academia emite un certificado con un código único. Cualquier empleador o contratista puede comprobarlo en línea.'),
                              btns([btn('Mi aprendizaje', B.L('mi-aprendizaje'), 'primary', icon='fas fa-user-graduate'), btn('Verificar un certificado', B.L('verificar'), 'outline')]),
                              p(academia.AVISO, 'orn-small')], 'orn-stack orn-panel')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec orn-soft'),
    ]


def page_aprendizaje():
    return B.apphead('mi-aprendizaje', 'fas fa-graduation-cap', 'Mi cuenta', 'Mi aprendizaje', 'Sus cursos, su progreso y sus certificados.', tabs=B.ACCOUNT, area='Mi cuenta') + [
        B.appbody([B.panel([w('wakoo-ac-progreso', {'cert_url': cert_link(), 'suggest': 3, **words('progreso'), **ACCENT}, 'orn-ac-dash')])])]


def page_verificar():
    return B.apphead('verificar', 'fas fa-certificate', 'Mi cuenta', 'Certificados de la Academia', 'Vea e imprima sus certificados, o escriba el código impreso en un certificado para comprobarlo.',
                     tabs=B.ACCOUNT, area='Mi cuenta') + [
        B.appbody([B.panel([w('wakoo-ac-certificado', {'org': 'ORINOCO BUSINESS & INVESTMENT', 'signer': 'Academia Orinoco de Nuevos Negocios',
                                                       'signer_role': 'Programa Regional de Formación para el Empleo Productivo',
                                                       'note': 'Certificado de un curso en línea de la Academia Orinoco. No es un título oficial.', 'demo': 'yes', **words('certificado'), **ACCENT}, 'orn-ac-cert')])])]


def pages():
    """Entradas para PAGES de build.py: (key, slug, title, builder, desc, parent)."""
    return [('curso-' + c['clave'], c['clave'], c['titulo'], (lambda c=c: page_curso(c)), c['lema'], 'academia') for c in CURSOS]


def media():
    return [(cover(c), 'Portada del curso ' + c['titulo']) for c in CURSOS]
