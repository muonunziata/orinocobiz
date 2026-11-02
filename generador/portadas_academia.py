"""Portadas de los cursos de la Academia Orinoco (pack/images/academia/<clave>.webp).

Gráficos de marca, no fotos: fondo azul de la marca (con la foto de la ponencia de la escuela, oscurecida, cuando la hay),
líneas topográficas en dorado, el icono del curso (Font Awesome 5 Free, SIL OFL 1.1 / CC BY 4.0) y el nombre de la escuela.
Se ejecuta a mano cuando cambian los cursos: python3 portadas_academia.py
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import academia
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'pack', 'images', 'academia')
FA = '/root/wakoo-env/elementor-build/assets/lib/font-awesome/webfonts/fa-solid-900.ttf'
W, H = 1200, 675
NAVY, DEEP, GOLD = (16, 53, 91), (10, 36, 64), (197, 161, 91)

# Foto de la ponencia que acompaña a cada curso (None = solo gráfico) e icono (código de Font Awesome 5 solid).
ART = {
    'tecnico-a-proveedor': ('taller-metalmecanico', ''),     # tools
    'formalizacion': (None, ''),                             # file-signature
    'seguridad-industrial': ('operaciones-planta-energia', ''),  # hard-hat
    'proveer-operadoras': ('operaciones-planta-energia', ''),    # handshake
    'inocuidad': ('cultivos-yuca-maiz', ''),                  # utensils
    'cadena-frio': ('pesca-acuicultura', ''),                 # snowflake
    'inventarios': (None, ''),                                # boxes
    'documentacion-carga': ('embarcadero-flotante', ''),      # ship
    'administracion': (None, ''),                             # calculator
    'comercio-electronico': (None, ''),                       # shopping-cart
}


def font(size, bold=True):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def topo(draw, seed):
    rnd = random.Random(seed)
    cx, cy = W * (0.62 + rnd.random() * 0.2), H * (0.3 + rnd.random() * 0.4)
    for k in range(14):
        r = 60 + k * 46
        pts = []
        for a in range(0, 361, 6):
            t = math.radians(a)
            wob = 1 + 0.08 * math.sin(3 * t + k * 0.7 + seed) + 0.05 * math.cos(5 * t + seed)
            pts.append((cx + r * wob * math.cos(t) * 1.25, cy + r * wob * math.sin(t)))
        draw.line(pts, fill=GOLD + (34 if k % 3 else 60,), width=2)


def cover(c, school):
    photo, ic = ART[c['clave']]
    base = Image.new('RGB', (W, H), NAVY)
    if photo:
        ph = Image.open(os.path.join(HERE, 'pack', 'images', photo + '.webp')).convert('RGB')
        s = max(W / ph.width, H / ph.height)
        ph = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
        base.paste(ph.crop((0, 0, W, H)), (0, 0))
    # Gradient from deep navy (left, under the text) to a translucent navy (right).
    grad = Image.new('RGBA', (W, H))
    gd = ImageDraw.Draw(grad)
    for x in range(W):
        a = int(250 - 120 * (x / W)) if photo else 255
        col = tuple(int(DEEP[i] + (NAVY[i] - DEEP[i]) * x / W) for i in range(3))
        gd.line([(x, 0), (x, H)], fill=col + (a,))
    img = Image.alpha_composite(base.convert('RGBA'), grad)
    lines = Image.new('RGBA', (W, H))
    topo(ImageDraw.Draw(lines), sum(map(ord, c['clave'])))
    img = Image.alpha_composite(img, lines)
    d = ImageDraw.Draw(img)
    # Icon in a gold circle.
    # Everything sits inside the central 4:3 area: the course header shows the cover cropped to about 4:3.
    r = 84
    cx, cy = 290, 230
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD + (255,))
    f = ImageFont.truetype(FA, 84)
    bb = d.textbbox((0, 0), ic, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), ic, font=f, fill=DEEP + (255,))
    # School name and the academy.
    x0, y = 206, 360
    for ln in wrap(d, school.upper(), font(28), 800):
        d.text((x0, y), ln, font=font(28), fill=(255, 255, 255, 255))
        y += 40
    d.rectangle([x0, y + 10, x0 + 72, y + 14], fill=GOLD + (255,))
    d.text((x0, y + 34), 'ACADEMIA ORINOCO DE NUEVOS NEGOCIOS', font=font(20, False), fill=(220, 229, 239, 255))
    os.makedirs(OUT, exist_ok=True)
    img.convert('RGB').save(os.path.join(OUT, c['clave'] + '.webp'), 'WEBP', quality=82, method=6)


def wrap(d, text, f, width):
    out, cur = [], ''
    for wd in text.split():
        t = (cur + ' ' + wd).strip()
        if cur and d.textlength(t, font=f) > width:
            out.append(cur)
            cur = wd
        else:
            cur = t
    return out + [cur]


def short(name):
    return name.replace('Escuela de ', '').replace('Escuela ', '')


if __name__ == '__main__':
    schools = {sc['slug']: sc['name'] for sc in C.SCHOOLS}
    for c in academia.cursos():
        cover(c, short(schools[c['escuela']]))
    print(len(academia.cursos()), 'portadas en', OUT)
