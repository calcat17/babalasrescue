"""Build Babalas Rescue+ logo colourways from the supplied vector logo PDF (source-assets/babalas-logo.pdf).
Run: pdftocairo -svg source-assets/babalas-logo.pdf brand/logo/_raw.svg && python3 scripts/build_logos.py
"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent / "brand" / "logo"
raw = (root / "_raw.svg").read_text()
paths = re.findall(r'<path fill-rule="nonzero" fill="rgb\(96[^"]*"[^>]*d="([^"]+)"', raw)
print(len(paths), "foreground paths")

def bbox(d):
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)

icon, word = [], []
for d in paths:
    x0, y0, x1, y1 = bbox(d)
    (icon if x1 < 172 else word).append(d)
print(len(icon), "icon paths,", len(word), "wordmark paths")
ib = [bbox(d) for d in icon]
IX0, IY0 = min(b[0] for b in ib), min(b[1] for b in ib)
IX1, IY1 = max(b[2] for b in ib), max(b[3] for b in ib)

BLUE, YELLOW, PINK, WHITE, INK = "#2CACEF", "#FDEA12", "#F6009D", "#FFFFFF", "#0B1F2E"
W, H = 476.44, 240.09

def svg(ds, fg, bg=None, vb=(0, 0, W, H), title="Babalas Rescue+"):
    x, y, w, h = vb
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    body = "".join(f'<path d="{d}"/>' for d in ds)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{rect}<g fill="{fg}" fill-rule="nonzero">{body}</g></svg>')

# Full lockup colourways (artwork bounds = original artboard; keep clear space built in)
tight = (IX0 - 4, 28, W - (IX0 - 4) - 6, 188 - 28 + 2)
variants = {
    "babalas-logo-yellow-on-blue": (paths, YELLOW, BLUE),
    "babalas-logo-blue-on-yellow": (paths, BLUE, YELLOW),
    "babalas-logo-yellow": (paths, YELLOW, None),
    "babalas-logo-blue": (paths, BLUE, None),
    "babalas-logo-white": (paths, WHITE, None),
    "babalas-logo-black": (paths, INK, None),
}
for name, (ds, fg, bg) in variants.items():
    (root / f"{name}.svg").write_text(svg(ds, fg, bg))

# Climber icon only
pad = 6
ivb = (IX0 - pad, IY0 - pad, IX1 - IX0 + 2 * pad, IY1 - IY0 + 2 * pad)
for name, fg, bg in [("babalas-icon-yellow", YELLOW, None), ("babalas-icon-blue", BLUE, None),
                     ("babalas-icon-white", WHITE, None), ("babalas-icon-yellow-on-blue", YELLOW, BLUE)]:
    (root / f"{name}.svg").write_text(svg(icon, fg, bg, ivb, "Babalas Rescue+ climber icon"))

# Wordmark only (no climber)
wb = [bbox(d) for d in word]
WX0, WY0 = min(b[0] for b in wb), min(b[1] for b in wb)
WX1, WY1 = max(b[2] for b in wb), max(b[3] for b in wb)
wvb = (WX0 - pad, WY0 - pad, WX1 - WX0 + 2 * pad, WY1 - WY0 + 2 * pad)
for name, fg in [("babalas-wordmark-yellow", YELLOW), ("babalas-wordmark-blue", BLUE), ("babalas-wordmark-white", WHITE)]:
    (root / f"{name}.svg").write_text(svg(word, fg, None, wvb, "babalas rescue+ wordmark"))
print("icon bbox", IX0, IY0, IX1, IY1, "| word bbox", WX0, WY0, WX1, WY1)
