"""Paquete Wakoo del portal ORINOCO BUSINESS & INVESTMENT: wakoo-pack.json + images/ + fonts/ + styles/.

python3 build.py <carpeta_salida> [es,fr,en,zh-tw,it]

Todo se construye con widgets de Elementor y de Wakoo (sin widgets HTML). El español es la versión
maestra; francés, inglés, chino tradicional e italiano salen de traducciones.json (traducción de
trabajo, pendiente de revisión nativa) con los mismos ids de elemento, para que Wakoo → Idiomas
propague después los cambios del español. Los textos sin traducir se listan en faltan-traducciones.json.
"""
import itertools, json, os, re, sys
import el
from el import s, img, con, col, row, grid, section, w, h, p, eyebrow, btn, btns, image, icon, iconlist, iconbox, lnk, tpl, ul
import content as C

PACK = 'orinoco'
LN = 'es'



# Límites de referencia (no oficiales) para el zoom del globo y el mapa: ver docs/analisis-documental.md.
GEO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'limites-subregion.json'), encoding='utf-8'))
GEO_SOURCE = ('Límites de referencia, no oficiales: estado según Natural Earth (dominio público); municipios según C. E. Porto Tapiquén (2015) '
              'vía geoBoundaries (ODbL 1.0); río Orinoco según Natural Earth.')
GEO_LAYERS = {'limites-estado': ('Límite del estado (referencia)', '#E6C98C'), 'municipios-subregion': ('Municipios de la subregión (referencia)', '#C5A15B'),
              'rio-orinoco': ('Río Orinoco', '#2E86DE')}
MUN_FILL = {'José Gregorio Monagas': '#2E6FA8', 'Francisco de Miranda': '#3C8C79', 'Independencia': '#C5A15B'}


def sticky_header(node):
    """Cabecera flotante de Wakoo (Movimiento → Fijar al hacer scroll): se compacta al bajar y muestra el progreso de lectura."""
    node['settings'].update({'wakoo_sticky': 'yes', 'wakoo_sticky_pos': 'top', 'wakoo_sticky_offset': {'unit': 'px', 'size': 0},
                             'wakoo_sticky_z': 200, 'wakoo_sticky_fx': 'condense', 'wakoo_sticky_progress': 'yes', 'wakoo_sticky_progress_color': '#C5A15B'})
    node['settings']['_css_classes'] = (node['settings'].get('_css_classes', '') + ' orn-sticky').strip()
    return node


def zoom_geo():
    feats = [{'type': 'Feature', 'properties': {'role': 'outline', 'stroke': '#E6C98C'}, 'geometry': GEO['anzoategui']}]
    for n, c in MUN_FILL.items():
        feats.append({'type': 'Feature', 'properties': {'name': n, 'fill': c, 'stroke': '#FFFFFF', 'fit': True}, 'geometry': GEO[n]})
    feats.append({'type': 'Feature', 'properties': {'role': 'river', 'name': 'Río Orinoco'}, 'geometry': GEO['orinoco']})
    return json.dumps({'type': 'FeatureCollection', 'features': feats}, ensure_ascii=False, separators=(',', ':'))


def globe_zoom():
    return {'zoom': 'yes', 'zoom_geo': zoom_geo(), 'zoom_title': 'Subregión Orinoco · Sur de Anzoátegui', 'zoom_source': GEO_SOURCE,
            'zoom_scale': 2.8, 'zoom_hint': 'Pase el ratón o toque el globo para acercarse a la subregión'}


def L(key, anchor=''):
    """Link to another page of the pack."""
    return f'wakoo-pack://link/{LN}-{key}' + (('#' + anchor) if anchor else '')


def reveal(node, kind='fade-up', delay=0):
    node['settings']['wakoo_reveal'] = kind
    if delay:
        node['settings']['wakoo_reveal_delay'] = {'unit': 'px', 'size': round(delay / 1000, 2)}
    return node


def topo(node, color='#C5A15B', alpha=26, levels=12, grid_=True, speed=2):
    node['settings'].update({'wakoo_topo': 'yes', 'wakoo_topo_color': color, 'wakoo_topo_alpha': alpha, 'wakoo_topo_levels': levels,
                             'wakoo_topo_speed': speed, 'wakoo_topo_mouse': 'yes', 'wakoo_topo_grid': 'yes' if grid_ else ''})
    return node


def head(eb, title, lead=None, cls='', level=2):
    items = [eyebrow(eb)] if eb else []
    items.append(h(title, level))
    if lead:
        items.append(p(lead, 'orn-lead'))
    return col(items, ('orn-head ' + cls).strip())


def pagehead(eb, title, lead, crumbs=None, bg=None):
    items = []
    if crumbs:
        items.append(iconlist([(t, None, u) for t, u in crumbs], 'orn-crumbs', inline=True))
    items += [eyebrow(eb), h(title, 1), p(lead, 'orn-lead')]
    sec = section([col(items, 'orn-pagehead__inner')], cls='orn-pagehead orn-dark', css_id='contenido')
    if bg:
        sec['settings'].update({'background_background': 'classic', 'background_image': {'url': img(bg), 'id': '', 'alt': ''},
                                'background_position': 'center center', 'background_size': 'cover',
                                'background_overlay_background': 'gradient', 'background_overlay_color': 'rgba(10,36,64,0.97)',
                                'background_overlay_color_b': 'rgba(16,53,91,0.78)', 'background_overlay_gradient_angle': {'unit': 'deg', 'size': 100},
                                'background_overlay_opacity': {'unit': 'px', 'size': 1}})
    return topo(sec, alpha=20, levels=10)


def card(ic, title, text, url=None, cls='', delay=0):
    items = [icon(ic, 'orn-card__ico'), h(title, 3, url=url), p(text)]
    if url:
        items.append(btn('Ver más', url, 'text', icon='fas fa-arrow-right'))
    return reveal(col(items, ('orn-card ' + cls).strip()), delay=delay)


def bullets(items, ic='fas fa-check', cls=''):
    return iconlist([(t, ic, None) for t in items], ('orn-bullets ' + cls).strip())


def steps(items, cls=''):
    """Numbered steps as headings + text (each one editable)."""
    out = []
    for i, it in enumerate(items):
        t, d = (it if isinstance(it, tuple) else (it, ''))
        kids = [h(f'{i + 1:02d}', 'div', 'orn-step__n'), h(t, 3, 'orn-step__t')]
        if d:
            kids.append(p(d))
        out.append(reveal(col(kids, 'orn-step'), delay=i * 50))
    return grid(out, 3 if len(items) > 4 else len(items), tablet=2, mobile=1, gap=18, cls=('orn-steps ' + cls).strip())


def callout(title, text, ic='fas fa-info-circle'):
    return col([iconlist([(title, ic, None)], 'orn-callout__t'), p(text)], 'orn-callout')


def tw(name, settings=None, cls=''):
    """Territorio / Wakoo widget with its default (editable) texts."""
    return w(name, settings or {}, ('orn-tw ' + cls).strip())


def cta_band(title, text, buttons):
    return topo(section([col([h(title, 2), p(text, 'orn-lead'), btns(buttons)], 'orn-cta__inner')], cls='orn-sec orn-cta orn-dark'), alpha=30)


# ------------------------------------------------------------------ cabecera y pie

MENU = [
    ('Institución', 'institucion', [('Presentación y visión', 'institucion'), ('Territorio y municipios', 'territorio'), ('Gobernanza e inversión', 'gobernanza'),
                                    ('Desarrollo sostenible', 'sostenibilidad'), ('Documentos', 'documentos')]),
    ('Sectores', 'sectores', [(sc['name'], 'sector-' + sc['slug']) for sc in C.SECTORS]),
    ('Proyectos', 'proyectos', []),
    ('Directorio', 'directorio', []),
    ('Herramientas', 'ventanilla', [('Ventanilla única del inversionista', 'ventanilla'), ('Mapa del territorio', 'mapa'), ('Directorio empresarial B2B', 'directorio'),
                                    ('Proveedores y necesidades de compra', 'proveedores'), ('Observatorio', 'observatorio')]),
    ('Academia', 'academia', []),
    ('Noticias', 'noticias', []),
    ('Contacto', 'contacto', []),
]


def menu_tree():
    return [{'title': t, 'link': f'{LN}-{k}', 'children': [{'title': ct, 'link': f'{LN}-{ck}'} for ct, ck in kids]} for t, k, kids in MENU]


def wordmark(cls='orn-wordmark'):
    return w('heading', {'title': 'ORINOCO <span>BUSINESS &amp; INVESTMENT</span>', 'header_size': 'div', 'link': lnk(L('inicio'))}, cls)


def header():
    return [
        con([
            iconlist([('Subregión Orinoco · Sur de Anzoátegui · Venezuela', 'fas fa-map-pin', None)], 'orn-topbar__info', inline=True),
            con([
                iconlist([('Directorio de empresas', 'fas fa-building', L('directorio')), ('Mi cuenta', 'fas fa-user-circle', L('acceso')), ('Verificar certificado', 'fas fa-certificate', L('verificar'))], 'orn-topbar__links', inline=True),
                w('wakoo-idiomas', {'style': 'codes', 'label': 'Idioma', 'color': '#E6C98C'}, 'orn-langs'),
            ], cls='orn-topbar__right wk-keep-row', direction='row', inner=True),
        ], cls='orn-topbar wk-keep-row', boxed=True, direction='row'),
        con([
            btn('Saltar al contenido', '#contenido', 'primary', 'orn-skip'),
            wordmark(),
            w('wakoo-menu', {'menu': f'wakoo-pack://menu/main-{LN}', 'mode': 'horizontal', 'mega': '', 'breakpoint': 1180,
                             'toggle_label': 'Menú', 'accent': '#C5A15B', 'txt': '#FFFFFF'}, 'orn-nav'),
            btn('Presentar un proyecto', L('ventanilla'), 'gold', 'orn-btn--sm orn-header__cta'),
        ], cls='orn-header wk-keep-row', boxed=True, direction='row'),
    ]


