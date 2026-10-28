"""Small builder for Elementor (flexbox container) JSON used by the ORINOCO BUSINESS pack
(copied from the ICGlobal generator; same helpers).

Every helper returns a plain dict in Elementor's _elementor_data shape. Text can be a
str or a T(es, en, zh) object; render(lang) resolves it. Links to other portal pages are
written as wakoo-pack://link/<lang>-<key>, which the Wakoo importer turns into real URLs.
"""
import hashlib, itertools, json, os

_counter = itertools.count(1)
LANG = ['es']  # current language while building


# Traducciones de trabajo a francés, italiano y chino tradicional (Taiwán), por texto en español.
# fr/it: traducción propia pendiente de revisión nativa. zh-tw: el chino simplificado convertido con
# OpenCC (s2twp, Apache-2.0) y guardado aquí para no depender de OpenCC al generar.
_TR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'traducciones.json')
TR = json.load(open(_TR_FILE, encoding='utf-8')) if os.path.exists(_TR_FILE) else {}
MISSING = set()


def _zh_tw(zh):
    try:
        from opencc import OpenCC
    except ImportError:
        return None
    return OpenCC('s2twp').convert(zh)


class T:
    def __init__(self, es, en=None, zh=None, fr=None, it=None, zh_tw=None):
        en = en if en is not None else es
        zh = zh if zh is not None else en
        t = TR.get(es, {}) if es else {}
        self.v = {'es': es, 'en': en, 'zh': zh,
                  'fr': fr if fr is not None else t.get('fr'),
                  'it': it if it is not None else t.get('it'),
                  'zh-tw': zh_tw if zh_tw is not None else (t.get('zh-tw') or _zh_tw(zh))}
        for k in ('fr', 'it', 'zh-tw'):
            if self.v[k] is None:
                MISSING.add((k, es))
                self.v[k] = es

    def __str__(self):
        return self.v[LANG[0]]

    def __add__(self, o):
        return str(self) + str(o)

    def __radd__(self, o):
        return str(o) + str(self)


def s(x):
    """Resolve T or str (or list of them) to the current language."""
    if isinstance(x, T):
        return x.v[LANG[0]]
    if isinstance(x, (list, tuple)):
        return ''.join(s(i) for i in x)
    return '' if x is None else str(x)


def eid():
    n = next(_counter)
    return hashlib.md5(f'orn{n}'.encode()).hexdigest()[:7]


def link(key, anchor=''):
    """Internal page link for the current language."""
    if key.startswith(('http', 'mailto:', 'tel:', '#')):
        return key
    return f'wakoo-pack://link/{key_prefix()}-{key}' + (('#' + anchor) if anchor else '')


def key_prefix(lang=None):
    """Pack key prefix per language. Traditional Chinese keeps the old «zh» keys so that a
    replace-import updates the pages of the earlier zh pack instead of leaving them behind."""
    lang = lang or LANG[0]
    return 'zh' if lang == 'zh-tw' else lang


def img(path):
    return f'wakoo-pack://images/{path}'


def pad(t, r=None, b=None, l=None, unit='px'):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}


# ------------------------------------------------------------------ containers

def con(children, cls='', direction='column', boxed=False, gap=None, settings=None, css_id='', tag=None, inner=False):
    st = {
        'content_width': 'boxed' if boxed else 'full',
        'flex_direction': direction,
        'padding': pad(0),
    }
    if direction == 'row':
        st['flex_wrap'] = 'wrap'
    if gap is not None:
        st['flex_gap'] = {'unit': 'px', 'size': gap, 'column': str(gap), 'row': str(gap), 'isLinked': True}
    if cls:
        st['css_classes'] = cls
    if css_id:
        st['_element_id'] = css_id
    if tag:
        st['html_tag'] = tag
    if settings:
        st.update(settings)
    return {'id': eid(), 'elType': 'container', 'isInner': inner, 'settings': st, 'elements': [c for c in children if c]}


def section(children, cls='orn-sec', bg=None, overlay=None, css_id='', tag='section', label=None):
    """Full-width band with boxed inner content. bg = image path in the pack."""
    st = {}
    if bg:
        st.update({
            'background_background': 'classic',
            'background_image': {'url': img(bg), 'id': '', 'alt': ''},
            'background_position': 'center center',
            'background_size': 'cover',
        })
    if overlay:
        st.update({
            'background_overlay_background': 'gradient',
            'background_overlay_color': overlay[0],
            'background_overlay_color_b': overlay[1],
            'background_overlay_gradient_angle': {'unit': 'deg', 'size': overlay[2] if len(overlay) > 2 else 100},
            'background_overlay_opacity': {'unit': 'px', 'size': 1},
        })
    return con(children, cls=cls, boxed=True, settings=st, css_id=css_id, tag=tag)


def grid(children, cols=3, cls='', tablet=2, mobile=1, gap=24):
    st = {
        'container_type': 'grid',
        'grid_columns_grid': {'unit': 'fr', 'size': cols},
        'grid_columns_grid_tablet': {'unit': 'fr', 'size': tablet},
        'grid_columns_grid_mobile': {'unit': 'fr', 'size': mobile},
        'grid_rows_grid': {'unit': 'fr', 'size': 1},
        'grid_auto_flow': 'row',
        'grid_gaps': {'unit': 'px', 'size': gap, 'column': str(gap), 'row': str(gap), 'isLinked': True},
        'content_width': 'full',
        'padding': pad(0),
    }
    if cls:
        st['css_classes'] = cls
    return {'id': eid(), 'elType': 'container', 'isInner': True, 'settings': st, 'elements': [c for c in children if c]}


