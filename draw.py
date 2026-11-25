#!/usr/bin/env python3
"""Render the news-image entry for Wednesday 25 November 2026.

Fresh code written for news-image-20261125. Draws a 1024x1024 newspaper
front page with PIL and Google Sans, from the story list below. Every story
was researched on 25 Nov 2026 and first reported that day (UTC).
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
GREY = (90, 88, 82)
RULE = (26, 26, 26)
SEA = (214, 226, 232)
LAND = (232, 220, 192)
LAND_LINE = (178, 164, 128)

REGION_COLORS = {
    "Europe": (31, 78, 121),
    "Asia": (178, 34, 34),
    "Middle East": (146, 94, 20),
    "Africa": (32, 120, 72),
    "Americas": (84, 48, 130),
    "Oceania": (14, 120, 120),
    "Global": (70, 70, 70),
}

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

F_BOLD = lambda s: font("GoogleSans-Bold.ttf", s)
F_SEMI = lambda s: font("GoogleSans-SemiBold.ttf", s)
F_MED = lambda s: font("GoogleSans-Medium.ttf", s)
F_REG = lambda s: font("GoogleSans-Regular.ttf", s)

DATE_STR = "Wednesday 25 November 2026"

# ---- stories: (num, region, tag, headline, deck, source) ----
LEADS = [
    (1, "Middle East", "RAS TANURA · RIYADH — WAR",
     "Houthi drones strike Saudi oil refinery and Riyadh tower",
     "Saudi defences down four drones over Ras Tanura; 11 people were hurt in a tower strike a day earlier.",
     "REUTERS"),
    (2, "Asia", "JIUQUAN, CHINA — SPACE",
     "China launches its first foreign astronaut into orbit",
     "Shenzhou-24 lifts off at 00:18 UTC and docks at Tiangong; Pakistani pilot Zeeshan Ali, 40, is aboard.",
     "REUTERS"),
    (3, "Global", "TOKYO · SEOUL · TAIPEI — MARKETS",
     "Asian stocks tumble as tariff threats return",
     "Korea falls 5.3%, Taiwan 5.1% and the Nikkei 2.9% as the US plans new duties on 16 trading partners.",
     "REUTERS"),
]

MEDIUM = [
    (4, "Asia", "SHANGHAI — POLITICS",
     "China investigates a fourth Politburo member for graft",
     "Shanghai chief Chen Jining probed in a graft case.",
     "REUTERS"),
    (5, "Global", "DEEP SPACE — SCIENCE",
     "Europe's Hera reaches the asteroid NASA struck",
     "First close-up images of Dimorphos due today.",
     "BBC"),
    (6, "Americas", "IOWA, USA — SAFETY",
     "Army to blow up five tons of unstable explosives",
     "Court-approved blast to destroy degraded lead azide.",
     "AP"),
    (7, "Middle East", "STRAIT OF HORMUZ — ENERGY",
     "Two tankers hit mines in the Strait of Hormuz",
     "Iran says the tankers struck naval mines; Brent near $91.",
     "REUTERS"),
    (8, "Europe", "MOSCOW — WAR",
     "Russia's own figures show almost 500,000 war dead",
     "Leaked data reveal the invasion's toll on Russia.",
     "BBC"),
    (9, "Oceania", "CANBERRA — DIPLOMACY",
     "Solomon Islands picks Australia as security partner",
     "Treaty names Australia its primary security partner.",
     "AP"),
    (10, "Europe", "MADRID — POLITICS",
     "Spain's election turns on a housing crisis",
     "Sanchez and Feijoo clash before Sunday's vote.",
     "REUTERS"),
    (11, "Americas", "WASHINGTON — POLITICS",
     "Democrats clinch 259 House seats, most since 1990",
     "Final count confirms the party's best result in decades.",
     "AP"),
    (12, "Americas", "WASHINGTON — SECURITY",
     "Cyberattack breaches an unclassified CIA system",
     "Intruders got into an unclassified system, AP source says.",
     "AP"),
    (13, "Asia", "SEOUL — DIPLOMACY",
     "North Korea expels a senior Swiss diplomat",
     "Pyongyang orders the envoy to leave.",
     "AP"),
]

# ---- briefs: (num, text incl. source) ----
BRIEFS = [
    (14, "Jordan: death sentence over officer killing (REUTERS)"),
    (15, "Gaza: Hamas security chief killed in strike (BBC)"),
    (16, "DR Congo plane missing; rebels claim kill (BBC)"),
    (17, "Sahel rebels fight with cheap drones (REUTERS)"),
    (18, "Nigeria monarch, 92, suspended over claims (BBC)"),
    (19, "Argentina slips into technical recession (INDEC)"),
    (20, "Venezuela: clashes over minimum wage (AL JAZEERA)"),
    (21, "Shein to pay $100m in US FTC settlement (AP)"),
    (22, "Nikkei poll: 65,000 by June 2027 (REUTERS)"),
    (23, "Australia inflation still above target (REUTERS)"),
    (24, "India: food prices squeeze households (BBC)"),
    (25, "Hanoi eatery blast kills 6 (AP)"),
    (26, "Turkish helicopter crash kills 5 crew (AP)"),
    (27, "Sarkozy and Carla Bruni to face trial (BBC)"),
    (28, "NATO vows defence against space threats (BBC)"),
    (29, "Cuba life expectancy falls, says WHO (WHO)"),
    (30, "Dhaka garment workers win 36% pay rise (REPORTS)"),
    (31, "Nollywood star Pete Edochie dies at 79 (BBC)"),
]

REGIONS = [("Europe", 5), ("Asia", 7), ("Middle East", 4), ("Africa", 4),
           ("Americas", 7), ("Oceania", 2), ("Global", 2)]

STATS = [
    ("-5.3%", "Seoul shares fall most in Asia rout"),
    ("$90.97", "Brent crude a barrel"),
    ("~500,000", "Russian war dead, Moscow's own figures"),
    ("259", "Democrats' House seats, most since 1990"),
    ("5 tons", "lead azide to be detonated in Iowa"),
    ("00:18 UTC", "Shenzhou-24 lifts off from Jiuquan"),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off from Jiuquan"),
    ("03:56", "Shenzhou-24 docks at the Tiangong station"),
    ("18:45", "ESA unveils Hera's first close-up images"),
]

# ---- text helpers ----
def wrap(draw, text, fnt, width):
    """Wrap text to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def fit_font(draw, text, start_size, width, name="GoogleSans-Regular.ttf", minimum=10):
    size = start_size
    while size > minimum and draw.textlength(text, font=font(name, size)) > width:
        size -= 1
    return font(name, size)