def footer():
    inst = [(t, None, L(k)) for t, k in (('Presentación y visión', 'institucion'), ('Territorio y municipios', 'territorio'), ('Gobernanza e inversión', 'gobernanza'),
                                          ('Desarrollo sostenible', 'sostenibilidad'), ('Documentos', 'documentos'), ('Noticias', 'noticias'))]
    tools = [(t, None, L(k)) for t, k in (('Cartera de proyectos', 'proyectos'), ('Ventanilla única', 'ventanilla'), ('Mapa del territorio', 'mapa'),
                                           ('Directorio B2B', 'directorio'), ('Observatorio', 'observatorio'), ('Academia Orinoco', 'academia'))]
    legal = [(t, None, L(k)) for t, k in (('Privacidad y datos personales', 'privacidad'), ('Términos de uso', 'terminos'), ('Accesibilidad', 'accesibilidad'), ('Contacto', 'contacto'))]
    return [topo(con([
        grid([
            col([wordmark('orn-wordmark orn-wordmark--footer'), p(C.MOTTO + '.', 'orn-footer__motto'),
                 p('Municipios Independencia, José Gregorio Monagas y Francisco de Miranda · Estado Anzoátegui · República Bolivariana de Venezuela.', 'orn-small')], 'orn-stack'),
            col([h('Institución', 3), iconlist(inst, 'orn-footer__links')], 'orn-stack'),
            col([h('Herramientas', 3), iconlist(tools, 'orn-footer__links')], 'orn-stack'),
            col([h('Información legal', 3), iconlist(legal, 'orn-footer__links')], 'orn-stack'),
        ], 4, tablet=2, mobile=1, gap=36, cls='orn-footer__grid'),
        con([p('© 2026 ORINOCO BUSINESS &amp; INVESTMENT · Portal institucional en construcción: los datos de contacto, la información territorial y los indicadores están pendientes de validación oficial. '
               'La ventanilla orienta y hace seguimiento; no concede permisos ni aprueba proyectos.', 'orn-footer__legal')], cls='orn-footer__bottom', inner=True),
    ], cls='orn-footer orn-dark', boxed=True, tag='footer'), alpha=16, levels=9, grid_=False, speed=1)]


# ------------------------------------------------------------------ inicio

QUICK = [
    ('fas fa-briefcase', 'Cartera de proyectos', 'Fichas con estado de preparación y condiciones previas.', 'proyectos'),
    ('fas fa-concierge-bell', 'Ventanilla única', 'Registre su iniciativa y siga su expediente.', 'ventanilla'),
    ('fas fa-map-marked-alt', 'Mapa del territorio', 'Capas verificadas, corredores y proyectos.', 'mapa'),
    ('fas fa-building', 'Directorio B2B', 'Empresas, proveedores y necesidades de compra.', 'directorio'),
    ('fas fa-chart-area', 'Observatorio', 'Indicadores con fuente, fecha y metodología.', 'observatorio'),
    ('fas fa-graduation-cap', 'Academia Orinoco', 'Cinco escuelas para nuevos negocios.', 'academia'),
]

FIGURES = [
    ('', 3, '', 'municipios en el ámbito de planificación'),
    ('≈ ', 8000, ' km²', 'territorio de referencia'),
    ('', 631, ' km²', 'potencialmente aprovechables para la agricultura'),
    ('', 10, '', 'sectores de oportunidad'),
    ('', 8, '', 'proyectos en la cartera inicial'),
    ('', 2, '', 'puentes sobre el Orinoco: Angostura y Orinoquia'),
]


def counter(prefix, n, suffix, title, delay=0):
    return reveal(col([w('counter', {'starting_number': 0, 'ending_number': n, 'prefix': prefix, 'suffix': suffix, 'duration': 1800,
                                     'thousand_separator': 'yes', 'thousand_separator_char': '.', 'title': title}, 'orn-counter')], 'orn-figure'), delay=delay)


def page_inicio():
    hero = section([
        grid([
            col([
                eyebrow('Subregión Orinoco · Sur de Anzoátegui'),
                h('ORINOCO <span>BUSINESS &amp; INVESTMENT</span>', 1, 'orn-hero__title'),
                h(C.SUB, 2, 'orn-hero__sub'),
                p(C.INTRO, 'orn-lead'),
                btns([btn('Explorar oportunidades', L('sectores'), 'gold', icon='fas fa-arrow-right'),
                      btn('Presentar un proyecto', L('ventanilla'), 'light'),
                      btn('Directorio de empresas', L('directorio'), 'ghost', icon='fas fa-building')]),
                p(C.MOTTO + '.', 'orn-hero__motto'),
            ], 'orn-hero__text'),
            col([w('wakoo-globe', {'focus_lat': 8.4, 'focus_lng': -64.3, 'spin': 1.5, 'swing': 40, 'size': 560,
                                   'label': 'Globo terráqueo que señala la Subregión Orinoco, en el sur del estado Anzoátegui, Venezuela',
                                   'markers': [{'_id': el.eid(), 'title': 'Subregión Orinoco (referencia aproximada)', 'lat': 8.4, 'lng': -64.3, 'size': 0.09, 'main': 'yes'}],
                                   'legend': 'yes', 'dark': 'yes', 'base': '#4A7FB5', 'mark': '#FFFFFF', 'accent': '#C5A15B', 'glow': '#2A6DB0', 'legend_color': '#C9D6E5', **globe_zoom()}, 'orn-globe')],
                'orn-hero__globe'),
        ], 2, tablet=1, mobile=1, gap=24, cls='orn-hero__grid'),
    ], cls='orn-hero orn-dark', css_id='contenido')
    topo(hero, alpha=30, levels=14)

    quick = section([grid([reveal(col([icon(ic, 'orn-quick__ico'), h(t, 3, url=L(k)), p(d)], 'orn-quick'), delay=i * 60)
                           for i, (ic, t, d, k) in enumerate(QUICK)], 6, tablet=3, mobile=2, gap=14, cls='orn-quick__grid')], cls='orn-quickbar')

    figures = section([
        head('Datos de referencia', 'El territorio en cifras', 'Cifras tomadas de la ponencia y de la caracterización económica. Se publican como referencia y están pendientes de validación oficial.'),
        grid([counter(a, n, b, t, i * 60) for i, (a, n, b, t) in enumerate(FIGURES)], 6, tablet=3, mobile=2, gap=16, cls='orn-figures'),
        p(C.SOURCE + ' ' + C.PENDING + '.', 'orn-source'),
    ], cls='orn-sec')

    vision = section([col([eyebrow('Visión estratégica'), h(C.VISION, 2, 'orn-quote'), btns([btn('Conocer la institución', L('institucion'), 'light', icon='fas fa-arrow-right')])], 'orn-vision__inner')],
                     cls='orn-sec orn-vision orn-dark', bg='franja-territorio.webp', overlay=('rgba(10,36,64,0.96)', 'rgba(16,53,91,0.80)', 100))

    sectors = section([
        row([head('Portafolio estratégico', 'Diez sectores de oportunidad', 'Cada sector reúne su relevancia, las oportunidades identificadas, la infraestructura que requiere y las condiciones previas.'),
             btn('Ver todos los sectores', L('sectores'), 'outline', icon='fas fa-arrow-right')], cls='orn-row-between'),
        grid([card(sc['icon'], sc['name'], sc['lead'], L('sector-' + sc['slug']), 'orn-card--sector', i * 40) for i, sc in enumerate(C.SECTORS)], 5, tablet=2, mobile=2, gap=12, cls='orn-sectors-grid'),
    ], cls='orn-sec orn-soft')

    projects = section([
        grid([
            col([head('Cartera de proyectos', 'Proyectos estructurados, con su grado real de preparación',
                      'Cada ficha distingue un proyecto conceptual de uno con terrenos, permisos, estudios y acuerdos. Las cifras se publican como estimación o como dato verificado, nunca al revés.'),
                 btns([btn('Ver la cartera completa', L('proyectos'), 'primary', icon='fas fa-arrow-right'), btn('Presentar un proyecto', L('ventanilla'), 'outline')])], 'orn-stack'),
            col([tw('wakoo-t-stages', {'link': lnk(L('proyectos'))})], 'orn-stack'),
        ], 2, tablet=1, mobile=1, gap=48, cls='orn-split'),
        tw('wakoo-t-projects', {'filters': '', 'per': 4, 'cols': '4', 'paging': ''}),
    ], cls='orn-sec orn-home-projects')

    territory = section([
        head('Conectividad', 'Un territorio entre corredores terrestres y el río Orinoco', C.TERRITORY),
        grid([reveal(col([image(im, alt, cls='orn-photo'), col([icon(ic, 'orn-card__ico'), h(t, 3), p(d)], 'orn-card__body')], 'orn-card orn-card--photo'), delay=i * 80)
              for i, (ic, t, d, im, alt) in enumerate(C.CORRIDORS)], 3, tablet=1, mobile=1, gap=20),
        btns([btn('Consultar el mapa', L('mapa'), 'primary', icon='fas fa-map'), btn('Territorio y municipios', L('territorio'), 'outline')]),
    ], cls='orn-sec orn-soft')

    tools = topo(section([
        head('Herramientas', 'Del interés a la inversión, con seguimiento', 'Cuatro herramientas conectadas que ordenan la información y acompañan cada iniciativa.', 'orn-head--light'),
        grid([card('fas fa-concierge-bell', 'Ventanilla única', 'Registro de la iniciativa, clasificación, organismos competentes, hoja de ruta y seguimiento. Orienta: no concede permisos.', L('ventanilla'), 'orn-card--glass', 0),
              card('fas fa-map-marked-alt', 'Mapa del territorio', 'Google Maps con capas públicas verificadas y proyectos con ubicación confirmada.', L('mapa'), 'orn-card--glass', 60),
              card('fas fa-network-wired', 'Proveedores', 'Directorio B2B, niveles de verificación, consultas y necesidades de compra.', L('proveedores'), 'orn-card--glass', 120),
              card('fas fa-chart-area', 'Observatorio', 'Indicadores con ficha técnica: fuente, fecha, periodicidad, responsable y verificación.', L('observatorio'), 'orn-card--glass', 180)],
             4, tablet=2, mobile=1, gap=18),
    ], cls='orn-sec orn-dark'), alpha=22)

    academy = section([
        grid([
            col([head('Academia Orinoco de Nuevos Negocios', 'Talento local para las nuevas inversiones', C.ACADEMY_INTRO),
                 btns([btn('Acceder a la academia', L('academia'), 'primary', icon='fas fa-graduation-cap'), btn('Verificar un certificado', L('verificar'), 'outline')])], 'orn-stack'),
            col([iconlist([(sc['name'], sc['icon'], L('academia')) for sc in C.SCHOOLS], 'orn-schools')], 'orn-stack'),
        ], 2, tablet=1, mobile=1, gap=48, cls='orn-split'),
    ], cls='orn-sec')

    directory = section([
        grid([
            col([image('taller-metalmecanico.webp', 'Soldador trabajando en una estructura metálica dentro de un taller industrial', cls='orn-photo orn-photo--tall')], 'orn-media'),
            col([head('Directorio empresarial B2B', 'Proveedores locales preparados para competir',
                      'Registre su empresa, cargue su documentación en un expediente privado y reciba consultas de compradores. Tres niveles de verificación muestran qué revisó el equipo.'),
                 grid([col([icon(ic, 'orn-card__ico'), h(t, 3), p(d)], 'orn-level') for ic, t, d in C.LEVELS], 3, tablet=1, mobile=1, gap=12),
                 btns([btn('Registrar una empresa', L('mi-empresa'), 'primary', icon='fas fa-arrow-right'), btn('Consultar el directorio', L('directorio'), 'outline')])], 'orn-stack'),
        ], 2, tablet=1, mobile=1, gap=48, cls='orn-split'),
    ], cls='orn-sec orn-soft')

    news = section([
        grid([
            col([head('Noticias y agenda', 'Rondas de negocios y novedades', 'Las rondas de negocios, presentaciones sectoriales y novedades se publicarán aquí.'),
                 tw('wakoo-events-list', {'count': 3, 'empty': 'Pronto anunciaremos las próximas rondas de negocios y presentaciones sectoriales.', 'accent': '#174A7E'}),
                 btns([btn('Ver noticias', L('noticias'), 'outline', icon='fas fa-arrow-right')])], 'orn-stack'),
            col([head('Documentos', 'Ponencia de referencia', 'Propuesta para la articulación estratégica entre el sector público, el sector privado, los inversionistas, las empresas operadoras, las contratistas, las universidades y las organizaciones socioproductivas.'),
                 iconlist([('Ponencia ORINOCO BUSINESS & INVESTMENT FORUM (PDF, 21/10/2026)', 'fas fa-file-pdf', img(C.PDF))], 'orn-docs'),
                 btns([btn('Todos los documentos', L('documentos'), 'outline', icon='fas fa-arrow-right')])], 'orn-stack orn-panel'),
        ], 2, tablet=1, mobile=1, gap=40, cls='orn-split'),
    ], cls='orn-sec')

    validate = section([
        head('Transparencia', 'Lo que falta validar antes de presentarse a inversionistas', 'La ponencia recomienda completar cuatro validaciones. El portal las muestra para que nadie confunda una oportunidad con un compromiso.'),
        grid([reveal(col([icon(ic, 'orn-card__ico'), h(t, 3), p(d)], 'orn-card'), delay=i * 60) for i, (ic, t, d) in enumerate(C.VALIDATIONS)], 4, tablet=2, mobile=1, gap=16),
    ], cls='orn-sec orn-soft')

    return [hero, quick, figures, vision, sectors, projects, territory, tools, academy, directory, news, validate,
            cta_band('Invertir para producir, producir para transformar', C.CLOSING, [btn('Presentar un proyecto', L('ventanilla'), 'gold', icon='fas fa-arrow-right'), btn('Contacto', L('contacto'), 'light')])]


