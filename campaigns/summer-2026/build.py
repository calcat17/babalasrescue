"""Babalas Rescue+ summer campaign 2026: "Hang in there, Mzansi".

Builds 30 artboards as Illustrator-editable SVG into ./svg.
Concept: the climber from the logo hangs off South African summer icons
(Table Mountain, rugby posts, braai tongs, beach umbrellas, festival bunting...).
"""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

OUT = pathlib.Path(__file__).parent / "svg"
ASSETS = []


def asset(slug, title, w, h, fmt):
    def deco(fn):
        ASSETS.append((slug, title, w, h, fmt, fn))
        return fn
    return deco


def stars(w, h, n=40, seed=1, fill=WHITE):
    import random
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(1.5, 4):.1f}" fill="{fill}" opacity="{r.uniform(.4, .9):.2f}"/>' for _ in range(n))


def sea(y, w, h, top=BLUE2, deep=DEEP):
    return waves(y, w, top, 14, 180, h=h) + waves(y + 50, w, deep, 12, 150, h=h)


def cape_scene(w, h, base, mw, mh, mx, climb_h, sky=BLUE, mountain=DEEP, climber=YEL, sun_xy=None, sea_on=True):
    out = [rect(0, 0, w, h, sky)]
    if sun_xy:
        out.append(sun(*sun_xy))
    m, top, R, L = table_mountain(mx, base, mw, mh, mountain)
    out += [m, tablecloth(L, R, top), hang(R - 6, top + 4, climb_h, climber, id_="climber-hanging")]
    if sea_on:
        out.append(sea(base, w, h))
    return "".join(out), top, R