# ---- lead illustrations (drawn by code) ----
def ill_houthis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    # stars
    for sx, sy in [(20, 18), (70, 10), (130, 24), (200, 12), (260, 20), (45, 40), (170, 34)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(240, 240, 220))
    # moon
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(240, 230, 190))
    # refinery silhouette
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(8, 14, 28))
    for tx in (30, 80, 150, 210):
        d.rectangle([x + tx, y + h - 78, x + tx + 14, y + h - 40], fill=(8, 14, 28))
        d.rectangle([x + tx + 5, y + h - 96, x + tx + 9, y + h - 78], fill=(8, 14, 28))
    # flare
    d.ellipse([x + 84, y + h - 58, x + 96, y + h - 46], fill=(255, 170, 40))
    d.ellipse([x + 88, y + h - 54, x + 92, y + h - 50], fill=(255, 230, 120))
    # drones + dashed paths
    for dx, dy in [(60, 30), (150, 44), (230, 28)]:
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=(255, 220, 90))
    for i in range(0, 60, 8):
        d.ellipse([x + 62 + i, y + 34 + i // 3, x + 64 + i, y + 36 + i // 3], fill=(255, 220, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(255, 255, 255))

def ill_shenzhou(d, x, y, w, h):
    # draw on a temp layer so the earth curve cannot spill outside the box
    w, h = int(w), int(h)
    tmp = Image.new("RGB", (w, h), (10, 20, 60))
    t = ImageDraw.Draw(tmp)
    for sx, sy in [(15, 15), (60, 30), (120, 12), (180, 26), (240, 14), (290, 40), (90, 55), (210, 55)]:
        t.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    t.ellipse([-120, h - 18, w + 120, h + 130], fill=(30, 90, 160))
    t.ellipse([-120, h - 18, w + 120, h + 130], outline=(90, 160, 220), width=2)
    cx = w // 2
    t.polygon([(cx - 12, 78), (cx + 12, 78), (cx + 12, 30), (cx, 12), (cx - 12, 30)], fill=(245, 245, 245))
    t.rectangle([cx - 20, 52, cx - 12, 78], fill=(185, 28, 28))
    t.rectangle([cx + 12, 52, cx + 20, 78], fill=(185, 28, 28))
    t.polygon([(cx - 8, 78), (cx + 8, 78), (cx + 4, 100), (cx - 4, 100)], fill=(255, 170, 40))
    t.ellipse([cx - 4, 96, cx + 4, 104], fill=(255, 230, 120))
    d._image.paste(tmp, (int(x), int(y)))

def ill_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # grid
    for gy in range(y + 16, y + h - 8, 18):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(228, 228, 228), width=1)
    # falling bars
    vals = [86, 72, 76, 58, 62, 44, 48, 30, 34, 18]
    bw = (w - 24) // len(vals)
    for i, v in enumerate(vals):
        bx = x + 12 + i * bw
        d.rectangle([bx, y + h - 12 - v, bx + bw - 4, y + h - 12], fill=(185, 28, 28))
    # red trend line
    pts = [(x + 14 + i * bw, y + h - 20 - v) for i, v in enumerate(vals)]
    d.line(pts, fill=(140, 20, 20), width=3)

ILLUSTRATIONS = {1: ill_houthis, 2: ill_shenzhou, 3: ill_markets}

def draw_lead(d, x, y, w, h, story):
    num, region, tag, headline, deck, source = story
    ill_h = 100
    ILLUSTRATIONS[num](d, x, y, w, ill_h)
    # red label banner over illustration
    label = tag.split(" — ")[0]
    f_lbl = F_BOLD(15)
    lw = d.textlength(label, font=f_lbl) + 16
    d.rectangle([x, y + 6, x + lw, y + 28], fill=RED)
    d.text((x + 8, y + 9), label, font=f_lbl, fill=(255, 255, 255))
    # white tag box bottom-right of illustration
    f_tag = F_MED(10)
    tag2 = "4 drones downed" if num == 1 else ("Docked 03:56 UTC" if num == 2 else "Closing prices")
    tw = d.textlength(tag2, font=f_tag) + 12
    d.rectangle([x + w - tw - 6, y + ill_h - 20, x + w - 6, y + ill_h - 4], fill=(255, 255, 255))
    d.text((x + w - tw, y + ill_h - 18), tag2, font=f_tag, fill=INK)
    ty = y + ill_h + 6
    d.text((x, ty), f"{num}  {tag}", font=F_BOLD(11), fill=RED)
    ty += 15
    ty = draw_wrapped(d, x, ty, headline, F_BOLD(19), w, leading=21, max_lines=2)
    ty += 2
    ty = draw_wrapped(d, x, ty, deck, F_REG(12.5), w, fill=(60, 58, 52), leading=15, max_lines=2)
    d.text((x, y + h - 13), f"({source})", font=F_MED(10.5), fill=GREY)

def draw_medium(d, x, y, w, h, story):
    num, region, tag, headline, deck, source = story
    col = REGION_COLORS[region]
    # top band with number + label
    d.rectangle([x, y, x + w, y + 22], fill=col)
    lab = tag.split(" — ")[0]
    f_lab = fit_font(d, lab, 12, w - 34, "GoogleSans-Bold.ttf", 9)
    d.text((x + 6, y + 5), lab, font=f_lab, fill=(255, 255, 255))
    d.text((x + w - 20, y + 4), str(num), font=F_BOLD(13), fill=(255, 255, 255))
    ty = y + 27
    ty = draw_wrapped(d, x, ty, headline, F_BOLD(14.5), w, leading=17, max_lines=2)
    ty += 1
    draw_wrapped(d, x, ty, deck, F_REG(11.5), w, fill=(60, 58, 52), leading=14, max_lines=2)
    d.text((x, y + h - 12), f"({source})", font=F_MED(9.5), fill=GREY)
    # thin rule under card
    d.line([(x, y + h), (x + w, y + h)], fill=(200, 196, 186), width=1)

# ---- world map (simplified continents, equirectangular) ----
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-55, 62), (-60, 47),
     (-75, 35), (-80, 25), (-97, 26), (-105, 20), (-110, 23), (-125, 40), (-125, 49),
     (-145, 60), (-168, 66)],
    # South America
    [(-80, 10), (-60, 10), (-50, 0), (-35, -8), (-40, -20), (-55, -35), (-70, -55),
     (-75, -40), (-80, -20), (-80, 10)],
    # Europe
    [(-10, 36), (0, 44), (10, 45), (20, 55), (30, 60), (30, 70), (10, 70), (0, 60),
     (-10, 50), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 30), (10, 37), (30, 32), (35, 28), (43, 12), (51, 10), (40, -5),
     (35, -20), (20, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    # Asia
    [(30, 70), (60, 70), (90, 75), (120, 75), (170, 67), (180, 65), (160, 55),
     (140, 40), (127, 35), (120, 20), (105, 10), (95, 15), (80, 8), (70, 20),
     (60, 25), (45, 30), (35, 36), (30, 60)],
    # Australia
    [(113, -22), (114, -30), (130, -32), (140, -38), (150, -37), (153, -27),
     (146, -19), (142, -11), (135, -12), (126, -14), (113, -22)],
]