# ------------------------------------------------------------------ institución

def page_institucion():
    return [
        pagehead('Institución', 'Presentación, visión y principios', 'Una propuesta para articular al sector público, el sector privado, los inversionistas, las empresas operadoras, las contratistas, las universidades y las organizaciones socioproductivas del territorio.', bg='franja-territorio.webp'),
        section([grid([col([head('Presentación', 'Propósito de la iniciativa'), *[p(x) for x in C.PURPOSE], callout('Propuestas, no beneficios vigentes', C.NOT_IN_FORCE)], 'orn-stack'),
                       col([image('puente-orinoquia.webp', 'Vista aérea del Puente Orinoquia sobre el río Orinoco', 'Puente Orinoquia. Foto: @miguelsayeghd, publicada en la ponencia.', cls='orn-photo'),
                            col([eyebrow('Posicionamiento'), h(C.POSITIONING, 3, 'orn-quote orn-quote--sm')], 'orn-panel')], 'orn-stack')], 2, tablet=1, mobile=1, gap=48, cls='orn-split')], cls='orn-sec'),
        topo(section([col([eyebrow('Visión'), h(C.VISION, 2, 'orn-quote')], 'orn-vision__inner')], cls='orn-sec orn-vision orn-dark'), alpha=24),
        section([head('Objetivos', 'Qué busca el portal'), grid([card(ic, t, d, delay=i * 50) for i, (ic, t, d) in enumerate(C.OBJECTIVES)], 3, tablet=2, mobile=1, gap=18)], cls='orn-sec'),
        section([head('Principios rectores', 'Siete principios para invertir con desarrollo territorial'),
                 grid([card(ic, t, d, delay=i * 40) for i, (ic, t, d) in enumerate(C.PRINCIPLES)], 4, tablet=2, mobile=1, gap=16)], cls='orn-sec orn-soft'),
        section([head('Escalas de inversión', 'Una política de inversión basada en cadenas de valor', 'Los recursos naturales generan oportunidades, pero es la organización de las cadenas productivas la que permite convertirlas en riqueza, empleo y competitividad.'),
                 grid([card(ic, t, d, delay=i * 60) for i, (ic, t, d) in enumerate(C.SCALES)], 3, tablet=1, mobile=1, gap=18)], cls='orn-sec'),
        cta_band('¿Tiene una iniciativa para la Subregión Orinoco?', 'Regístrela en la ventanilla: le asignamos un código, la clasificamos y le indicamos los organismos competentes.',
                 [btn('Presentar un proyecto', L('ventanilla'), 'gold', icon='fas fa-arrow-right')]),
    ]


