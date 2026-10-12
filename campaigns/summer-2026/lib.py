"""Shared vector building blocks for the Babalas Rescue+ "Hang in there, Mzansi" summer campaign.

Every artboard is plain SVG (opens as editable vector artwork in Adobe Illustrator).
Run build.py to regenerate all artboards, previews and the multi-artboard PDF.
"""
import re, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"

# ---- palette (brand + derived campaign tints) -------------------------------------------
BLUE, YEL, PINK, NIGHT, WHITE = "#2CACEF", "#FDEA12", "#F6009D", "#0B2A40", "#FFFFFF"
DEEP = "#0F5F8F"      # derived deep blue (brand guide)
SKY = "#E6F6FD"       # derived pale blue
SUN = "#FFFBD1"       # derived pale yellow
BLUE2 = "#8FD3F6"     # 50% tint of Babalas Blue (campaign: sea / distant hills)
YEL2 = "#FFF48A"      # 50% tint of Rescue Yellow (campaign: sand / light)

DISPLAY = "'Futura PT','Futura','Futura LT Pro','Jost',sans-serif"
BODY = "'Montserrat',sans-serif"

# ---- logo parts from the supplied vector logo -----------------------------------------------
def _paths(svgfile):
    s = (BRAND / "logo" / svgfile).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    ds = re.findall(r'<path d="([^"]+)"', s)
    return vb, ds

ICON_VB, ICON_D = _paths("babalas-icon-yellow.svg")
WORD_VB, WORD_D = _paths("babalas-wordmark-yellow.svg")
LOGO_VB, LOGO_D = _paths("babalas-logo-yellow.svg")


def _climber_clip():
    """Polygon (icon user units) that keeps the climber and drops the cliff."""
    im = Image.open(BRAND / "logo" / "babalas-icon-yellow.png").getchannel("A")
    W, H = im.size
    px = im.load()
    sx, sy = ICON_VB[2] / W, ICON_VB[3] / H
    def runs(y):
        r, inside = [], False
        for x in range(W):
            on = px[x, y] > 128
            if on and not inside:
                s, inside = x, True
            if not on and inside:
                r.append((s, x - 1)); inside = False
        if inside:
            r.append((s, W - 1))
        return r
    mids = []
    for y in range(0, H, 3):
        r = runs(y)
        if len(r) >= 2 and r[1][0] > W * 0.5 or (mids and len(r) >= 2):
            mids.append(((r[0][1] + r[1][0]) / 2, y))
        elif mids and y < H * 0.75:
            mids = []   # separation not sustained yet (jagged cliff-top bumps); restart
    y0 = mids[0][1]
    pts = [(mids[0][0], y0), (W + 10, y0), (W + 10, H + 10), (mids[-1][0], H + 10)]
    pts += [(x, y) for x, y in reversed(mids)]
    pts = [(ICON_VB[0] + x * sx, ICON_VB[1] + y * sy) for x, y in pts]
    # grip point = centre of the wrist on the first separated row
    r = runs(y0)
    grip = (ICON_VB[0] + (r[1][0] + r[1][1]) / 2 * sx, ICON_VB[1] + y0 * sy)
    feet = ICON_VB[1] + 1650 / H * ICON_VB[3] if H > 1650 else ICON_VB[1] + ICON_VB[3]
    return pts, grip, feet

CLIP_PTS, GRIP, FEET_Y = _climber_clip()
CLIMB_H = FEET_Y - GRIP[1]


def defs():
    poly = " ".join(f"{x:.2f},{y:.2f}" for x, y in CLIP_PTS)
    icon = "".join(f'<path d="{d}"/>' for d in ICON_D)
    word = "".join(f'<path d="{d}"/>' for d in WORD_D)
    logo = "".join(f'<path d="{d}"/>' for d in LOGO_D)
    return f"""<defs>
<clipPath id="climberClip" clipPathUnits="userSpaceOnUse"><polygon points="{poly}"/></clipPath>
<g id="climber"><g clip-path="url(#climberClip)">{icon}</g></g>
<g id="icon">{icon}</g>
<g id="wordmark">{word}</g>
<g id="logo">{logo}</g>
</defs>"""