def col(children, cls='', gap=None, tag=None):
    return con(children, cls=cls, gap=gap, inner=True, tag=tag)


def row(children, cls='', gap=24):
    return con(children, cls=cls, direction='row', gap=gap, inner=True)


# ------------------------------------------------------------------ widgets

def w(kind, settings, cls=''):
    st = dict(settings)
    if cls:
        st['_css_classes'] = cls
    return {'id': eid(), 'elType': 'widget', 'widgetType': kind, 'settings': st, 'elements': []}


def h(text, level=2, cls='', url=None, css_id=''):
    st = {'title': s(text), 'header_size': level if isinstance(level, str) else f'h{level}'}
    if css_id:
        st['_element_id'] = css_id
    if url:
        st['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return w('heading', st, cls)


def eyebrow(text, cls=''):
    return w('heading', {'title': s(text), 'header_size': 'p'}, ('orn-eyebrow ' + cls).strip())


def p(html, cls=''):
    html = s(html)
    if not html.lstrip().startswith('<'):
        html = f'<p>{html}</p>'
    return w('text-editor', {'editor': html}, cls)


def ul(items, cls=''):
    return p('<ul>' + ''.join(f'<li>{s(i)}</li>' for i in items) + '</ul>', ('orn-list ' + cls).strip())


def btn(text, url, kind='primary', cls='', external=False, icon=None):
    st = {'text': s(text), 'link': {'url': url, 'is_external': 'on' if external else '', 'nofollow': ''}, 'size': 'md'}
    if icon:
        st['selected_icon'] = fa(icon)
        st['icon_align'] = 'row-reverse'
        st['icon_indent'] = {'unit': 'px', 'size': 8}
    return w('button', st, f'orn-btn orn-btn--{kind} {cls}'.strip())


def btns(items, cls=''):
    return row(items, cls=('orn-btns wk-keep-row ' + cls).strip(), gap=12)


def image(path, alt, caption=None, cls='', size='large', w_=None, h_=None, lazy=True):
    st = {'image': {'url': img(path), 'id': '', 'alt': s(alt), 'source': 'library'}, 'image_size': size}
    if caption:
        st['caption_source'] = 'custom'
        st['caption'] = s(caption)
    return w('image', st, ('orn-img ' + cls).strip())


def fa(name):
    """Font Awesome 5 icon as Elementor stores it: 'fab fa-whatsapp' or 'fas fa-phone'."""
    lib = {'fab': 'fa-brands', 'far': 'fa-regular'}.get(name.split()[0], 'fa-solid')
    return {'value': name, 'library': lib}


def lnk(url, external=None):
    if external is None:
        external = url.startswith('http') and not url.startswith('wakoo-pack://')
    return {'url': url, 'is_external': 'on' if external else '', 'nofollow': ''}


def icon(name, cls='', url=None):
    st = {'selected_icon': fa(name), 'view': 'default', 'align': 'start'}
    if url:
        st['link'] = lnk(url)
    return w('icon', st, ('orn-ico ' + cls).strip())


def iconlist(items, cls='', inline=False):
    """items: (text, icon or None, url or None)."""
    rows = []
    for text, ic, url in items:
        r = {'_id': eid(), 'text': s(text), 'selected_icon': fa(ic) if ic else {'value': '', 'library': ''}}
        if url:
            r['link'] = lnk(url)
        rows.append(r)
    st = {'icon_list': rows, 'view': 'inline' if inline else 'traditional'}
    return w('icon-list', st, cls)


def social(items, cls=''):
    """items: (icon, url)."""
    rows = [{'_id': eid(), 'social_icon': fa(ic), 'link': lnk(url, True if url.startswith('http') else False)} for ic, url in items]
    return w('social-icons', {'social_icon_list': rows, 'shape': 'circle', 'icon_color': 'custom', 'align': 'left'}, ('orn-social ' + cls).strip())


def iconbox(ic, title, desc='', url=None, cls='', position='left'):
    st = {'selected_icon': fa(ic), 'title_text': s(title), 'description_text': s(desc), 'position': position, 'title_size': 'span'}
    if url:
        st['link'] = lnk(url)
    return w('icon-box', st, cls)


def only(node, lang):
    """Element shown only in one language (Advanced → Idioma, Wakoo)."""
    node['settings']['wk_lang_only'] = lang
    return node


def html(code, cls=''):
    return w('html', {'html': s(code)}, cls)


def sc(code, cls=''):
    return w('shortcode', {'shortcode': code}, cls)


def spacer(px=24):
    return w('spacer', {'space': {'unit': 'px', 'size': px}})


def tpl(key):
    """Saved template (header/footer) by pack key."""
    return w('wk-template', {'template_id': f'wakoo-pack://post/{key}'}, 'orn-tpl')


def to_json(elements):
    return json.loads(json.dumps(elements, ensure_ascii=False))