def page_territorio():
    muns = [reveal(col([icon('fas fa-map-marker-alt', 'orn-card__ico'), h(m['name'], 3), p(m['focus'], 'orn-strong'), bullets(m['invest'], 'fas fa-angle-right')], 'orn-card'), delay=i * 60)
            for i, m in enumerate(C.MUNICIPIOS)]
    return [
        pagehead('Territorio', 'Territorio y municipios', C.TERRITORY, bg='puente-orinoquia.webp'),
        section([grid([col([head('Ubicación estratégica', 'Tres razones de una posición geoeconómica'), *[iconbox(ic, t, d, cls='orn-iconbox') for ic, t, d in C.WHY], callout('Superficie de referencia', C.AREA_NOTE, 'fas fa-ruler-combined')], 'orn-stack'),
                       col([w('wakoo-globe', {'focus_lat': 8.4, 'focus_lng': -64.3, 'spin': 1, 'swing': 30, 'size': 460, 'label': 'Globo que señala la Subregión Orinoco',
                                              'markers': [{'_id': el.eid(), 'title': 'Subregión Orinoco (referencia aproximada)', 'lat': 8.4, 'lng': -64.3, 'size': 0.09, 'main': 'yes'}],
                                              'legend': 'yes', 'dark': 'yes', 'base': '#4A7FB5', 'accent': '#C5A15B', 'glow': '#2A6DB0', **globe_zoom()}, 'orn-globe orn-globe--panel')], 'orn-globe-panel')],
                      2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
        section([head('Municipios', 'Desarrollo diferenciado por municipio', 'Los tres municipios comparten un marco geográfico, pero no necesariamente las mismas ventajas, infraestructuras ni condiciones de inversión.'),
                 grid(muns, 3, tablet=1, mobile=1, gap=18), callout('Propuesta inicial de especialización', C.MUN_NOTE)], cls='orn-sec orn-soft'),
        section([head('Conectividad terrestre y fluvial', 'Corredores y accesos'),
                 grid([reveal(col([image(im, alt, cls='orn-photo'), col([icon(ic, 'orn-card__ico'), h(t, 3), p(d)], 'orn-card__body')], 'orn-card orn-card--photo'), delay=i * 80)
                       for i, (ic, t, d, im, alt) in enumerate(C.CORRIDORS)], 3, tablet=1, mobile=1, gap=20),
                 grid([col([h('Rutas agrícolas y ganaderas', 3), bullets(C.RUTAS, 'fas fa-route')], 'orn-panel'),
                       col([h('Déficit vial interno', 3), p(C.ROAD_WARNING)], 'orn-panel orn-panel--warn')], 2, tablet=1, mobile=1, gap=20)], cls='orn-sec'),
        topo(section([grid([col([eyebrow('El Orinoco'), h('Un activo logístico y comercial por construir', 2), p(C.RIVER)], 'orn-stack'),
                            col([eyebrow('Caribe y Sur Global'), h('Diversificación comercial, no una ruta garantizada', 2), p(C.CARIBE)], 'orn-stack')], 2, tablet=1, mobile=1, gap=48)],
                     cls='orn-sec orn-dark'), alpha=24),
        section([grid([col([head('Caracterización económica', 'Macapaima: plataforma industrial de referencia', C.MACAPAIMA)], 'orn-stack'),
                       col([image('plantacion-forestal-uverito.webp', 'Vista aérea de una plantación forestal atravesada por un camino', cls='orn-photo')], 'orn-media')], 2, tablet=1, mobile=1, gap=48, cls='orn-split')], cls='orn-sec'),
        cta_band('Explore el territorio en el mapa', 'Capas públicas con fuente y fecha, y proyectos cuya ubicación ya fue verificada.', [btn('Consultar el mapa', L('mapa'), 'gold', icon='fas fa-map')]),
    ]


def page_sostenibilidad():
    return [
        pagehead('Desarrollo sostenible', 'Inversión responsable con el río, los suelos y los bosques', 'La sostenibilidad ambiental es un principio rector: cada oportunidad se evalúa con sus condiciones técnicas, sanitarias y ambientales.', bg='rio-curiaras.webp'),
        section([head('Compromisos', 'Cómo se aplica en cada sector'), grid([card(ic, t, d, delay=i * 50) for i, (ic, t, d) in enumerate(C.SUSTAIN)], 3, tablet=2, mobile=1, gap=18)], cls='orn-sec'),
        section([grid([col([head('Formación y empleo local', 'Desarrollo con la gente del territorio', 'La propuesta sustituye la visión del empleo local como un compromiso accesorio por una política de formación, certificación y empleabilidad vinculada a la demanda efectiva de las empresas.'),
                            bullets(['Porcentaje de vacantes cubiertas con trabajadores de la subregión cuando existan perfiles idóneos', 'Personas capacitadas y certificadas', 'Tasa de inserción laboral de los egresados',
                                     'Empresas locales incorporadas a las cadenas de suministro', 'Horas de formación técnica financiadas por los proyectos', 'Participación de jóvenes y mujeres en la capacitación'])], 'orn-stack'),
                       col([head('Seguridad', 'Seguridad como factor de confianza', C.SECURITY)], 'orn-stack orn-panel')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec orn-soft'),
        section([head('Servicios públicos', 'Matriz de garantía de servicios para proyectos de inversión', 'Compromisos propuestos que solo se acuerdan cuando existe viabilidad técnica, jurídica y presupuestaria.'),
                 grid([reveal(col([icon(ic, 'orn-card__ico'), h(t, 3), p(f'<strong>Compromiso propuesto:</strong> {a}'), p(f'<strong>Indicador verificable:</strong> {b}', 'orn-small')], 'orn-card'), delay=i * 40)
                       for i, (ic, t, a, b) in enumerate(C.SERVICES_MATRIX)], 4, tablet=2, mobile=1, gap=16)], cls='orn-sec'),
    ]


def page_gobernanza():
    return [
        pagehead('Gobernanza e inversión', 'Gobernanza económica permanente', 'Un mecanismo de coordinación capaz de ordenar proyectos, identificar obstáculos, priorizar inversiones y dar seguimiento a los compromisos institucionales.', bg='franja-territorio.webp'),
        section([grid([col([head('Mesa de Gobernanza Económica (propuesta)', 'Quién podría integrarla', 'Carácter de coordinación y concertación, sin desplazar las competencias de los organismos reguladores, las autoridades municipales ni las decisiones comerciales de las empresas.'),
                            bullets(C.MESA_MEMBERS, 'fas fa-user-tie')], 'orn-stack'),
                       col([h('Siete funciones', 3), steps(C.MESA_FUNCTIONS[:], 'orn-steps--compact')], 'orn-stack')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
        section([head('Hoja de ruta', 'De la ponencia a los resultados', C.PHASES_NOTE),
                 grid([reveal(col([h(f, 'div', 'orn-phase__f'), h(t, 'div', 'orn-phase__t'), h(n, 3), bullets(items, 'fas fa-angle-right')], 'orn-phase'), delay=i * 80) for i, (f, t, n, items) in enumerate(C.PHASES)],
                      4, tablet=2, mobile=1, gap=16, cls='orn-phases')], cls='orn-sec orn-soft'),
        section([grid([col([head('Gobernanza contractual', 'Reglas claras para la confianza empresarial'), bullets(C.CONTRACT, 'fas fa-file-contract')], 'orn-stack'),
                       col([head('Indicadores de desempeño institucional', 'La gobernanza se mide por resultados', 'Cada indicador tendrá línea base, fuente verificable y periodicidad. Se publicarán en el observatorio.'),
                            iconlist([(f'{a} — {b}', 'fas fa-chart-bar', None) for a, b in C.INST_INDICATORS], 'orn-bullets'),
                            btns([btn('Ir al observatorio', L('observatorio'), 'outline', icon='fas fa-arrow-right')])], 'orn-stack')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
        section([head('Incentivos tributarios', 'Instrumentos que se propone evaluar', 'Mejor trato fiscal con incentivos selectivos, temporales, transparentes y vinculados a resultados verificables.'),
                 grid([col([h(a, 3), p(f'<strong>Aplicación potencial:</strong> {b}'), p(f'<strong>Condición:</strong> {c}', 'orn-small')], 'orn-card orn-card--flat') for a, b, c in C.INCENTIVES], 4, tablet=2, mobile=1, gap=14),
                 callout('Ningún incentivo está vigente', C.INCENTIVES_NOTE, 'fas fa-exclamation-triangle')], cls='orn-sec orn-soft'),
    ]


def page_documentos():
    docs = [('Ponencia ORINOCO BUSINESS & INVESTMENT FORUM — Subregión Orinoco (PDF, 21/10/2026)', 'fas fa-file-pdf', img(C.PDF))]
    pending = ['Caracterización económica de la Subregión Orinoco (20/10/2026)', 'Portafolio «Venezuela Oil & Gas Opportunities»', 'Cartografía georreferenciada y fichas de terrenos',
               'Fichas de inversión de la cartera inicial', 'Estudios de servicios públicos por zona de inversión']
    return [
        pagehead('Documentos', 'Sala de documentos', 'Documentación técnica verificable para inversionistas, instituciones y comunidades.'),
        section([grid([col([head('Disponibles', 'Descargar'), iconlist(docs, 'orn-docs'), p('La ponencia es una propuesta para evaluación y concertación. Sus cifras provienen de la caracterización económica y deben validarse antes de usarse en decisiones de inversión.', 'orn-small')], 'orn-stack orn-panel'),
                       col([head('Pendientes de publicación', 'Se publicarán cuando estén validados'), bullets(pending, 'far fa-clock')], 'orn-stack')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
        section([head('Validaciones', 'Antes de la versión institucional definitiva'), grid([card(ic, t, d, delay=i * 60) for i, (ic, t, d) in enumerate(C.VALIDATIONS)], 4, tablet=2, mobile=1, gap=16)], cls='orn-sec orn-soft'),
    ]


# ------------------------------------------------------------------ sectores

def page_sectores():
    return [
        pagehead('Portafolio estratégico', 'Sectores de oportunidad', 'Diez sectores con sus oportunidades, la infraestructura que requieren y las condiciones previas que deben cumplirse.', bg='franja-territorio.webp'),
        section([grid([card(sc['icon'], sc['name'], sc['lead'], L('sector-' + sc['slug']), 'orn-card--sector', i * 40) for i, sc in enumerate(C.SECTORS)], 3, tablet=2, mobile=1, gap=18)], cls='orn-sec'),
        section([head('Escalas', 'Tres escalas de inversión'), grid([card(ic, t, d) for ic, t, d in C.SCALES], 3, tablet=1, mobile=1, gap=18)], cls='orn-sec orn-soft'),
    ]


def page_sector(sc):
    media = image(sc['img'] + '.webp', sc['alt'], cls='orn-photo') if sc['img'] else col([icon(sc['icon'], 'orn-bigico')], 'orn-iconpanel')
    blocks = [('Oportunidades identificadas', sc['opps'], 'fas fa-lightbulb'), ('Tipos de inversión', sc['types'], 'fas fa-layer-group'),
              ('Infraestructura requerida', sc['infra'], 'fas fa-tools'), ('Condiciones previas y riesgos', sc['risks'], 'fas fa-exclamation-circle')]
    return [
        pagehead('Sector', sc['name'], sc['lead'], crumbs=[('Inicio', L('inicio')), ('Sectores', L('sectores'))]),
        section([grid([col([head('Relevancia', 'Por qué este sector', sc['relevance']), p(C.SOURCE, 'orn-source')], 'orn-stack'), col([media], 'orn-media')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
        section([grid([reveal(col([iconlist([(t, ic, None)], 'orn-block__t'), bullets(items, 'fas fa-angle-right')], 'orn-card'), delay=i * 60) for i, (t, items, ic) in enumerate(blocks)],
                      4, tablet=2, mobile=1, gap=16)], cls='orn-sec orn-soft'),
        section([head('Proyectos relacionados', 'Proyectos de la cartera en este sector'), tw('wakoo-t-projects', {'sector': sc['slug'], 'filters': '', 'per': 6, 'cols': '3'})], cls='orn-sec'),
        section([head('Empresas vinculadas', 'Empresas y proveedores del sector'), tw('wakoo-t-companies', {'sector': sc['slug'], 'filters': '', 'per': 6, 'register': lnk(L('mi-empresa'))})], cls='orn-sec orn-soft'),
        cta_band('¿Tiene una iniciativa en este sector?', 'Preséntela en la ventanilla: el formulario llega con el sector ya elegido.',
                 [btn('Presentar una iniciativa', L('ventanilla') + '?sector=' + sc['slug'], 'gold', icon='fas fa-arrow-right'), btn('Registrar una empresa', L('mi-empresa'), 'light')]),
    ]


# ------------------------------------------------------------------ proyectos y ventanilla

# ------------------------------------------------------------------ herramientas (vista de aplicación)

TOOLS = [('proyectos', 'Proyectos', 'fas fa-briefcase'), ('ventanilla', 'Ventanilla', 'fas fa-concierge-bell'), ('mapa', 'Mapa', 'fas fa-map-marked-alt'),
         ('directorio', 'Directorio', 'fas fa-building'), ('proveedores', 'Proveedores', 'fas fa-truck-loading'), ('observatorio', 'Observatorio', 'fas fa-chart-line')]
ACCOUNT = [('mis-solicitudes', 'Mis solicitudes', 'fas fa-folder-open'), ('mi-empresa', 'Mi empresa', 'fas fa-building'),
           ('mi-aprendizaje', 'Mi aprendizaje', 'fas fa-graduation-cap'), ('acceso', 'Mi cuenta', 'fas fa-user-circle')]


def apptabs(tabs, current, label):
    """Barra de pestañas de la aplicación: un botón por herramienta, la actual resaltada."""
    return section([row([btn(t, L(k), 'tab', 'orn-apptab' + (' is-on' if k == current else ''), icon=ic) for k, t, ic in tabs], 'orn-apptabs__row wk-keep-row', gap=4)],
                   cls='orn-apptabs', label=label)


def apphead(key, ic, eb, title, lead, actions=(), tabs=TOOLS, area='Herramientas'):
    """Cabecera compacta de herramienta (en vez del gran encabezado de página) + pestañas."""
    left = col([iconlist([('Inicio', None, L('inicio')), (area, None, L(tabs[0][0]))], 'orn-crumbs', inline=True),
                row([icon(ic, 'orn-appicon'), col([eyebrow(eb), h(title, 1, 'orn-apphead__t'), p(lead, 'orn-apphead__lead')], 'orn-apphead__txt', gap=6)], 'orn-apphead__id wk-keep-row', gap=18)],
               'orn-apphead__main', gap=14)
    kids = [left] + ([btns(list(actions), 'orn-apphead__actions')] if actions else [])
    head_ = topo(section([row(kids, 'orn-apphead__row', gap=24)], cls='orn-apphead orn-dark', css_id='contenido'), alpha=14, levels=8)
    return [head_, apptabs(tabs, key, area)]


def panel(children, title=None, ic=None, cls=''):
    items = ([iconlist([(title, ic, None)], 'orn-apppanel__t')] if title else []) + children
    return col(items, ('orn-apppanel ' + cls).strip(), gap=14)


def appbody(main, side=None, cls=''):
    body = grid([col(main, 'orn-appmain', gap=20), col(side, 'orn-appside', gap=20)], 1, tablet=1, mobile=1, gap=24, cls='orn-appgrid') if side else col(main, 'orn-appmain', gap=20)
    return section([body], cls=('orn-app ' + cls).strip())


def defs(items, cls=''):
    """Lista compacta título + texto (glosarios, niveles, pasos) para las columnas laterales."""
    items = [it if isinstance(it, tuple) else (it, '') for it in items]
    return col([col([h(t, 4, 'orn-def__t')] + ([p(d, 'orn-def__d')] if d else []), 'orn-def') for t, d in items], ('orn-defs ' + cls).strip(), gap=0)


def page_proyectos():
    return apphead('proyectos', 'fas fa-briefcase', 'Cartera de proyectos', 'Proyectos de inversión de la Subregión Orinoco', 'Fichas estandarizadas con estado de preparación, objetivo económico y condición previa. ' + C.PROJECT_NOTE,
                   [btn('Presentar un proyecto', L('ventanilla'), 'gold', icon='fas fa-plus')]) + [
        appbody([panel([tw('wakoo-t-projects', {'filters': 'yes', 'per': 12, 'cols': '3'})])]),
        appbody([panel([tw('wakoo-t-stages', {'zero': 'yes'})], 'Siete estados de preparación', 'fas fa-tasks')],
                [panel([iconlist([(f'{i + 1}. {t}', None, None) for i, t in enumerate(C.SHEET_10)], 'orn-numlist')], 'Qué contiene cada ficha', 'fas fa-file-alt'),
                 panel([defs(C.STAGES)], 'Qué significa cada estado', 'fas fa-book')], 'orn-app--sub'),
    ]


def page_ventanilla():
    return apphead('ventanilla', 'fas fa-concierge-bell', 'Ventanilla única del inversionista', 'Presente su iniciativa y siga su expediente',
                   'Un punto de contacto que acompaña al empresario desde la presentación inicial hasta la identificación de las autorizaciones necesarias.',
                   [btn('Mis solicitudes', L('mis-solicitudes'), 'light', icon='fas fa-folder-open')]) + [
        appbody([panel([p('Necesita una cuenta gratuita. Al enviar el formulario recibirá un código de seguimiento.', 'orn-small'), tw('wakoo-t-caseform')], 'Registrar una iniciativa', 'fas fa-plus-circle'),
                 panel([bullets(C.LOCATION_SERVICES, 'fas fa-check')], 'Información que puede solicitar', 'fas fa-map-signs')],
                [callout('Qué hace y qué no hace la ventanilla', C.WINDOW_NOTE, 'fas fa-balance-scale'),
                 panel([defs(C.WINDOW_STEPS, 'orn-defs--steps')], 'Procedimiento en siete pasos', 'fas fa-route')]),
    ]


def page_panel(key, title, lead, widget, settings=None):
    tabs = ACCOUNT + [('hub', 'Hub', 'fas fa-user-shield')] if key == 'hub' else ACCOUNT
    ic = dict((k, i) for k, _t, i in tabs + [('verificar', '', 'fas fa-certificate')]).get(key, 'fas fa-user-circle')
    return apphead(key, ic, 'Mi cuenta', title, lead, tabs=tabs, area='Mi cuenta') + [appbody([panel([tw(widget, settings)])])]


def page_mapa():
    return apphead('mapa', 'fas fa-map-marked-alt', 'Mapa del territorio', 'Mapa de la Subregión Orinoco', 'Google Maps con capas públicas que tienen fuente y fecha, y los proyectos cuya ubicación ya fue verificada.') + [
        appbody([panel([tw('wakoo-t-gis', {'engine': 'google', 'gtype': 'clean', 'projects': 'yes', 'filter': 'yes', 'center': '8.4,-64.3', 'zoom': 8})], cls='orn-apppanel--flush')]),
        appbody([panel([grid([col([icon(ic, 'orn-card__ico'), h(t, 4), p(d)], 'orn-mini') for ic, t, d, _i, _a in C.CORRIDORS], 3, tablet=1, mobile=1, gap=14),
                        p('Se describen aquí en texto hasta que la cartografía oficial permita dibujarlos con precisión.', 'orn-small')], 'Corredores de referencia', 'fas fa-route')],
                [callout('Cómo se publican las capas', 'El equipo carga capas desde Territorio → Importar al mapa (GeoJSON o CSV), indicando la fuente, la fecha y si la información está verificada. Nada se dibuja sin coordenadas con fuente.', 'fas fa-layer-group')], 'orn-app--sub'),
    ]


def page_directorio():
    return apphead('directorio', 'fas fa-building', 'Directorio empresarial B2B', 'Empresas y proveedores de la Subregión Orinoco', 'Perfiles revisados por el equipo, con nivel de verificación y formulario de consulta.',
                   [btn('Registrar una empresa', L('mi-empresa'), 'gold', icon='fas fa-plus')]) + [
        appbody([panel([tw('wakoo-t-companies', {'filters': 'yes', 'per': 12, 'register': lnk(L('mi-empresa'))})])]),
        appbody([panel([grid([col([icon(ic, 'orn-card__ico'), h(t, 4), p(d)], 'orn-mini') for ic, t, d in C.LEVELS], 3, tablet=1, mobile=1, gap=14)],
                       'Niveles de verificación', 'fas fa-shield-alt')], cls='orn-app--sub'),
    ]


def page_proveedores():
    return apphead('proveedores', 'fas fa-truck-loading', 'Proveedores', 'Proveeduría para operadoras, contratistas y empresas ancla', 'Una base regional de abastecimiento para las operaciones que efectivamente demanden servicios en el área de influencia.',
                   [btn('Registrar una empresa', L('mi-empresa'), 'gold', icon='fas fa-plus'), btn('Ver el directorio', L('directorio'), 'light', icon='fas fa-building')]) + [
        appbody([panel([p('Empresas registradas publican lo que necesitan comprar; los proveedores responden desde su cuenta.', 'orn-small'), tw('wakoo-t-needs')], 'Necesidades de compra abiertas', 'fas fa-clipboard-list')],
                [panel([defs(C.SUPPLIER_PROGRAM, 'orn-defs--steps')], 'Programa de Desarrollo de Proveedores', 'fas fa-hands-helping'),
                 callout('Sin contratos garantizados', C.SUPPLIER_NOTE)]),
        appbody([panel([grid([col([icon(ic, 'orn-card__ico'), h(t, 4), p(a), p(f'<strong>Infraestructura:</strong> {b}', 'orn-small')], 'orn-mini') for ic, t, a, b in C.CPPH], 3, tablet=2, mobile=1, gap=14)],
                       'Servicios a operadoras y contratistas', 'fas fa-cogs')],
                [panel([iconlist([(f'{i + 1}. {t}', None, None) for i, t in enumerate(C.GRADUAL)], 'orn-numlist')], 'Entrada gradual según la demanda real', 'fas fa-layer-group')], 'orn-app--sub'),
    ]


def page_observatorio():
    return apphead('observatorio', 'fas fa-chart-line', 'Observatorio', 'Indicadores con fuente, fecha y metodología', 'El seguimiento se concentra en resultados verificables. Cada indicador muestra su ficha técnica; los que aún no tienen línea base aparecen sin datos, nunca con cifras de relleno.') + [
        appbody([panel([tw('wakoo-t-observatory', {'cols': '2'})], cls='orn-apppanel--bare')],
                [panel([defs([('Ficha técnica', 'Unidad, fuente, periodicidad, responsable y metodología.'), ('Línea base', 'Se levanta en la Fase I con datos validados.'),
                              ('Verificación', 'Pendiente, en verificación o verificado, visible en cada tarjeta.'), ('Publicación', 'Solo datos autorizados y agregados; los datos de prueba nunca se muestran como oficiales.')], 'orn-defs--steps')],
                       'Cómo se publica un indicador', 'fas fa-clipboard-check')]),
    ]


def page_academia():
    schools = [reveal(iconbox(sc['icon'], sc['name'], sc['desc'], cls='orn-iconbox orn-school', position='top'), delay=i * 50) for i, sc in enumerate(C.SCHOOLS)]
    return [
        pagehead('Academia Orinoco de Nuevos Negocios', 'Formación para el empleo productivo y los nuevos negocios', C.ACADEMY_INTRO),
        section([head('Escuelas', 'Cinco escuelas'), grid(schools, 5, tablet=3, mobile=1, gap=18)], cls='orn-sec'),
        section([head('Cursos', 'Oferta de cursos', 'Toque un curso para ver su ficha. Los cursos en diseño aceptan registro de interés; el curso de demostración permite probar la plataforma completa.'),
                 tw('wakoo-t-courses', {'layout': 'icons', 'group': 'yes', 'demo': 'yes'})], cls='orn-sec orn-soft'),
        section([grid([col([head('Líneas del programa', 'Programa Regional de Formación para el Empleo Productivo'), *[iconbox('fas fa-check-circle', t, d, cls='orn-iconbox') for t, d in C.TRAINING_LINES]], 'orn-stack'),
                       col([head('Certificados verificables', 'Cada certificado tiene un código'), p('Al completar un curso, la academia emite un certificado con un código único. Cualquier empleador puede comprobarlo en línea.'),
                            btns([btn('Mi aprendizaje', L('mi-aprendizaje'), 'primary', icon='fas fa-user-graduate'), btn('Verificar un certificado', L('verificar'), 'outline')]),
                            p('Los cursos también pueden impartirse en un aula Moodle externa: cada curso admite un enlace a su aula.', 'orn-small')], 'orn-stack orn-panel')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
    ]


def page_noticias():
    return [
        pagehead('Noticias y agenda', 'Noticias, rondas de negocios y presentaciones', 'Novedades del portal y de la agenda de promoción de inversiones.'),
        section([grid([col([head('Agenda', 'Próximos encuentros'), tw('wakoo-events-list', {'count': 6, 'empty': 'Pronto anunciaremos las próximas rondas de negocios y presentaciones sectoriales.', 'accent': '#174A7E'})], 'orn-stack'),
                       col([head('Noticias', 'Publicaciones recientes'), w('wk-post-list', {'post_type': 'post', 'posts_per_page': 6, 'feature_image': 'yes', 'meta': 'yes', 'date_meta': 'yes'}, 'orn-posts'),
                            p('Las noticias se publican desde Entradas en el escritorio de WordPress.', 'orn-small')], 'orn-stack')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
    ]


def page_contacto():
    fields = [('text', 'Nombre y apellido', True, 50), ('email', 'Correo electrónico', True, 50), ('text', 'Organización o empresa', False, 50),
              ('select', 'Tema', True, 50, ['Inversión o proyecto', 'Proveedores y directorio', 'Academia', 'Prensa', 'Otro']), ('textarea', 'Mensaje', True, 100),
              ('acceptance', 'Acepto el tratamiento de mis datos para responder a este mensaje.', True, 100)]
    fl = []
    for f in fields:
        r = {'_id': el.eid(), 'ftype': f[0], 'flabel': f[1], 'frequired': 'yes' if f[2] else '', 'fwidth': str(f[3])}
        if len(f) > 4:
            r['foptions'] = '\n'.join(f[4])
        fl.append(r)
    return [
        pagehead('Contacto', 'Hablemos de su iniciativa', 'Para registrar un proyecto use la ventanilla: así recibe un código de seguimiento. Para otras consultas, escríbanos.'),
        section([grid([col([w('wakoo-form', {'fields': fl, 'button_text': 'Enviar mensaje', 'success_msg': 'Gracias. Su mensaje fue recibido y le responderemos por correo.',
                                             'form_name': 'Contacto ORINOCO BUSINESS', 'store': 'yes', 'email_subject': 'Contacto desde el portal', 'accent': '#10355B'}, 'orn-form')], 'orn-stack orn-panel'),
                       col([head('Datos de contacto', 'Canales institucionales'),
                            callout('Pendientes de validación', 'Los correos, teléfonos y direcciones oficiales se publicarán cuando la Mesa de Gobernanza y las alcaldías los confirmen. Mientras tanto, los mensajes llegan al correo del administrador del sitio.', 'fas fa-info-circle'),
                            btns([btn('Presentar un proyecto', L('ventanilla'), 'primary', icon='fas fa-arrow-right')])], 'orn-stack')], 2, tablet=1, mobile=1, gap=40, cls='orn-split')], cls='orn-sec'),
    ]


LEGAL = {
    'privacidad': ('Privacidad y datos personales', [
        ('Qué datos tratamos', 'Los datos de su cuenta (nombre, correo), los de las solicitudes que registra en la ventanilla, el perfil y los documentos de su empresa, su inscripción y progreso en la academia y los mensajes que envía.'),
        ('Para qué', 'Para gestionar su solicitud, el directorio, la academia y responder a sus mensajes. Los documentos de su expediente son privados: solo usted y el equipo autorizado pueden verlos.'),
        ('Seguridad', 'Los archivos se guardan fuera del acceso público y cada descarga queda registrada. Los indicadores del observatorio solo muestran datos agregados.'),
        ('Sus derechos', 'Puede pedir acceso, rectificación o supresión de sus datos por el formulario de contacto.'),
    ]),
    'terminos': ('Términos de uso', [
        ('Naturaleza del portal', 'Este portal informa, registra y hace seguimiento. Las iniciativas, mecanismos, incentivos y compromisos que describe son propuestas para evaluación y concertación, no beneficios vigentes.'),
        ('Ventanilla', 'La ventanilla no concede permisos, licencias ni autorizaciones, ni sustituye los procedimientos de ningún organismo.'),
        ('Directorio y proveedores', 'La información de cada empresa es responsabilidad de quien la publica. Ningún nivel de verificación garantiza contratos.'),
        ('Cifras', 'Las cifras se publican con su fuente y su estado de verificación. Una estimación nunca se presenta como dato verificado.'),
    ]),
    'accesibilidad': ('Accesibilidad', [
        ('Compromiso', 'El portal se diseña para cumplir las pautas WCAG 2.2 nivel AA: contraste suficiente, navegación con teclado, foco visible, textos alternativos y formularios con etiquetas.'),
        ('Movimiento', 'Los efectos animados se detienen si su sistema pide reducir el movimiento.'),
        ('Contacto', 'Si encuentra una barrera de accesibilidad, escríbanos por el formulario de contacto.'),
    ]),
}


def page_legal(key):
    title, parts = LEGAL[key]
    return [pagehead('Información legal', title, 'Texto base pendiente de revisión jurídica antes de la publicación oficial.'),
            section([col([x for t, d in parts for x in (h(t, 2), p(d))], 'orn-prose')], cls='orn-sec')]


# ------------------------------------------------------------------ plantillas de fichas

def tpl_sheet(widget, crumbs_label, crumbs_key):
    return [section([iconlist([('Inicio', None, L('inicio')), (crumbs_label, None, L(crumbs_key))], 'orn-crumbs orn-crumbs--light', inline=True),
                     tw(widget, {'contact': lnk(L('ventanilla'))} if widget == 'wakoo-t-project' else {})], cls='orn-sec orn-sheet', css_id='contenido')]


def tpl_course():
    title = w('heading', {'title': 'Curso', 'header_size': 'h1', '__dynamic__': {'title': '[elementor-tag id="orntitle" name="wakoo-post-title" settings="%7B%7D"]'}})
    head_ = section([col([iconlist([('Inicio', None, L('inicio')), ('Academia', None, L('academia'))], 'orn-crumbs', inline=True),
                          eyebrow('Academia Orinoco de Nuevos Negocios'), title], 'orn-pagehead__inner')], cls='orn-pagehead orn-pagehead--sm orn-dark', css_id='contenido')
    return [topo(head_, alpha=20, levels=10), section([tw('wakoo-t-course')], cls='orn-sec')]


# ------------------------------------------------------------------ ensamblado

PAGES = [
    # key, slug, title, builder, seo description, parent
    ('inicio', 'inicio', 'Inicio', page_inicio, C.INTRO, None),
    ('institucion', 'institucion', 'Presentación y visión', page_institucion, 'Presentación, visión estratégica, objetivos y principios rectores de ORINOCO BUSINESS & INVESTMENT.', None),
    ('territorio', 'territorio', 'Territorio y municipios', page_territorio, 'Ubicación, municipios, conectividad terrestre y fluvial de la Subregión Orinoco, sur de Anzoátegui.', None),
    ('sostenibilidad', 'desarrollo-sostenible', 'Desarrollo sostenible', page_sostenibilidad, 'Sostenibilidad ambiental, empleo local, seguridad y servicios públicos para la inversión en la Subregión Orinoco.', None),
    ('gobernanza', 'gobernanza', 'Gobernanza e inversión', page_gobernanza, 'Mesa de Gobernanza Económica, hoja de ruta, gobernanza contractual, indicadores e incentivos propuestos.', None),
    ('documentos', 'documentos', 'Documentos', page_documentos, 'Sala de documentos de ORINOCO BUSINESS & INVESTMENT: ponencia y documentación técnica.', None),
    ('sectores', 'sectores', 'Sectores', page_sectores, 'Diez sectores de oportunidad de inversión en la Subregión Orinoco.', None),
    ('proyectos', 'proyectos-de-inversion', 'Proyectos', page_proyectos, 'Cartera de proyectos de inversión de la Subregión Orinoco con estado de preparación.', None),
    ('ventanilla', 'ventanilla', 'Ventanilla única', page_ventanilla, 'Ventanilla Única del Inversionista: registre su iniciativa y siga su expediente.', None),
    ('mapa', 'mapa', 'Mapa del territorio', page_mapa, 'Mapa interactivo de la Subregión Orinoco con capas verificadas y proyectos.', None),
    ('directorio', 'directorio', 'Directorio B2B', page_directorio, 'Directorio empresarial B2B de la Subregión Orinoco.', None),
    ('proveedores', 'proveedores', 'Proveedores', page_proveedores, 'Proveeduría para operadoras, contratistas y empresas ancla; necesidades de compra.', None),
    ('observatorio', 'observatorio', 'Observatorio', page_observatorio, 'Observatorio de inversión y desarrollo: indicadores con ficha técnica.', None),
    ('academia', 'academia', 'Academia Orinoco', page_academia, 'Academia Orinoco de Nuevos Negocios: cinco escuelas y certificados verificables.', None),
    ('noticias', 'noticias', 'Noticias', page_noticias, 'Noticias, rondas de negocios y agenda de ORINOCO BUSINESS & INVESTMENT.', None),
    ('contacto', 'contacto', 'Contacto', page_contacto, 'Contacto con ORINOCO BUSINESS & INVESTMENT.', None),
    ('acceso', 'acceso', 'Acceso', lambda: page_panel('acceso', 'Iniciar sesión o crear una cuenta', 'Una sola cuenta para la ventanilla, el directorio y la academia.', 'wakoo-t-access', {'privacy': lnk(L('privacidad'))}), 'Acceso a la cuenta del portal.', None),
    ('mis-solicitudes', 'mis-solicitudes', 'Mis solicitudes', lambda: page_panel('mis-solicitudes', 'Mis solicitudes', 'Estado, historial, mensajes y documentos de sus solicitudes en la ventanilla.', 'wakoo-t-cases'), 'Solicitudes en la ventanilla.', None),
    ('mi-empresa', 'mi-empresa', 'Mi empresa', lambda: page_panel('mi-empresa', 'Mi empresa', 'Perfil para el directorio, documentos privados, consultas recibidas y necesidades de compra.', 'wakoo-t-companypanel'), 'Panel de empresa.', None),
    ('mi-aprendizaje', 'mi-aprendizaje', 'Mi aprendizaje', lambda: page_panel('mi-aprendizaje', 'Mi aprendizaje', 'Sus cursos, su progreso y sus certificados.', 'wakoo-t-student', {'catalog': lnk(L('academia'))}), 'Panel del estudiante.', None),
    ('hub', 'hub-administrativo', 'Hub administrativo', lambda: page_panel('hub', 'Hub administrativo', 'Solicitudes de la ventanilla, usuarios y cuentas de las empresas. Solo para el equipo del portal.', 'wakoo-t-hub'), 'Hub administrativo del equipo del portal.', None),
    ('verificar', 'verificar-certificado', 'Verificar certificado', lambda: page_panel('verificar', 'Verificar un certificado', 'Escriba el código impreso en el certificado de la Academia Orinoco.', 'wakoo-t-verify'), 'Verificación de certificados de la Academia Orinoco.', None),
    ('privacidad', 'privacidad', 'Privacidad', lambda: page_legal('privacidad'), 'Privacidad y datos personales.', None),
    ('terminos', 'terminos-de-uso', 'Términos de uso', lambda: page_legal('terminos'), 'Términos de uso del portal.', None),
    ('accesibilidad', 'accesibilidad', 'Accesibilidad', lambda: page_legal('accesibilidad'), 'Declaración de accesibilidad.', None),
]
for _sc in C.SECTORS:
    PAGES.append(('sector-' + _sc['slug'], _sc['slug'], _sc['name'], (lambda sc=_sc: page_sector(sc)), _sc['lead'], 'sectores'))

SECTOR_NAME = {sc['slug']: sc['name'] for sc in C.SECTORS}
PANELS = {'acceso', 'mis-solicitudes', 'mi-empresa', 'mi-aprendizaje', 'hub'}


def doc(data):
    return el.to_json([sticky_header(tpl(f'{LN}-header'))] + data + [tpl(f'{LN}-footer')])


def page_item(key, slug, title, data, desc, parent, order):
    it = {'key': f'{LN}-{key}', 'title': title, 'type': 'page', 'slug': slug, 'menu_order': order,
          'meta': {'_elementor_edit_mode': 'builder', '_wp_page_template': 'elementor_canvas', '_elementor_data': doc(data),
                   '_elementor_page_settings': {'hide_title': 'yes'}, '_wakoo_lang': LN, '_wakoo_tr': f'orinoco-{key}',
                   '_wakoo_seo_title': f'{title} | ORINOCO BUSINESS & INVESTMENT' if key != 'inicio' else f'ORINOCO BUSINESS & INVESTMENT · {C.SUB}',
                   '_wakoo_seo_desc': desc[:300]}}
    if parent:
        it['parent'] = f'{LN}-{parent}'
    return it


def template_item(key, title, data, kind='section', wrap=True):
    return {'key': f'{LN}-{key}', 'title': f'Orinoco · {title}', 'type': 'elementor_library',
            'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': kind, '_elementor_data': doc(data) if wrap else el.to_json(data),
                     '_wakoo_lang': LN, '_wakoo_tr': f'orinoco-{key}'}}


def content_items():
    items = []
    for i, pj in enumerate(C.PROJECTS):
        items.append({'key': f'pj-{pj["key"]}', 'title': pj['title'], 'type': 'wakoo_project', 'slug': pj['key'], 'menu_order': i,
                      'excerpt': pj['objective'], 'content': f'<p>{pj["desc"]}</p>',
                      'terms': {'wakoo_sector': [{'name': SECTOR_NAME[x], 'slug': x} for x in pj['sectors']]},
                      'meta': {'_wakoo_t_code': pj['code'], '_wakoo_t_stage': 'conceptual', '_wakoo_t_scale': pj['scale'], '_wakoo_t_objective': pj['objective'],
                               '_wakoo_t_precond': pj['precond'], '_wakoo_t_infra': pj['infra'], '_wakoo_t_location': 'Localización por definir',
                               '_wakoo_t_amount_kind': 'estimate', '_wakoo_t_source': 'Ponencia ORINOCO BUSINESS & INVESTMENT FORUM, 10.1 (21/10/2026)',
                               '_wakoo_t_pending': 'Localización georreferenciada\nInversión preliminar y estructura de financiamiento\nEstudios de factibilidad\nEmpleos directos e indirectos estimados\nResponsable autorizado',
                               '_wakoo_t_docs': f'Ponencia de referencia (PDF)|{img(C.PDF)}', '_wakoo_lang': LN}})
    for i, ind in enumerate(C.INDICATORS):
        m = {'_wakoo_t_' + k: ind[k] for k in ('auto', 'group', 'unit', 'chart', 'check', 'method', 'period', 'owner', 'source') if k in ind}
        m['_wakoo_t_public'] = 'yes'
        items.append({'key': f'ind-{i + 1}', 'title': ind['title'], 'type': 'wakoo_indicator', 'menu_order': i, 'excerpt': ind['excerpt'], 'meta': m})
    # A clearly marked test series, hidden unless the widget's «mostrar indicadores de prueba» is on.
    items.append({'key': 'ind-demo', 'title': 'Serie de prueba del observatorio', 'type': 'wakoo_indicator', 'menu_order': 99, 'excerpt': 'Datos inventados para revisar el diseño del gráfico. Nunca se muestran como oficiales.',
                  'meta': {'_wakoo_t_demo': 'yes', '_wakoo_t_public': 'yes', '_wakoo_t_chart': 'line', '_wakoo_t_unit': 'unidades de prueba', '_wakoo_t_check': 'pendiente',
                           '_wakoo_t_series': '2025-T1;4;no\n2025-T2;6;no\n2025-T3;5;no\n2025-T4;9;no\n2026-T1;11;no'}})
    # Capas de referencia del mapa: límites no oficiales con su fuente (nunca se marcan como verificados).
    geo = [('Estado Anzoátegui', 'anzoategui', 'limites-estado', 'Límite estatal de referencia. Fuente: Natural Earth (dominio público), escala 1:10 m.', 'Natural Earth 1:10m Admin 1 (dominio público)')]
    geo += [(f'Municipio {n}', n, 'municipios-subregion', 'Límite municipal de referencia, no oficial. Debe confirmarse con la cartografía oficial.',
             'C. E. Porto Tapiquén, «Municipios de Venezuela» (2015), vía geoBoundaries (ODbL 1.0)') for n in MUN_FILL]
    geo += [('Río Orinoco', 'orinoco', 'rio-orinoco', 'Eje central del río (referencia a pequeña escala).', 'Natural Earth 1:10m Rivers (dominio público)')]
    for i, (title, k, layer, desc, src) in enumerate(geo):
        items.append({'key': f'geo-{el_slug(k)}', 'title': title, 'type': 'wakoo_geo', 'menu_order': i, 'content': f'<p>{desc}</p>',
                      'terms': {'wakoo_geo_layer': [{'name': GEO_LAYERS[layer][0], 'slug': layer}]},
                      'meta': {'_wakoo_t_geojson': json.dumps(GEO[k], separators=(',', ':')), '_wakoo_t_public': 'yes', '_wakoo_t_verified': 'no',
                               '_wakoo_t_source': src, '_wakoo_t_date': 'Consultado el 28/10/2026'}})
    # Empresas públicas de la zona: perfiles de referencia con fuente, sin cuenta ni contactos privados.
    mun_name = {m['slug']: m['name'] for m in C.MUNICIPIOS}
    for i, co in enumerate(C.PUBLIC_COMPANIES):
        terms = {'wakoo_company_cat': [{'name': 'Empresas públicas', 'slug': 'empresas-publicas'}]}
        if co['sector']:
            terms['wakoo_sector'] = [{'name': SECTOR_NAME[co['sector']], 'slug': co['sector']}]
        if co['mun']:
            terms['wakoo_municipio'] = [{'name': mun_name[x], 'slug': x} for x in co['mun']]
        meta = {'_wakoo_t_level': 'referencia', '_wakoo_t_products': co['products'], '_wakoo_t_source': '\n'.join(co['sources'])}
        if co.get('photos'):
            meta['_wakoo_t_photo_src'] = '\n'.join(co['photos'])
        if co['web']:
            meta['_wakoo_t_web'] = co['web']
            meta['_wakoo_t_public'] = ['web']
        items.append({'key': f'co-{co["key"]}', 'title': co['title'], 'type': 'wakoo_company', 'slug': co['key'], 'menu_order': i,
                      'excerpt': co['excerpt'], 'content': co['content'], 'terms': terms, 'meta': meta})
    order = 0
    for sc in C.SCHOOLS:
        for t in sc['courses']:
            order += 1
            items.append({'key': f'c-{order}', 'title': t, 'type': 'wakoo_course', 'menu_order': order, 'excerpt': 'Curso en diseño. Registre su interés y le avisaremos cuando abra la inscripción.',
                          'content': f'<p>{sc["desc"]}</p><p>El programa, la duración, la modalidad y el costo se publicarán cuando el curso esté listo.</p>',
                          'terms': {'wakoo_school': [{'name': sc['name'], 'slug': sc['slug']}]},
                          'meta': {'_wakoo_t_cstatus': 'design', '_wakoo_t_cost': 'Por definir', '_wakoo_t_certify': 'yes', '_wakoo_t_icon': C.COURSE_ICONS.get(t, ''), '_wakoo_lang': LN}})
    d = C.DEMO_COURSE
    items.append({'key': 'c-demo', 'title': d['title'], 'type': 'wakoo_course', 'menu_order': 0, 'excerpt': d['excerpt'], 'content': f'<p>{d["content"]}</p>',
                  'terms': {'wakoo_school': [{'name': C.SCHOOLS[-1]['name'], 'slug': 'gestion-digital'}]},
                  'meta': {'_wakoo_t_cstatus': 'open', '_wakoo_t_demo': 'yes', '_wakoo_t_icon': C.COURSE_ICONS[d['title']], '_wakoo_t_mode': 'virtual', '_wakoo_t_certify': 'yes', '_wakoo_t_hours': '1',
                           '_wakoo_t_criteria': 'Completar las tres lecciones y aprobar la evaluación con 70 % o más.', '_wakoo_lang': LN}})
    for i, (t, body, quiz) in enumerate(d['lessons']):
        m = {'_wakoo_t_course': 'wakoo-pack://post/c-demo'}
        if quiz:
            m['_wakoo_t_quiz'] = json.dumps(quiz, ensure_ascii=False)
            m['_wakoo_t_pass'] = '70'
        items.append({'key': f'l-demo-{i + 1}', 'title': t, 'type': 'wakoo_lesson', 'menu_order': i + 1, 'content': body, 'meta': m})
    return items


LANGS = ['es', 'fr', 'en', 'zh-tw', 'it']  # mismo orden que Wakoo → Idiomas; el español es el maestro
LANG_NAMES = [['es', 'Español'], ['fr', 'Français'], ['en', 'English'], ['zh-tw', '繁體中文'], ['it', 'Italiano']]
_TRF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'traducciones.json')
TR = json.load(open(_TRF, encoding='utf-8')) if os.path.exists(_TRF) else {}
MISSING = {}

# Ajustes de widget que llevan texto visible (se traducen por idioma; el resto es configuración).
TXT_KEYS = {'title', 'editor', 'text', 'title_text', 'description_text', 'caption', 'toggle_label', 'label', 'empty', 'zoom_title', 'zoom_hint',
            'zoom_source', 'button_text', 'email_subject', 'form_name', 'success_msg', 'flabel', 'foptions', 'alt', 'legend', 'placeholder'}
# Campos de texto del contenido (proyectos, indicadores, cursos, lecciones).
META_TXT = {'_wakoo_t_objective', '_wakoo_t_precond', '_wakoo_t_infra', '_wakoo_t_location', '_wakoo_t_source', '_wakoo_t_pending', '_wakoo_t_cost',
            '_wakoo_t_criteria', '_wakoo_t_method', '_wakoo_t_period', '_wakoo_t_owner', '_wakoo_t_unit'}


def t_(text, ln=None):
    """Traducción de trabajo de un texto en español (traducciones.json); si falta, se anota y queda el español."""
    ln = ln or LN
    if ln == 'es' or not isinstance(text, str) or not text.strip() or text in ('yes', 'no') or not re.search('[A-Za-zÁ-ú]', text):
        return text
    v = TR.get(text, {}).get(ln)
    if v is None:
        MISSING.setdefault(text, set()).add(ln)
        return text
    return v


def tr_elements(els):
    for e in els:
        tr_settings(e.get('settings', {}))
        tr_elements(e.get('elements', []))
    return els


def tr_settings(st):
    for k, v in list(st.items()):
        if isinstance(v, str) and k in TXT_KEYS:
            st[k] = t_(v)
        elif isinstance(v, dict):
            tr_settings(v)
        elif isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    tr_settings(it)


def slug_for(key, slug, title):
    if LN == 'es':
        return slug
    if key == 'inicio':
        return LN
    return slug if LN == 'zh-tw' else (el_slug(t_(title)) or slug)


def localize_item(it):
    """Copia de un elemento del paquete en el idioma actual: textos, claves, enlaces y grupo de traducción."""
    it = json.loads(json.dumps(it, ensure_ascii=False))
    m = it.get('meta', {})
    if '_elementor_data' in m:
        m['_elementor_data'] = tr_elements(m['_elementor_data'])
    for k in ('title', 'excerpt'):
        if k in it and it.get('type') != 'elementor_library':
            it[k] = t_(it[k])
    if 'content' in it:
        it['content'] = t_(it['content'])
    for k in list(m):
        if k in META_TXT and isinstance(m[k], str):
            m[k] = '\n'.join(t_(x) for x in m[k].split('\n'))
        elif k in ('_wakoo_seo_title', '_wakoo_seo_desc'):
            m[k] = t_(m[k])
        elif k == '_wakoo_t_docs':
            m[k] = '\n'.join('|'.join([t_(x.split('|', 1)[0])] + x.split('|', 1)[1:]) for x in m[k].split('\n'))
        elif k == '_wakoo_t_quiz':
            q = json.loads(m[k])
            for x in q:
                x['q'] = t_(x['q'])
                x['options'] = [t_(o) for o in x['options']]
            m[k] = json.dumps(q, ensure_ascii=False)
        elif k == '_wakoo_t_course' and m[k].startswith('wakoo-pack://post/'):
            m[k] = m[k].replace('wakoo-pack://post/', f'wakoo-pack://post/{LN}-', 1)
    return it


def build(out, langs=LANGS):
    global LN
    items, menus, content_es = [], [], None
    for ln in langs:
        LN = ln
        el.LANG[0] = 'es'  # los textos se escriben en español y se traducen después
        el._counter = itertools.count(1)  # mismos ids de elemento en todos los idiomas (la sincronización los empareja)
        part = [template_item('header', 'Cabecera', header(), wrap=False), template_item('footer', 'Pie de página', footer(), wrap=False)]
        for i, (key, slug, title, fn, desc, parent) in enumerate(PAGES):
            it = page_item(key, slug, title, fn(), desc, parent, i)
            if ln != 'es':
                it['slug'] = slug_for(key, slug, title)
                if key != 'inicio':
                    it['parent'] = f'{ln}-{parent}' if parent else f'{ln}-inicio'
            part.append(it)
        part += [template_item('tpl-proyecto', 'Ficha de proyecto', tpl_sheet('wakoo-t-project', 'Proyectos', 'proyectos'), 'page'),
                 template_item('tpl-empresa', 'Ficha de empresa', tpl_sheet('wakoo-t-company', 'Directorio', 'directorio'), 'page'),
                 template_item('tpl-curso', 'Ficha de curso', tpl_course(), 'page')]
        if ln != 'es':
            part = [localize_item(x) for x in part]
            for x in part:
                if x['type'] == 'elementor_library':
                    x['title'] = x['title'].replace('Orinoco · ', 'Orinoco · ') + f' ({ln.upper()})'
        items += part
        menus.append({'key': f'main-{ln}', 'name': f'Orinoco · Menú principal ({ln.upper()})',
                      'items': [{'title': t_(m['title']), 'link': m['link'], 'children': [{'title': t_(c['title']), 'link': c['link']} for c in m['children']]} for m in menu_tree()]})
        # Contenido traducible: proyectos, indicadores, cursos y lecciones (las empresas y las capas del mapa son únicas).
        LN = 'es'
        if content_es is None:
            content_es = content_items()
            items += content_es
        LN = ln
        if ln != 'es':
            for x in content_es:
                if x['type'] not in ('wakoo_project', 'wakoo_indicator', 'wakoo_course', 'wakoo_lesson'):
                    continue
                y = localize_item(x)
                y['key'] = f'{ln}-{x["key"]}'
                if 'slug' in y:
                    y['slug'] = f'{x["slug"]}-{ln}'
                y.setdefault('meta', {})['_wakoo_lang'] = ln
                y['meta']['_wakoo_tr'] = f'orinoco-{x["key"]}'
                if 'terms' in y:
                    y['terms'] = x['terms']
                items.append(y)
    LN = 'es'
    for x in content_es:
        if x['type'] in ('wakoo_project', 'wakoo_indicator', 'wakoo_course', 'wakoo_lesson'):
            x.setdefault('meta', {})['_wakoo_lang'] = 'es'
            x['meta']['_wakoo_tr'] = f'orinoco-{x["key"]}'

    def names(n):
        return {f'wk_name_{l.replace("-", "_")}': TR[n][l] for l in langs if l != 'es' and TR.get(n, {}).get(l)}

    terms = {
        'wakoo_sector': [{'name': sc['name'], 'slug': sc['slug'], 'meta': {'wk_order': i + 1, **names(sc['name'])}} for i, sc in enumerate(C.SECTORS)],
        'wakoo_municipio': [{'name': m['name'], 'slug': m['slug'], 'description': m['focus'], 'meta': {'wk_order': i + 1}} for i, m in enumerate(C.MUNICIPIOS)],
        'wakoo_school': [{'name': sc['name'], 'slug': sc['slug'], 'description': sc['desc'], 'meta': {'wk_order': i + 1, 'wk_icon': sc['icon'], **names(sc['name'])}} for i, sc in enumerate(C.SCHOOLS)],
        'wakoo_company_cat': [{'name': n, 'slug': el_slug(n), 'meta': {'wk_order': i + 1, **names(n)}} for i, n in enumerate(COMPANY_CATS)],
        'wakoo_geo_layer': [{'name': n, 'slug': sl, 'meta': {'wk_order': i + 1, 'wk_color': c, **names(n)}} for i, (sl, (n, c)) in enumerate(GEO_LAYERS.items())] +
                           [{'name': n, 'slug': el_slug(n), 'meta': {'wk_order': i + 10, 'wk_color': c, **names(n)}} for i, (n, c) in enumerate(EXTRA_LAYERS)],
    }
    for n in [x['name'] for v in terms.values() for x in v if x not in terms['wakoo_municipio']]:
        for l in langs:
            if l != 'es':
                t_(n, l)
    # Palabras de la interfaz de los widgets Territorio (estados, botones, avisos) en cada idioma.
    i18n = {}
    for l in langs:
        if l == 'es':
            continue
        i18n[l] = {}
        # Company excerpts too: companies stay single Spanish posts, the listings translate their summary.
        for es in UI_STRINGS + [x['excerpt'] for x in C.PUBLIC_COMPANIES]:
            v = t_(es, l)
            if v != es:
                i18n[l][es] = v
    pack = {
        'format': 'wakoo-export', 'version': 1, 'pack': PACK,
        'title': 'ORINOCO BUSINESS & INVESTMENT · Portal institucional (Subregión Orinoco)',
        'items': items,
        'menus': menus,
        'media': {f'images/{n}': {'alt': a} for n, a in [
            ('puente-angostura.webp', 'Puente Angostura sobre el río Orinoco'), ('puente-orinoquia.webp', 'Vista aérea del Puente Orinoquia sobre el río Orinoco'),
            ('embarcadero-flotante.webp', 'Embarcadero flotante en la ribera del Orinoco'), ('cultivos-yuca-maiz.webp', 'Productores en un cultivo de yuca y maíz'),
            ('pesca-acuicultura.webp', 'Productores junto a una laguna de cultivo de peces'), ('plantacion-forestal-uverito.webp', 'Vista aérea de una plantación forestal'),
            ('taller-metalmecanico.webp', 'Soldador en un taller industrial'), ('operaciones-planta-energia.webp', 'Operarios en una planta de energía'),
            ('rio-curiaras.webp', 'Curiaras en la orilla de un río'), ('franja-territorio.webp', 'Ilustración del río, la industria, la agroindustria y el puerto'),
            (C.PDF, 'Ponencia ORINOCO BUSINESS & INVESTMENT FORUM')]},
        'site': {
            'front_page': 'es-inicio',
            'css_file': 'styles/orinoco.css',
            'options': {'blogname': 'ORINOCO BUSINESS & INVESTMENT', 'blogdescription': C.SUB, 'elementor_google_font': '0', 'elementor_font_display': 'swap',
                        'elementor_disable_color_schemes': 'yes', 'elementor_disable_typography_schemes': 'yes'},
            'wakoo': {
                'languages': [x for x in LANG_NAMES if x[0] in langs],
                'public_default': 'es',
                'seo': {'org_name': 'ORINOCO BUSINESS & INVESTMENT', 'meta_desc': 1, 'og': 1, 'jsonld': 1, 'llms': 1},
                'territorio': {
                    'tpl_project': 'es-tpl-proyecto', 'tpl_company': 'es-tpl-empresa', 'tpl_course': 'es-tpl-curso',
                    'page_access': 'es-acceso', 'page_cases': 'es-mis-solicitudes', 'page_cases_new': 'es-ventanilla', 'page_company': 'es-mi-empresa',
                    'page_student': 'es-mi-aprendizaje', 'page_verify': 'es-verificar', 'page_hub': 'es-hub',
                    'prefix': 'ORI', 'center': '8.4,-64.3', 'zoom': 8, 'register': 1, 'issuer': 'Academia Orinoco de Nuevos Negocios',
                    'terms': terms, 'i18n': i18n,
                },
            },
        },
    }
    os.makedirs(out, exist_ok=True)
    json.dump(pack, open(os.path.join(out, 'wakoo-pack.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    miss = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faltan-traducciones.json')
    if MISSING:
        json.dump({k: sorted(v) for k, v in MISSING.items()}, open(miss, 'w'), ensure_ascii=False, indent=1)
    elif os.path.exists(miss):
        os.remove(miss)
    return pack


COMPANY_CATS = ['Empresas públicas', 'Transporte especializado', 'Izamiento y manejo de cargas', 'Tubulares y componentes', 'Mantenimiento industrial',
                'Fabricación metalmecánica', 'Seguridad industrial', 'Servicios al personal', 'Tecnología operacional', 'Servicios ambientales',
                'Producción agropecuaria y alimentos', 'Comercio y otros servicios']
EXTRA_LAYERS = [('Corredores viales', '#C5A15B'), ('Accesos fluviales y embarcaderos', '#2A6DB0'), ('Zonas industriales y logísticas', '#10355B'),
                ('Servicios públicos', '#1E6B45'), ('Áreas de preservación', '#4F7A3A')]
# Textos de la interfaz del módulo Territorio (los genera herramientas: ver BITACORA). Se traducen como el resto.
UI_STRINGS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'interfaz-territorio.json'), encoding='utf-8'))


def el_slug(t):
    import unicodedata, re
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


if __name__ == '__main__':
    pk = build(sys.argv[1] if len(sys.argv) > 1 else 'pack', sys.argv[2].split(',') if len(sys.argv) > 2 else LANGS)
    print(len(pk['items']), 'items', f'· faltan {len(MISSING)} traducciones' if MISSING else '')