FONT_CSS = """<style>
@font-face{font-family:'Jost';font-weight:800;src:url('../../../brand/fonts/jost-latin-800-normal.woff2')}
@font-face{font-family:'Jost';font-weight:700;src:url('../../../brand/fonts/jost-latin-700-normal.woff2')}
@font-face{font-family:'Jost';font-weight:500;src:url('../../../brand/fonts/jost-latin-500-normal.woff2')}
@font-face{font-family:'Montserrat';font-weight:400;src:url('../../../brand/fonts/montserrat-latin-400-normal.woff2')}
@font-face{font-family:'Montserrat';font-weight:600;src:url('../../../brand/fonts/montserrat-latin-600-normal.woff2')}
@font-face{font-family:'Montserrat';font-weight:700;src:url('../../../brand/fonts/montserrat-latin-700-normal.woff2')}
</style>"""


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{title}</title>{FONT_CSS}{defs()}'
            f'<g id="artwork">{body}</g></svg>')

# ---- placement helpers ---------------------------------------------------------------------

def hang(x, y, height, fill=YEL, flip=False, rot=0, id_=None):
    """Climber hanging with his grip exactly at (x, y), body `height` tall."""
    s = height / CLIMB_H
    sx = -s if flip else s
    t = f"translate({x:.1f} {y:.1f}) rotate({rot}) scale({sx:.4f} {s:.4f}) translate({-GRIP[0]:.3f} {-GRIP[1]:.3f})"
    i = f' id="{id_}"' if id_ else ""
    return f'<g{i} fill="{fill}" transform="{t}"><use href="#climber" xlink:href="#climber"/></g>'


def icon(x, y, height, fill=YEL, flip=False):
    s = height / ICON_VB[3]
    sx = -s if flip else s
    return (f'<g fill="{fill}" transform="translate({x:.1f} {y:.1f}) scale({sx:.4f} {s:.4f}) '
            f'translate({-ICON_VB[0]:.3f} {-ICON_VB[1]:.3f})"><use href="#icon" xlink:href="#icon"/></g>')


def wordmark(x, y, width, fill=YEL):
    s = width / WORD_VB[2]
    return (f'<g id="logo-wordmark" fill="{fill}" transform="translate({x:.1f} {y:.1f}) scale({s:.4f}) '
            f'translate({-WORD_VB[0]:.3f} {-WORD_VB[1]:.3f})"><use href="#wordmark" xlink:href="#wordmark"/></g>')


def logo(x, y, width, fill=YEL):
    s = width / LOGO_VB[2]
    return (f'<g id="logo-lockup" fill="{fill}" transform="translate({x:.1f} {y:.1f}) scale({s:.4f}) '
            f'translate({-LOGO_VB[0]:.3f} {-LOGO_VB[1]:.3f})"><use href="#logo" xlink:href="#logo"/></g>')


def wordmark_h(width):
    return width * WORD_VB[3] / WORD_VB[2]


def text(x, y, lines, size, fill=NIGHT, weight=800, anchor="start", lh=0.98, font=DISPLAY, ls=-0.02, id_=None):
    if isinstance(lines, str):
        lines = [lines]
    i = f' id="{id_}"' if id_ else ""
    tsp = "".join(
        f'<tspan x="{x}" dy="{0 if n == 0 else size * lh:.1f}">{l}</tspan>' for n, l in enumerate(lines))
    return (f'<text{i} x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" '
            f'letter-spacing="{ls}em" fill="{fill}" text-anchor="{anchor}">{tsp}</text>')


def tagline(x, y, size, fill=NIGHT, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{DISPLAY}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="500"><tspan font-weight="800">bounce back</tspan> from your '
            f'<tspan font-weight="800">hangover</tspan></text>')