# (num, lon, lat)
PINS = [
    (1, 50, 26.6), (2, 100.3, 39.8), (3, 139.7, 35.7), (4, 121.5, 31.2),
    (6, -93.1, 41.9), (7, 56.5, 26.6), (8, 30.5, 50.5), (9, 160, -9.6),
    (10, -3.7, 40.4), (11, -77, 38.9), (12, -80.5, 40.0), (13, 125.8, 39),
    (14, 36, 31.9), (16, 29, -3), (19, -58.4, -34.6), (22, 142, 38),
    (25, 105.8, 21), (29, -82.4, 23.1),
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    def proj(lon, lat):
        px = x + (lon + 170) / 360 * w
        py = y + (85 - lat) / 145 * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lo, la) for lo, la in poly], fill=LAND, outline=LAND_LINE)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        f = F_BOLD(9)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 5), str(num), font=f, fill=(255, 255, 255))

def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 28
    CW = W - 2 * M
    y = 12
    # masthead
    d.text((M, y), "THE WORLD IN ONE DAY", font=F_BOLD(16), fill=RED)
    right = "31 STORIES · 7 REGIONS · EVERY ONE DATED 25 NOVEMBER 2026"
    f_r = F_BOLD(12)
    d.text((W - M - d.textlength(right, font=f_r), y + 3), right, font=f_r, fill=INK)
    y += 24
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 8
    # giant date
    f_date = fit_font(d, DATE_STR, 66, CW, "GoogleSans-Bold.ttf", 50)
    d.text((M, y), DATE_STR, font=f_date, fill=INK)
    y += int(f_date.size * 1.15) + 2
    # red sub-headline
    sub = ("Houthi drones hit Saudi oil sites  ·  Shenzhou-24 carries Pakistan's first "
           "astronaut  ·  Asia's markets tumble on tariff threats")
    y = draw_wrapped(d, M, y, sub, F_MED(19), CW, fill=RED, leading=23, max_lines=2)
    y += 4
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 8
    # stat strip: 6 numbers
    colw = CW / 6
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * colw
        if i:
            d.line([(cx - 5, y), (cx - 5, y + 56)], fill=(200, 196, 186), width=1)
        f_n = fit_font(d, num, 30, colw - 12, "GoogleSans-Bold.ttf", 20)
        d.text((cx, y), num, font=f_n, fill=INK)
        draw_wrapped(d, cx, y + 36, lab, F_REG(11.5), colw - 12, fill=GREY, leading=13, max_lines=2)
    y += 66
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5
    # region strip
    segw = CW / 7
    for i, (name, cnt) in enumerate(REGIONS):
        cx = M + i * segw
        d.rectangle([cx, y, cx + segw - 2, y + 20], fill=REGION_COLORS[name])
        t = f"{name} {cnt}"
        f_t = fit_font(d, t, 12, segw - 8, "GoogleSans-Bold.ttf", 9)
        d.text((cx + (segw - 2 - d.textlength(t, font=f_t)) / 2, y + 4), t, font=f_t, fill=(255, 255, 255))
    y += 26
    # lead cards
    lw = (CW - 26) / 3
    lh = 210
    for i, story in enumerate(LEADS):
        draw_lead(d, M + i * (lw + 13), y, lw, lh, story)
    y += lh + 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 8
    # medium cards: 2 rows x 5
    mw = (CW - 40) / 5
    mh = 100
    for row in range(2):
        for col in range(5):
            story = MEDIUM[row * 5 + col]
            draw_medium(d, M + col * (mw + 10), y + row * (mh + 8), mw, mh, story)
    y += 2 * mh + 8 + 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6
    # timeline
    d.text((M, y), "THE DAY IN UTC", font=F_BOLD(13), fill=RED)
    tx = M + 150
    for t, ev in TIMELINE:
        d.text((tx, y), t, font=F_BOLD(12), fill=INK)
        d.text((tx + 52, y), ev, font=F_REG(12), fill=INK)
        tx += 52 + d.textlength(ev, font=F_REG(12)) + 26
    y += 20
    # bottom: map left, ALSO list right
    map_w = 330
    d.text((M, y), "WHERE IT HAPPENED", font=F_BOLD(14), fill=INK)
    d.text((M + map_w + 16, y), "ALSO ON WEDNESDAY 25 NOVEMBER — 18 MORE STORIES",
           font=F_BOLD(14), fill=INK)
    y += 20
    map_h = 150
    draw_map(d, M, y, map_w, map_h)
    d.text((M, y + map_h + 4), "Each number matches that story on this page. 5 is in deep space.",
           font=F_REG(10), fill=GREY)
    ax = M + map_w + 16
    aw = W - M - ax
    col_w = (aw - 14) / 2
    for i, (num, text) in enumerate(BRIEFS):
        col = i // 9
        row = i % 9
        bx = ax + col * (col_w + 14)
        by = y + row * 19
        d.text((bx, by), f"{num}", font=F_BOLD(12), fill=RED)
        f_b = fit_font(d, text, 12, col_w - 24, "GoogleSans-Regular.ttf", 10)
        d.text((bx + 22, by), text, font=f_b, fill=INK)
    y += map_h + 22
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6
    # DATE CHECK
    d.rectangle([M, y, W - M, y + 44], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=F_BOLD(12), fill=RED)
    dc = ("Left out — reported before today: COP31 collapse · Huawei verdict · Tuesday's "
          "Champions League results · Senegal title ruling · Zambia treason case · Cartagena siege.")
    draw_wrapped(d, M + 8, y + 21, dc, F_REG(11.5), CW - 16, leading=14, max_lines=2)
    y += 50
    # footer
    foot = ("Every story here happened, or was first reported, on Wednesday 25 November 2026.  "
            "Sources named beside each story · original drawings")
    d.text((M, y), foot, font=F_REG(10.5), fill=GREY)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    render()