# 01 ---------------------------------------------------------------------------------------
@asset("01-hero-table-mountain-feed", "Hero · Table Mountain · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a01(W, H):
    s, top, R = cape_scene(W, H, 860, 1260, 330, -90, 300, sun_xy=(190, 230, 80))
    return (s + logo(740, 70, 280) + text(70, 1010, ["Hang in there,", "Mzansi."], 100, WHITE)
            + text(70, 1196, "Summer’s long. Bounce back.", 40, YEL, 700)
            + pack("can", 800, 900, 300) + legal(70, 1305, 18, WHITE) + hashtag(1010, 1305, 22, WHITE, "end"))


# 02 ---------------------------------------------------------------------------------------
@asset("02-hero-table-mountain-story", "Hero · Table Mountain · Story 9:16", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a02(W, H):
    s, top, R = cape_scene(W, H, 1180, 1300, 400, -110, 360, sun_xy=(860, 560, 90))
    return (s + text(80, 330, ["Hang in there,", "Mzansi."], 116, WHITE)
            + text(80, 545, "Summer’s long. Bounce back.", 44, YEL, 700)
            + pack("can", 640, 1300, 430) + wordmark(80, 1440, 420) + legal(80, 1850, 20, WHITE))


# 03 ---------------------------------------------------------------------------------------
@asset("03-billboard-cape-town", "Billboard · Cape Town · 3:1", 3000, 1000, "Roadside billboard 3:1 (scale to site)")
def a03(W, H):
    s, top, R = cape_scene(W, H, 860, 2000, 520, -120, 440, sun_xy=(1440, 150, 70))
    return (s + text(1640, 300, "CAPE TOWN:", 64, YEL, 800, ls=0.08)
            + text(1640, 430, ["Big nights.", "Bigger mornings."], 112, WHITE)
            + wordmark(1640, 680, 430) + pack("can", 2470, 330, 560) + legal(2960, 975, 22, WHITE, "end"))


# 04 ---------------------------------------------------------------------------------------
@asset("04-braai-feed", "Braai · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a04(W, H):
    cx, top = 470, 900
    return (rect(0, 0, W, H, NIGHT) + stars(W, 820, 50) + logo(790, 60, 230)
            + text(70, 290, ["The braai ended", "at 2am."], 92, WHITE)
            + text(70, 510, ["The rescue", "starts now."], 92, YEL)
            + braai(cx, top, 460, BLUE, WHITE) + wors(cx - 90, top - 26, 34) + wors(cx + 60, top - 24, 30)
            + tongs(cx + 150, top - 20, 880, 680) + hang(880, 676, 270, YEL)
            + pack("can", 50, 1000, 270) + legal(1010, 1325, 18, WHITE, "end"))


# 05 ---------------------------------------------------------------------------------------
@asset("05-braai-story", "Braai · Tjops Wors Rescue+ · Story", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a05(W, H):
    cx, top = 520, 1320
    return (rect(0, 0, W, H, YEL) + wordmark(80, 130, 300, BLUE)
            + text(80, 520, ["Tjops.", "Wors."], 170, NIGHT) + text(80, 860, "Rescue+", 170, BLUE)
            + pack("can", 720, 360, 360)
            + braai(cx, top, 540, NIGHT, WHITE) + wors(cx - 100, top - 28, 40) + wors(cx + 80, top - 26, 34)
            + tongs(cx + 170, top - 24, 880, 1010, NIGHT) + hang(880, 1006, 290, BLUE)
            + text(80, 1000, "Sunday sorted.", 54, NIGHT, 700) + legal(80, 1870, 20))


# 06 ---------------------------------------------------------------------------------------
@asset("06-rugby-posts-feed", "Rugby · Final whistle · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a06(W, H):
    stripes = "".join(rect(0, 1150 + i * 50, W, 25, DEEP) for i in range(4))
    return (rect(0, 0, W, H, BLUE) + rect(0, 1150, W, 200, "#0d5a87") + stripes
            + text(70, 230, ["Hang on till the", "final whistle."], 96, WHITE)
            + rugby_ball(900, 470, 70, YEL)
            + rugby_posts(540, 1150, 760, 440, 640) + hang(600, 760, 300, YEL)
            + pack("can", 50, 880, 270) + logo(790, 1185, 230) + legal(50, 1325, 18, WHITE))


# 07 ---------------------------------------------------------------------------------------
@asset("07-rugby-ball-square", "Rugby · Post-match, pre-Monday · Square", 1080, 1080, "Instagram / Facebook square 1080×1080")
def a07(W, H):
    cx, cy, rx, rot = 540, 340, 300, -20
    ry = rx * 0.6
    gx, gy = cx - ry * math.sin(math.radians(rot)), cy + ry * math.cos(math.radians(rot))
    return (rect(0, 0, W, H, YEL) + rugby_ball(cx, cy, rx, BLUE, WHITE, rot) + hang(gx - 4, gy - 8, 300, NIGHT)
            + text(70, 930, ["Post-match.", "Pre-Monday."], 96, NIGHT)
            + wordmark(780, 860, 230, BLUE) + legal(70, 1050, 17))


# 08 ---------------------------------------------------------------------------------------
@asset("08-uvongo-falls-feed", "Uvongo · Falls · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a08(W, H):
    rock_top, lip = 560, 520
    rockp = (f"M-10 {rock_top} L{lip} {rock_top} L{lip - 18} {rock_top + 160} L{lip + 14} {rock_top + 300} "
             f"L{lip - 30} {rock_top + 520} L-10 {rock_top + 520} Z")
    falls = "".join(rect(250 + i * 30, rock_top - 2, 16, 470, WHITE, 8, f'opacity="{0.95 - i * 0.17:.2f}"') for i in range(4))
    notch = f'<path d="M230 {rock_top} Q290 {rock_top + 26} 360 {rock_top} Z" fill="{BLUE}"/>'
    splash = "".join(f'<circle cx="{270 + i * 22}" cy="{1010 + (i % 2) * 12}" r="{14 - i}" fill="{WHITE}"/>' for i in range(6))
    return (rect(0, 0, W, H, BLUE) + sun(920, 470, 60)
            + f'<path id="uvongo-cliff" d="{rockp}" fill="{DEEP}"/>' + notch + falls
            + waves(1000, W, BLUE2, 12, 160, h=400) + splash + waves(1060, W, "#5cc0f2", 10, 140, h=400)
            + hang(lip - 6, rock_top + 2, 300, YEL)
            + text(70, 200, "Uvongo by day.", 84, WHITE) + text(70, 290, "Babalas by morning.", 84, YEL)
            + pack("can", 790, 1000, 270) + wordmark(60, 1150, 260) + legal(60, 1325, 18, WHITE))


# 09 ---------------------------------------------------------------------------------------
@asset("09-margate-umbrella-feed", "Margate · Umbrella · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a09(W, H):
    u, rim = umbrella(700, 430, 560, (PINK, WHITE), NIGHT, 700)
    return (rect(0, 0, W, H, BLUE) + sun(930, 140, 60) + rect(0, 760, W, 160, BLUE2) + waves(780, W, WHITE, 8, 120, h=20)
            + rect(0, 900, W, 450, YEL2) + lifeguard_tower(110, 900, 250) + palm(990, 900, 300, DEEP, -40)
            + u + hang(438, rim + 18, 280, NIGHT)
            + text(70, 170, "Margate.", 92, YEL) + text(70, 262, ["Mid-December.", "Mid-babalas."], 80, WHITE)
            + pack("can", 810, 1010, 250) + slops(470, 1110, 0.7) + wordmark(60, 1150, 250, BLUE) + legal(60, 1325, 18))


# 10 ---------------------------------------------------------------------------------------
@asset("10-south-coast-packing-list-story", "South Coast packing list · Story", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a10(W, H):
    items = ["Slops", "Sunscreen (SPF 50)", "Cooler box", "Beach cricket bat", "Babalas Rescue+"]
    out = [rect(0, 0, W, H, YEL), text(80, 330, ["South Coast", "packing list"], 110, NIGHT)]
    y = 620
    for i, it in enumerate(items):
        last = i == len(items) - 1
        out.append(rect(90, y - 60, 76, 76, BLUE if last else WHITE, 14, f'stroke="{NIGHT}" stroke-width="5"'))
        if last:
            out.append(f'<path d="M106 {y - 24} L124 {y - 4} L154 {y - 46}" stroke="{YEL}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(text(200, y, it, 64, BLUE if last else NIGHT, 800 if last else 600, font=DISPLAY if last else BODY, ls=0 if not last else -0.01))
        y += 120
    out.append(hang(128, y - 120 + 16, 220, BLUE))
    out += [slops(260, 1300, 0.9), cooler(90, 1500, 230, BLUE, WHITE), pack("box", 600, 1250, 420),
            wordmark(80, 1720, 270, BLUE), legal(1000, 1880, 20, NIGHT, "end")]
    return "".join(out)


# 11 ---------------------------------------------------------------------------------------
@asset("11-breakfast-run-feed", "Breakfast run · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a11(W, H):
    return (rect(0, 0, W, H, YEL) + text(70, 210, ["Breakfast run?", "Bring backup."], 100, NIGHT)
            + egg(880, 500, 110) + mug(380, 640, 400, WHITE, NIGHT, WHITE)
            + hang(186, 642, 300, BLUE, flip=True)
            + pack("can", 780, 760, 320) + wordmark(70, 1150, 250, BLUE) + legal(1010, 1325, 18, NIGHT, "end"))


# 12 ---------------------------------------------------------------------------------------
@asset("12-morning-after-menu-story", "Morning-after menu · Story", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a12(W, H):
    toast = (f'<g id="toast"><path d="M170 {860} q-60 -10 -60 -70 q0 -70 80 -70 h120 q80 0 80 70 q0 60 -60 70 v120 h-160 Z" fill="{YEL2}"/>'
             f'<path d="M190 {860} q-40 -8 -40 -52 q0 -45 55 -45 h90 q55 0 55 45 q0 44 -40 52 v95 h-120 Z" fill="{SUN}"/></g>')
    return (rect(0, 0, W, H, BLUE) + text(80, 290, ["The morning-after", "menu"], 92, WHITE)
            + egg(240, 560, 120) + text(430, 600, "Eggs.", 130, WHITE)
            + toast + text(430, 900, "Toast.", 130, WHITE)
            + mug(240, 1080, 210, WHITE, NIGHT, WHITE) + text(430, 1220, "Coffee.", 130, WHITE)
            + pack("can", 150, 1330, 250) + text(430, 1520, "Rescue+", 130, YEL)
            + hang(800, 1534, 190, YEL)
            + wordmark(80, 1690, 300) + legal(1000, 1870, 20, WHITE, "end"))


# 13 ---------------------------------------------------------------------------------------
@asset("13-new-years-day-feed", "1 January · Feed 4:5", 1080, 1350, "Instagram / Facebook feed 1080×1350")
def a13(W, H):
    cal = (f'<g id="calendar-page">{rect(300, 260, 480, 500, WHITE, 28)}<path d="M300 288 a28 28 0 0 1 28 -28 h424 a28 28 0 0 1 28 28 v92 h-480 Z" fill="{PINK}"/>'
           f'{text(540, 352, "JANUARY", 58, WHITE, 800, "middle", ls=0.12)}{text(540, 690, "1", 330, NIGHT, 800, "middle")}</g>')
    return (rect(0, 0, W, H, NIGHT) + stars(W, H, 60, 3) + firework(150, 230, 110, YEL) + firework(930, 200, 90, PINK)
            + firework(940, 620, 70, BLUE) + firework(120, 700, 60, PINK)
            + cal + hang(690, 758, 280, BLUE) + pack("sachet", 160, 380, 380)
            + text(70, 1150, "New year. Same jol.", 54, WHITE, 700) + text(70, 1260, "Hang in there.", 110, YEL)
            + logo(800, 60, 220) + legal(1010, 1325, 18, WHITE, "end"))


# 14 ---------------------------------------------------------------------------------------
@asset("14-festival-season-story", "Festival season · Story", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a14(W, H):
    x1, y1, x2, y2, sag = -20, 360, 1100, 330, 80
    gx, gy = bunting_point(x1, y1, x2, y2, sag, 0.7)
    tents = "".join(f'<path d="M{x} 1720 L{x + 160} {1450 + (i % 2) * 40} L{x + 320} 1720 Z" fill="{c}"/>'
                    f'<path d="M{x + 160} {1450 + (i % 2) * 40} L{x + 130} 1720 L{x + 190} 1720 Z" fill="{NIGHT}" opacity=".35"/>'
                    for i, (x, c) in enumerate([(-80, WHITE), (180, PINK), (420, YEL2)]))
    return (rect(0, 0, W, H, BLUE) + wordmark(390, 110, 300) + bunting(x1, y1, x2, y2, sag, 11)
            + hang(gx, gy + 4, 330, YEL)
            + text(80, 980, ["Festival", "season."], 160, WHITE) + text(80, 1260, "Pack the rescue.", 74, YEL)
            + rect(0, 1720, W, 200, DEEP) + tents + pack("box", 620, 1330, 380) + legal(80, 1870, 20, WHITE))


# 15 ---------------------------------------------------------------------------------------
@asset("15-pool-day-square", "Pool day · Square", 1080, 1080, "Instagram / Facebook square 1080×1080")
def a15(W, H):
    tiles = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{BLUE2}" stroke-width="2" opacity=".6"/>' for x in range(0, W, 90)) + \
            "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{BLUE2}" stroke-width="2" opacity=".6"/>' for y in range(0, H, 90))
    ripples = "".join(f'<ellipse cx="800" cy="380" rx="{240 + i * 50}" ry="{70 + i * 16}" fill="none" stroke="{WHITE}" stroke-width="4" opacity="{.5 - i * .15:.2f}"/>' for i in range(3))
    return (rect(0, 0, W, H, BLUE) + tiles + ripples + pool_ring(800, 360, 200, PINK, WHITE) + hang(800, 556, 280, YEL)
            + text(70, 160, ["Pool day.", "Pool night."], 80, WHITE) + text(70, 320, "Pool rescue.", 80, YEL)
            + pack("can", 70, 720, 270) + wordmark(800, 930, 220) + legal(70, 1050, 17, WHITE))


# 16 ---------------------------------------------------------------------------------------
@asset("16-beach-cricket-square", "Beach cricket · Square", 1080, 1080, "Instagram / Facebook square 1080×1080")
def a16(W, H):
    stumps = "".join(rect(x - 9, 480, 18, 420, WHITE, 9) for x in (720, 780, 840))
    bails = rect(705, 466, 150, 14, PINK, 7)
    return (rect(0, 0, W, H, BLUE) + rect(0, 560, W, 110, BLUE2) + waves(570, W, WHITE, 8, 120, h=14)
            + rect(0, 650, W, 430, YEL2) + stumps + bails + hang(800, 478, 280, NIGHT)
            + cricket_bat(600, 610, 340, 25, YEL, PINK) + f'<circle cx="960" cy="780" r="28" fill="{PINK}"/>'
            + text(70, 190, ["One hand,", "one bounce."], 100, WHITE) + text(70, 400, "Bounce back.", 100, YEL)
            + pack("can", 70, 720, 260) + wordmark(800, 950, 220, BLUE) + legal(70, 1050, 17))


# 17 ---------------------------------------------------------------------------------------
@asset("17-heat-rehydrate-story", "Hot day, long night · Story", 1080, 1920, "Instagram / TikTok story 1080×1920")
def a17(W, H):
    gx, gy = 840, 330 + 150 * 1.55
    return (rect(0, 0, W, H, YEL) + sun(840, 330, 150, WHITE, True, BLUE) + thermometer(160, 250, 360, WHITE, PINK)
            + text(260, 430, "34°C", 120, NIGHT) + hang(gx, gy, 330, BLUE)
            + text(80, 1000, ["Hot day.", "Long night."], 130, NIGHT) + text(80, 1260, "Rehydrate.", 130, PINK)
            + pill(80, 1330, "ELECTROLYTES", 26, BLUE, NIGHT) + pill(380, 1330, "B-VITAMINS", 26, BLUE, NIGHT)
            + pill(640, 1330, "ANTIOXIDANTS", 26, BLUE, NIGHT)
            + pack("can", 650, 1450, 360) + wordmark(80, 1520, 340, BLUE) + legal(80, 1870, 20))


# 18-22 carousel ---------------------------------------------------------------------------
GUIDE = [
    ("01", ["Before the jol"], "Load up before the big night out so you get the most out of your night.", "can"),
    ("02", ["Before bed"], "Give your body what it needs to recover while you sleep.", "sachet"),
    ("03", ["The morning after"], "Start your day with the right stuff and jump back into action.", "can"),
    ("04", ["Know your limits"], "Pace yourself, drink water between rounds and never drink and drive. Designated drivers are the real heroes.", None),
]


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    return lines + [cur]


@asset("18-survival-guide-1-cover", "Summer Survival Guide 1/5 · Carousel", 1080, 1080, "Instagram carousel 1080×1080")
def a18(W, H):
    return (rect(0, 0, W, H, BLUE) + icon(-60, 40, 1000, YEL) + pill(560, 90, "1 / 5", 26, NIGHT, WHITE)
            + text(560, 330, ["The", "Summer", "Survival", "Guide"], 112, WHITE)
            + pill(560, 770, "SWIPE →", 28, YEL, NIGHT) + wordmark(560, 900, 260) + legal(1010, 1050, 16, WHITE, "end"))


def guide(i):
    num, title, body, p = GUIDE[i]
    def fn(W, H):
        bg, fg, acc = (YEL, NIGHT, BLUE) if i % 2 == 0 else (BLUE, WHITE, YEL)
        out = [rect(0, 0, W, H, bg), pill(70, 70, f"SUMMER SURVIVAL GUIDE · {i + 2} / 5", 22, NIGHT, WHITE),
               wordmark(800, 60, 210, acc if bg == YEL else YEL),
               text(70, 440, num, 260, acc), text(70, 580, title, 84, fg)]
        out.append(text(70, 660, wrap(body, 30 if p else 40), 36, fg, 600, font=BODY, lh=1.4, ls=0))
        out.append(rect(70, 900, 560, 14, fg, 7))
        out.append(hang(600, 905, 150, acc if bg == BLUE else BLUE))
        if p:
            out.append(pack(p, 760 if p == "can" else 880, 600 if p == "can" else 520, 380 if p == "can" else 470))
        else:
            out.append(plus_badge(880, 420, 120, BLUE, YEL))
        out.append(legal(70, 1050, 16, fg))
        return "".join(out)
    return fn


for _i, _slug in enumerate(["19-survival-guide-2-before-the-jol", "20-survival-guide-3-before-bed",
                            "21-survival-guide-4-morning-after", "22-survival-guide-5-know-your-limits"]):
    asset(_slug, f"Summer Survival Guide {_i + 2}/5 · Carousel", 1080, 1080, "Instagram carousel 1080×1080")(guide(_i))


# 23 ---------------------------------------------------------------------------------------
@asset("23-link-ad-stock-up", "Stock up for summer · Link ad", 1200, 628, "Facebook / Google display 1200×628")
def a23(W, H):
    m, top, R, L = table_mountain(-40, 628, 720, 300, DEEP)
    return (rect(0, 0, W, H, YEL) + cliff_split(W, H, 620, 560, BLUE) + sun(470, 130, 40)
            + m + tablecloth(L, R, top) + hang(R - 4, top + 3, 210, YEL)
            + wordmark(40, 36, 210) + text(690, 150, ["Stock up", "for summer."], 74, NIGHT)
            + pack("4pack", 690, 270, 270) + legal(1170, 610, 14, NIGHT, "end"))


# 24 ---------------------------------------------------------------------------------------
@asset("24-retail-poster-a3", "In-store poster · A3", 1190, 1684, "A3 portrait poster (297×420 mm), add 3 mm bleed")
def a24(W, H):
    m, top, R, L = table_mountain(-80, 1050, 1350, 420, DEEP)
    return (rect(0, 0, W, H, YEL) + f'<circle cx="1010" cy="520" r="70" fill="{PINK}"/>'
            + m + tablecloth(L, R, top) + hang(R - 6, top + 4, 360, BLUE)
            + sea(1050, W, H) + text(80, 220, ["Hang in there,", "Mzansi."], 128, NIGHT)
            + text(80, 1230, ["Summer survival,", "now in store."], 62, WHITE, 700)
            + pack("4pack", 650, 1150, 400) + wordmark(80, 1400, 400) + legal(80, 1655, 20, WHITE))


# 25 ---------------------------------------------------------------------------------------
@asset("25-shelf-wobbler", "Shelf wobbler · Ø100 mm", 1000, 1000, "Round shelf wobbler, die-cut on pink dashed line")
def a25(W, H):
    clip = '<clipPath id="wob"><circle cx="500" cy="500" r="480"/></clipPath>'
    return (f'<defs>{clip}</defs><g clip-path="url(#wob)">{rect(0, 0, W, H, BLUE)}{icon(20, 140, 720, YEL)}</g>'
            + text(580, 330, ["Hang", "in", "there!"], 110, YEL) + wordmark(370, 760, 280)
            + f'<circle id="cutline" cx="500" cy="500" r="480" fill="none" stroke="{PINK}" stroke-width="3" stroke-dasharray="14 10"/>')


# 26 ---------------------------------------------------------------------------------------
@asset("26-sticker-sheet", "Sticker sheet · 8 die-cuts", 1600, 1600, "Kiss-cut sticker sheet, die-cut on pink dashed lines")
def a26(W, H):
    def st(inner, outline):
        return (f'<g class="sticker"><g fill="{WHITE}" stroke="{WHITE}" stroke-width="40" stroke-linejoin="round">{outline}</g>'
                f'<g fill="none" stroke="{PINK}" stroke-width="3" stroke-dasharray="12 9">{outline}</g>{inner}</g>')
    out = [rect(0, 0, W, H, SKY), text(80, 120, "Hang in there, Mzansi · sticker sheet", 44, NIGHT, 800)]
    c1 = '<circle cx="330" cy="420" r="190"/>'
    out.append(st(f'<circle cx="330" cy="420" r="190" fill="{BLUE}"/>' + icon(205, 270, 280, YEL), c1))
    c2 = '<circle cx="800" cy="380" r="140"/>'
    out.append(st(plus_badge(800, 380, 140, YEL, BLUE), c2))
    c3 = '<rect x="1000" y="270" width="540" height="200" rx="100"/>'
    out.append(st(rect(1000, 270, 540, 200, PINK, 100) + text(1270, 392, "JOL RESPONSIBLY", 46, WHITE, 800, "middle", ls=0.04), c3))
    m, top, R, L = table_mountain(170, 1000, 420, 150, DEEP, peaks=True)
    c4 = '<circle cx="380" cy="930" r="220"/>'
    out.append(st(f'<circle cx="380" cy="930" r="220" fill="{YEL}"/>' + m + tablecloth(L, R, top) + hang(R - 3, top + 2, 120, BLUE)
                  + text(380, 1080, "CAPE TOWN", 40, NIGHT, 800, "middle", ls=0.1), c4))
    c5 = '<rect x="700" y="700" width="380" height="420" rx="30"/>'
    out.append(st(rect(700, 700, 380, 420, BLUE, 30) + text(890, 800, "UVONGO", 64, YEL, 800, "middle", ls=0.06)
                  + f'<g clip-path="url(#uvclip)"><clipPath id="uvclip"><rect x="700" y="700" width="380" height="420" rx="30"/></clipPath>' + waves(950, 380, BLUE2, 10, 90, x0=700, h=150) + "</g>" + text(890, 900, "&amp; MARGATE", 34, WHITE, 800, "middle", ls=0.1)
                  + text(890, 1080, "SOUTH COAST", 26, NIGHT, 800, "middle", ls=0.14), c5))
    c6 = '<rect x="1180" y="620" width="340" height="560" rx="40"/>'
    out.append(st(rect(1180, 620, 340, 560, YEL, 40) + rugby_ball(1350, 760, 100, BLUE, WHITE, -25)
                  + hang(1350, 822, 150, NIGHT) + text(1350, 1080, "80 MIN", 56, NIGHT, 800, "middle")
                  + text(1350, 1130, "+ RESCUE", 34, BLUE, 800, "middle"), c6))
    c7 = '<rect x="140" y="1270" width="760" height="230" rx="40"/>'
    out.append(st(rect(140, 1270, 760, 230, BLUE, 40) + wordmark(200, 1310, 420) + plus_badge(800, 1385, 60, YEL, BLUE), c7))
    c8 = '<circle cx="1260" cy="1380" r="150"/>'
    out.append(st(f'<circle cx="1260" cy="1380" r="150" fill="{NIGHT}"/>' + text(1260, 1365, "HANG", 64, YEL, 800, "middle")
                  + text(1260, 1430, "TIGHT", 64, WHITE, 800, "middle"), c8))
    return "".join(out)


# 27 ---------------------------------------------------------------------------------------
@asset("27-beach-towel", "Beach towel · 70×140 cm", 1000, 2000, "Beach towel 70×140 cm (print at 100 dpi full size)")
def a27(W, H):
    m, top, R, L = table_mountain(-60, 1720, 1120, 330, DEEP)
    band = lambda y: rect(0, y, W, 120, YEL) + rect(0, y + 140, W, 24, YEL)
    return (rect(0, 0, W, H, BLUE) + band(0) + hang(520, 120, 760, YEL)
            + f'<g transform="rotate(-90 930 1000)">{text(930, 1020, "HANG IN THERE, MZANSI", 70, WHITE, 800, "middle", ls=0.12)}</g>'
            + m + tablecloth(L, R, top) + sea(1720, W, 400) + rect(0, 1836, W, 24, YEL) + rect(0, 1880, W, 120, YEL)
            + wordmark(100, 1070, 520))


# 28 ---------------------------------------------------------------------------------------
@asset("28-cooler-box-wrap", "Cooler box wrap · panel", 2000, 1000, "Cooler box side panel wrap (2:1)")
def a28(W, H):
    climbers = "".join(hang(x, 88, 120, YEL if i % 2 else WHITE, flip=bool(i % 2)) for i, x in enumerate(range(150, 1300, 220)))
    return (rect(0, 0, W, H, YEL) + rect(0, 0, W, 90, BLUE) + climbers
            + text(100, 420, ["Ice. Wors.", "Rescue+."], 170, NIGHT) + wordmark(100, 640, 420, BLUE)
            + pack("4pack", 1330, 240, 520) + rect(0, 900, W, 100, BLUE)
            + hashtag(100, 965, 44, WHITE) + legal(1900, 965, 26, WHITE, "end"))


# 29 ---------------------------------------------------------------------------------------
@asset("29-postcard-greetings", "Postcard · Greetings from the morning after", 1800, 1200, "Postcard A5 landscape (148×210 mm ratio)")
def a29(W, H):
    pw, ph, py = 520, 740, 330
    defs_ = f'<defs><clipPath id="panel"><rect x="0" y="0" width="{pw}" height="{ph}" rx="36"/></clipPath></defs>'

    def panel(x, inner, label):
        return (f'<g transform="translate({x} {py})"><g clip-path="url(#panel)">{inner}</g>'
                f'{pill(pw / 2, ph - 90, label, 30, WHITE, NIGHT, anchor="middle")}</g>')
    m, top, R, L = table_mountain(-120, 560, 760, 250, DEEP)
    cape = rect(0, 0, pw, ph, BLUE) + sun(110, 120, 46) + m + tablecloth(L, R, top) + hang(R - 4, top + 3, 220, YEL) + sea(560, pw, 300)
    rockp = f"M-10 300 L330 300 L314 420 L340 560 L300 760 L-10 760 Z"
    uv = (rect(0, 0, pw, ph, BLUE) + f'<path d="{rockp}" fill="{DEEP}"/>' + "".join(rect(120 + i * 26, 298, 14, 360, WHITE, 7, f'opacity="{.9 - i * .2:.1f}"') for i in range(4))
          + waves(600, pw, BLUE2, 10, 120, h=200) + hang(326, 302, 230, YEL))
    u, rim = umbrella(330, 260, 380, (PINK, WHITE), NIGHT, 500)
    mg = rect(0, 0, pw, ph, BLUE) + rect(0, 470, pw, 90, BLUE2) + rect(0, 550, pw, 200, YEL2) + u + hang(162, rim + 14, 220, NIGHT) + sun(440, 90, 40)
    return (defs_ + rect(0, 0, W, H, YEL) + text(90, 150, "Greetings from", 70, NIGHT, 700)
            + text(90, 270, "the morning after.", 120, BLUE) + wordmark(1430, 80, 300, BLUE)
            + panel(90, cape, "CAPE TOWN") + panel(640, uv, "UVONGO") + panel(1190, mg, "MARGATE")
            + legal(90, 1150, 22) + hashtag(1710, 1150, 28, NIGHT, "end"))


# 30 ---------------------------------------------------------------------------------------
@asset("30-email-header", "Email header · Summer rescue plan", 1200, 400, "Email / newsletter header 1200×400")
def a30(W, H):
    m, top, R, L = table_mountain(620, 400, 640, 220, DEEP)
    return (rect(0, 0, W, H, BLUE) + sun(740, 90, 38) + m + tablecloth(L, R, top) + hang(R - 4, top + 3, 190, YEL)
            + text(60, 150, ["Your summer", "rescue plan."], 72, WHITE)
            + pill(60, 270, "SHOP THE RESCUE →", 24, YEL, NIGHT) + wordmark(990, 26, 180))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    for slug, title, w, h, fmt, fn in ASSETS:
        (OUT / f"{slug}.svg").write_text(svg(w, h, fn(w, h), f"Babalas Rescue+ · {title}"))
    import json
    (OUT.parent / "manifest.json").write_text(json.dumps(
        [{"file": f"svg/{s}.svg", "title": t, "width": w, "height": h, "format": f} for s, t, w, h, f, _ in ASSETS], indent=1))
    print(len(ASSETS), "artboards")