def legal(x, y, size=18, fill=NIGHT, anchor="start", opacity=0.85):
    return (f'<text x="{x}" y="{y}" font-family="{BODY}" font-weight="600" font-size="{size}" fill="{fill}" '
            f'opacity="{opacity}" text-anchor="{anchor}" letter-spacing="0.04em">PLEASE DRINK RESPONSIBLY · 18+</text>')


def hashtag(x, y, size=26, fill=NIGHT, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{DISPLAY}" font-weight="800" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="0.02em">#HangInThereMzansi</text>')


def pack(name, x, y, height, shadow=True):
    files = {"can": ("packshot-can-300ml.png", 1005, 1100), "sachet": ("packshot-sachet.png", 189, 1100),
             "box": ("packshot-sachet-box-6s.png", 1400, 1291), "4pack": ("packshot-can-4pack.png", 1400, 1166)}
    f, w0, h0 = files[name]
    w = height * w0 / h0
    sh = (f'<ellipse cx="{x + w / 2:.1f}" cy="{y + height * 0.985:.1f}" rx="{w * 0.42:.1f}" ry="{height * 0.025:.1f}" '
          f'fill="{NIGHT}" opacity="0.28"/>') if shadow else ""
    return (f'<g id="packshot-{name}">{sh}<image href="../../../brand/assets/{f}" xlink:href="../../../brand/assets/{f}" '
            f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{height:.1f}"/></g>')


def pack_w(name, height):
    r = {"can": 1005 / 1100, "sachet": 189 / 1100, "box": 1400 / 1291, "4pack": 1400 / 1166}[name]
    return height * r


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def pill(x, y, label, size=26, fill=NIGHT, color=WHITE, pad=22, anchor="start"):
    w = len(label) * size * 0.66 + pad * 2
    if anchor == "middle":
        x = x - w / 2
    h = size * 1.9
    return (f'<g><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{fill}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h * 0.66:.1f}" font-family="{DISPLAY}" font-weight="800" font-size="{size}" '
            f'fill="{color}" text-anchor="middle" letter-spacing="0.06em">{label}</text></g>')


def plus_badge(cx, cy, r, fill=YEL, color=BLUE):
    a = r * 0.55; b = r * 0.17
    return (f'<g id="plus-badge"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<rect x="{cx - a}" y="{cy - b}" width="{2 * a}" height="{2 * b}" rx="{b * 0.4}" fill="{color}"/>'
            f'<rect x="{cx - b}" y="{cy - a}" width="{2 * b}" height="{2 * a}" rx="{b * 0.4}" fill="{color}"/></g>')

# ---- illustration components (flat, silhouette style to match the logo) --------------------

def sun(cx, cy, r, fill=YEL, rays=True, ray_fill=None):
    out = []
    if rays:
        import math
        for i in range(16):
            a = i * math.pi / 8
            x1, y1 = cx + math.cos(a) * r * 1.18, cy + math.sin(a) * r * 1.18
            x2, y2 = cx + math.cos(a) * r * (1.55 if i % 2 == 0 else 1.38), cy + math.sin(a) * r * (1.55 if i % 2 == 0 else 1.38)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ray_fill or fill}" '
                       f'stroke-width="{r * 0.09:.1f}" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
    return f'<g id="sun">{"".join(out)}</g>'


def table_mountain(x, base, w, h, fill=DEEP, peaks=True):
    """Table Mountain with Devil's Peak (left) and Lion's Head (right). Returns (svg, table_top_y, right_edge_x)."""
    top = base - h
    L, R = x + w * 0.26, x + w * 0.74     # flat table between L and R
    d = (f"M{x} {base} L{x + w * 0.06} {base - h * 0.55} L{x + w * 0.12} {base - h * 1.08} "      # Devil's Peak
         f"L{x + w * 0.16} {base - h * 1.12} L{x + w * 0.2} {base - h * 0.9} L{L} {top} "
         f"L{R} {top + h * 0.01} L{R + w * 0.025} {base - h * 0.62} L{R + w * 0.06} {base - h * 0.46} "
         f"L{x + w * 0.86} {base - h * 0.42} ")
    if peaks:  # Lion's Head
        d += (f"L{x + w * 0.9} {base - h * 0.62} Q{x + w * 0.925} {base - h * 0.78} {x + w * 0.945} {base - h * 0.64} "
              f"L{x + w * 0.97} {base - h * 0.3} ")
    d += f"L{x + w} {base} Z"
    return f'<path id="table-mountain" d="{d}" fill="{fill}"/>', top, R, L


def tablecloth(L, R, top, fill=WHITE):
    """Signature 'tablecloth' cloud: a soft band on the flat top that spills down the front face."""
    w = R - L
    import random
    rnd = random.Random(3)
    d = f"M{L - w * 0.02:.1f} {top + 2:.1f} "
    n = 9
    for i in range(n):  # lumpy top
        x0 = L + w * i / n; x1 = L + w * (i + 1) / n
        d += f"Q{(x0 + x1) / 2:.1f} {top - w * rnd.uniform(0.025, 0.05):.1f} {x1:.1f} {top + 2:.1f} "
    d += f"L{R + w * 0.01:.1f} {top + w * 0.03:.1f} "
    for i in range(n, 0, -1):  # drips down the face
        x1 = L + w * (i - 1) / n; x0 = L + w * i / n
        d += f"Q{(x0 + x1) / 2:.1f} {top + w * rnd.uniform(0.06, 0.13):.1f} {x1:.1f} {top + w * 0.035:.1f} "
    d += "Z"
    return f'<path id="tablecloth-cloud" d="{d}" fill="{fill}"/>'


def waves(y, w, fill, amp=18, period=160, x0=0, h=2000):
    pts = [f"M{x0} {y}"]
    x = x0
    up = True
    while x < x0 + w:
        pts.append(f"Q{x + period / 4} {y - amp if up else y + amp} {x + period / 2} {y}")
        x += period / 2
        up = not up
    pts.append(f"L{x0 + w} {y + h} L{x0} {y + h} Z")
    return f'<path d="{" ".join(pts)}" fill="{fill}"/>'


def rugby_posts(cx, ground, bar_y, span, post_h, fill=WHITE, t=18):
    l, r = cx - span / 2, cx + span / 2
    pad = f'<rect x="{l - t * 1.4}" y="{ground - t * 9}" width="{t * 2.8}" height="{t * 9}" rx="{t * 0.6}" fill="{PINK}"/>' \
          f'<rect x="{r - t * 1.4}" y="{ground - t * 9}" width="{t * 2.8}" height="{t * 9}" rx="{t * 0.6}" fill="{PINK}"/>'
    return (f'<g id="rugby-posts" fill="{fill}">'
            f'<rect x="{l - t / 2}" y="{ground - post_h}" width="{t}" height="{post_h}" rx="{t / 2}"/>'
            f'<rect x="{r - t / 2}" y="{ground - post_h}" width="{t}" height="{post_h}" rx="{t / 2}"/>'
            f'<rect x="{l}" y="{bar_y - t / 2}" width="{span}" height="{t}" rx="{t / 2}"/>{pad}</g>')


def rugby_ball(cx, cy, rx, fill=YEL, seam=NIGHT, rot=-30):
    return (f'<g id="rugby-ball" transform="rotate({rot} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx * 0.6}" fill="{fill}"/>'
            f'<path d="M{cx - rx * 0.55} {cy} H{cx + rx * 0.55}" stroke="{seam}" stroke-width="{rx * 0.06}" stroke-linecap="round"/>'
            + "".join(f'<path d="M{cx + i * rx * 0.16} {cy - rx * 0.09} V{cy + rx * 0.09}" stroke="{seam}" stroke-width="{rx * 0.05}" stroke-linecap="round"/>' for i in (-2, -1, 0, 1, 2))
            + "</g>")


def braai(cx, top, w, fill=NIGHT, grid=WHITE):
    """Half-drum braai with grid; returns svg and grid y."""
    h = w * 0.42
    bars = "".join(f'<rect x="{cx - w / 2 + i * w / 11:.1f}" y="{top - 6}" width="{w * 0.018:.1f}" height="12" fill="{grid}"/>' for i in range(1, 11))
    legs = (f'<path d="M{cx - w * 0.36} {top + h * 0.8} L{cx - w * 0.44} {top + h * 2.1} M{cx + w * 0.36} {top + h * 0.8} '
            f'L{cx + w * 0.44} {top + h * 2.1} M{cx - w * 0.3} {top + h * 0.8} L{cx - w * 0.2} {top + h * 2.1} '
            f'M{cx + w * 0.3} {top + h * 0.8} L{cx + w * 0.2} {top + h * 2.1}" stroke="{fill}" stroke-width="{w * 0.025}" stroke-linecap="round"/>')
    flames = "".join(
        f'<path d="M{cx + dx} {top - 4} C{cx + dx - 24} {top - 50} {cx + dx + 8} {top - 70} {cx + dx + 4} {top - 110 - i * 10} '
        f'C{cx + dx + 30} {top - 70} {cx + dx + 34} {top - 40} {cx + dx + 22} {top - 4} Z" fill="{c}"/>'
        for i, (dx, c) in enumerate([(-w * 0.3, PINK), (-w * 0.12, YEL), (w * 0.05, PINK), (w * 0.22, YEL)]))
    return (f'<g id="braai">{flames}{legs}'
            f'<path d="M{cx - w / 2} {top} H{cx + w / 2} A{w / 2} {h} 0 0 1 {cx - w / 2} {top} Z" fill="{fill}"/>'
            f'<rect x="{cx - w / 2 - 10}" y="{top - 8}" width="{w + 20}" height="16" rx="8" fill="{grid}"/>{bars}</g>')


def wors(cx, cy, r, fill=PINK):
    """Boerewors coil."""
    return (f'<path id="boerewors" d="M{cx} {cy} m{-r} 0 a{r} {r} 0 1 0 {2 * r} 0 a{r * 0.75} {r * 0.75} 0 1 0 {-1.5 * r} 0 '
            f'a{r * 0.45} {r * 0.45} 0 1 0 {0.9 * r} 0" fill="none" stroke="{fill}" stroke-width="{r * 0.28}" stroke-linecap="round"/>')


def tongs(x1, y1, x2, y2, fill=WHITE, t=16):
    return (f'<g id="braai-tongs"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{fill}" stroke-width="{t}" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1 + t * 1.6}" x2="{x2}" y2="{y2 + t * 0.6}" stroke="{fill}" stroke-width="{t}" stroke-linecap="round"/></g>')


def umbrella(cx, top, w, colors=(PINK, WHITE), pole=NIGHT, pole_h=600, n=6):
    r = w / 2
    segs = []
    for i in range(n):
        a0, a1 = i / n, (i + 1) / n
        import math
        x0, y0 = cx - r * math.cos(math.pi * a0), top + r - r * math.sin(math.pi * a0)
        x1, y1 = cx - r * math.cos(math.pi * a1), top + r - r * math.sin(math.pi * a1)
        segs.append(f'<path d="M{cx} {top + r} L{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{colors[i % 2]}"/>')
    scal = "".join(
        f'<circle cx="{cx - r + (2 * r) * (i + 0.5) / n:.1f}" cy="{top + r}" r="{r / n / 2:.1f}" fill="{colors[i % 2]}"/>'
        for i in range(n))
    return (f'<g id="beach-umbrella"><rect x="{cx - 7}" y="{top}" width="14" height="{pole_h}" rx="7" fill="{pole}"/>'
            f'{"".join(segs)}{scal}</g>'), top + r


def palm(x, base, h, fill=NIGHT, lean=40):
    fr = []
    tx, ty = x + lean, base - h
    for ang, ln in [(-160, 1), (-125, 1.1), (-60, 1.1), (-20, 1), (-95, 0.8), (20, 0.8), (-200, 0.8)]:
        import math
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * h * 0.42 * ln, ty + math.sin(a) * h * 0.42 * ln + h * 0.12
        mx, my = tx + math.cos(a) * h * 0.2 * ln, ty + math.sin(a) * h * 0.2 * ln - h * 0.06
        fr.append(f'<path d="M{tx} {ty} Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" stroke="{fill}" stroke-width="{h * 0.06:.1f}" fill="none" stroke-linecap="round"/>')
    return (f'<g id="palm"><path d="M{x} {base} Q{x + lean * 0.2} {base - h * 0.5} {tx} {ty}" stroke="{fill}" '
            f'stroke-width="{h * 0.045:.1f}" fill="none" stroke-linecap="round"/>{"".join(fr)}</g>')


def lifeguard_tower(x, base, h, fill=WHITE, roof=PINK):
    w = h * 0.55
    return (f'<g id="lifeguard-tower"><path d="M{x} {base} L{x + w * 0.2} {base - h * 0.62} M{x + w} {base} L{x + w * 0.8} {base - h * 0.62} '
            f'M{x + w * 0.1} {base - h * 0.3} L{x + w * 0.9} {base - h * 0.3}" stroke="{fill}" stroke-width="{h * 0.035}" stroke-linecap="round"/>'
            f'<rect x="{x + w * 0.05}" y="{base - h * 0.82}" width="{w * 0.9}" height="{h * 0.22}" rx="6" fill="{fill}"/>'
            f'<path d="M{x - w * 0.05} {base - h * 0.82} L{x + w / 2} {base - h} L{x + w * 1.05} {base - h * 0.82} Z" fill="{roof}"/></g>')


def waterfall_cliff(x, top, w, h, rock=DEEP, water=WHITE):
    """Uvongo-style cliff with a waterfall dropping into the lagoon. Returns svg, lip (x,y)."""
    lip_x = x + w
    rockp = (f"M{x - 2000} {top} L{lip_x} {top} L{lip_x - w * 0.04} {top + h * 0.3} L{lip_x + w * 0.02} {top + h * 0.55} "
             f"L{lip_x - w * 0.06} {top + h} L{x - 2000} {top + h} Z")
    falls = "".join(f'<rect x="{lip_x - w * 0.02 + i * 26}" y="{top + 4}" width="14" height="{h}" rx="7" fill="{water}" opacity="{0.95 - i * 0.18}"/>' for i in range(4))
    return f'<g id="uvongo-falls"><path d="{rockp}" fill="{rock}"/>{falls}</g>', (lip_x - w * 0.12, top)


def mug(cx, top, w, fill=WHITE, coffee=NIGHT, steam=WHITE):
    h = w * 0.95
    return (f'<g id="coffee-mug">'
            + "".join(f'<path d="M{cx + dx} {top - 30} c-30 -40 30 -60 0 -110" stroke="{steam}" stroke-width="{w * 0.05}" fill="none" stroke-linecap="round" opacity="0.9"/>' for dx in (-w * 0.2, 0, w * 0.2))
            + f'<path d="M{cx + w / 2} {top + h * 0.2} c{w * 0.35} 0 {w * 0.35} {h * 0.5} 0 {h * 0.5}" stroke="{fill}" stroke-width="{w * 0.09}" fill="none"/>'
            f'<path d="M{cx - w / 2} {top} H{cx + w / 2} V{top + h * 0.8} Q{cx + w / 2} {top + h} {cx + w * 0.3} {top + h} H{cx - w * 0.3} Q{cx - w / 2} {top + h} {cx - w / 2} {top + h * 0.8} Z" fill="{fill}"/>'
            f'<ellipse cx="{cx}" cy="{top + 2}" rx="{w / 2 - 10}" ry="{w * 0.06}" fill="{coffee}"/></g>')


def egg(cx, cy, r, white=WHITE, yolk=YEL):
    d = (f"M{cx - r} {cy} C{cx - r * 1.1} {cy - r * 0.8} {cx - r * 0.2} {cy - r * 1.05} {cx + r * 0.2} {cy - r * 0.85} "
         f"C{cx + r * 0.9} {cy - r * 1.05} {cx + r * 1.2} {cy - r * 0.2} {cx + r * 0.95} {cy + r * 0.35} "
         f"C{cx + r * 0.8} {cy + r * 0.9} {cx - r * 0.1} {cy + r * 1.05} {cx - r * 0.55} {cy + r * 0.7} "
         f"C{cx - r * 0.95} {cy + r * 0.5} {cx - r * 0.95} {cy + r * 0.25} {cx - r} {cy} Z")
    return f'<g id="fried-egg"><path d="{d}" fill="{white}"/><circle cx="{cx + r * 0.05}" cy="{cy - r * 0.05}" r="{r * 0.38}" fill="{yolk}"/></g>'


def firework(cx, cy, r, fill=YEL, n=14):
    import math
    out = []
    for i in range(n):
        a = i * 2 * math.pi / n
        out.append(f'<line x1="{cx + math.cos(a) * r * 0.25:.1f}" y1="{cy + math.sin(a) * r * 0.25:.1f}" '
                   f'x2="{cx + math.cos(a) * r:.1f}" y2="{cy + math.sin(a) * r:.1f}" stroke="{fill}" stroke-width="{r * 0.06:.1f}" stroke-linecap="round"/>')
        out.append(f'<circle cx="{cx + math.cos(a) * r * 1.12:.1f}" cy="{cy + math.sin(a) * r * 1.12:.1f}" r="{r * 0.05:.1f}" fill="{fill}"/>')
    return f'<g class="firework">{"".join(out)}</g>'


def bunting(x1, y1, x2, y2, sag, n, colors=(YEL, PINK, WHITE, BLUE)):
    pts = []
    out = [f'<path d="M{x1} {y1} Q{(x1 + x2) / 2} {(y1 + y2) / 2 + sag * 2} {x2} {y2}" stroke="{NIGHT}" stroke-width="5" fill="none"/>']
    for i in range(n):
        t = (i + 0.5) / n
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * (x1 + x2) / 2 + t ** 2 * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * ((y1 + y2) / 2 + sag * 2) + t ** 2 * y2
        s = (x2 - x1) / n * 0.42
        out.append(f'<path d="M{x - s:.1f} {y:.1f} L{x + s:.1f} {y:.1f} L{x:.1f} {y + s * 1.9:.1f} Z" fill="{colors[i % len(colors)]}"/>')
    return f'<g id="bunting">{"".join(out)}</g>'


def bunting_point(x1, y1, x2, y2, sag, t):
    x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * (x1 + x2) / 2 + t ** 2 * x2
    y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * ((y1 + y2) / 2 + sag * 2) + t ** 2 * y2
    return x, y


def pool_ring(cx, cy, r, fill=PINK, stripe=WHITE):
    import math
    st = "".join(
        f'<path d="M{cx + math.cos(a) * r * 0.55:.1f} {cy + math.sin(a) * r * 0.55:.1f} L{cx + math.cos(a) * r:.1f} {cy + math.sin(a) * r:.1f}" '
        f'stroke="{stripe}" stroke-width="{r * 0.28:.1f}"/>' for a in [i * math.pi / 3 for i in range(6)])
    return (f'<g id="pool-ring"><circle cx="{cx}" cy="{cy}" r="{r * 0.775}" fill="none" stroke="{fill}" stroke-width="{r * 0.45}"/>'
            f'<g clip-path="none" opacity="1">{st}</g><circle cx="{cx}" cy="{cy}" r="{r * 0.55}" fill="none" stroke="{fill}" stroke-width="2"/></g>')


def cricket_bat(x, y, length, rot=35, fill=YEL2, grip=PINK):
    w = length * 0.16
    return (f'<g id="cricket-bat" transform="rotate({rot} {x} {y})">'
            f'<rect x="{x - w * 0.18}" y="{y}" width="{w * 0.36}" height="{length * 0.34}" rx="{w * 0.12}" fill="{grip}"/>'
            f'<rect x="{x - w / 2}" y="{y + length * 0.32}" width="{w}" height="{length * 0.68}" rx="{w * 0.3}" fill="{fill}"/></g>')


def thermometer(cx, top, h, fill=WHITE, liquid=PINK):
    w = h * 0.12
    return (f'<g id="thermometer"><rect x="{cx - w / 2}" y="{top}" width="{w}" height="{h}" rx="{w / 2}" fill="{fill}"/>'
            f'<circle cx="{cx}" cy="{top + h}" r="{w * 0.95}" fill="{fill}"/>'
            f'<rect x="{cx - w * 0.22}" y="{top + h * 0.18}" width="{w * 0.44}" height="{h * 0.85}" rx="{w * 0.22}" fill="{liquid}"/>'
            f'<circle cx="{cx}" cy="{top + h}" r="{w * 0.7}" fill="{liquid}"/></g>')


def cooler(x, y, w, fill=BLUE, lid=WHITE):
    h = w * 0.62
    return (f'<g id="cooler-box"><rect x="{x}" y="{y + h * 0.18}" width="{w}" height="{h * 0.82}" rx="{w * 0.06}" fill="{fill}"/>'
            f'<rect x="{x - w * 0.02}" y="{y}" width="{w * 1.04}" height="{h * 0.22}" rx="{w * 0.05}" fill="{lid}"/>'
            f'<rect x="{x + w * 0.35}" y="{y - h * 0.12}" width="{w * 0.3}" height="{h * 0.16}" rx="{h * 0.06}" fill="none" stroke="{lid}" stroke-width="{w * 0.025}"/></g>')


def slops(x, y, s=1, fill=PINK, strap=WHITE):
    o = []
    for dx, rot in ((0, -12), (s * 120, 10)):
        o.append(f'<g transform="rotate({rot} {x + dx + s * 45} {y + s * 110})"><ellipse cx="{x + dx + s * 45}" cy="{y + s * 110}" rx="{s * 45}" ry="{s * 110}" fill="{fill}"/>'
                 f'<path d="M{x + dx + s * 10} {y + s * 120} Q{x + dx + s * 45} {y + s * 20} {x + dx + s * 80} {y + s * 120}" stroke="{strap}" stroke-width="{s * 12}" fill="none" stroke-linecap="round"/></g>')
    return f'<g id="slops">{"".join(o)}</g>'


def grain_dots(w, h, fill, step=48, r=3, opacity=0.25):
    return (f'<pattern id="dots{abs(hash(fill)) % 999}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{fill}"/></pattern>'
            f'<rect width="{w}" height="{h}" fill="url(#dots{abs(hash(fill)) % 999})" opacity="{opacity}"/>')


def cliff_split(w, h, a, b, fill):
    """Jagged diagonal colour split (the brand's 'split along the cliff')."""
    import random
    rnd = random.Random(int(a * 7 + b))
    n = 9
    pts = [(a + (b - a) * i / n + rnd.uniform(-18, 18), h * i / n) for i in range(n + 1)]
    d = "M0 0 " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in pts) + f" L0 {h} Z"
    return f'<path id="cliff-split" d="{d}" fill="{fill}"/>'
