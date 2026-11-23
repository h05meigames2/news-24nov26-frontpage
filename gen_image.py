#!/usr/bin/env python3
"""Render a one-page front page summing up world news of 24 November 2026.

Original artwork drawn procedurally with Pillow only (stdlib + Pillow).
Deterministic: same bytes on every run, no network, no timestamps.
Output: entry.png (1024x1024, < 1 MiB) next to this script.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)      # off-white newsprint
INK = (27, 36, 54)           # ink navy/black
RED = (179, 32, 44)          # lead accent
GREY = (110, 108, 96)
LINE = (27, 36, 54)
PANEL_BG = (255, 253, 246)
PANEL_LINE = (196, 188, 168)
BODY = (58, 58, 52)

REGION_COLORS = {
    "AMERICAS": (122, 92, 46),
    "EUROPE": (74, 107, 138),
    "MIDDLE EAST": (138, 90, 60),
    "GLOBAL": (90, 107, 82),
    "ASIA": (107, 90, 122),
    "AFRICA": (150, 110, 40),
    "SPORT": (40, 110, 95),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 32)
F_LEAD_TAG = font("DejaVuSans-Bold.ttf", 20)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 54)
F_LEAD_DECK = font("DejaVuSans.ttf", 20)
F_TAG = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_DECK = font("DejaVuSans.ttf", 20)
F_TICKER_HEAD = font("DejaVuSans-Bold.ttf", 18)
F_TICKER = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, cx, y, text, fnt, fill, spacing=4):
    """Draw text centred on cx with extra letter spacing."""
    total = sum(draw.textlength(ch, font=fnt) for ch in text)
    total += spacing * (len(text) - 1)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def star_points(cx, cy, r_out, r_in, n=5):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pictogram(draw, kind, x, y, s=36):
    """Small procedural pictogram inside a s x s box at (x, y)."""
    c = INK
    if kind == "chip":  # Nvidia / AI chip
        draw.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], outline=c, width=2)
        draw.rectangle([x + 13, y + 15, x + s - 13, y + s - 15], fill=(40, 110, 95))
        for px in (x + 11, x + s // 2 - 1, x + s - 15):
            draw.line([px, y + 2, px, y + 8], fill=c, width=2)
            draw.line([px, y + s - 8, px, y + s - 2], fill=c, width=2)
    elif kind == "radar":  # AWACS early-warning aircraft
        draw.ellipse([x + 4, y + 2, x + s - 4, y + 18], outline=c, width=2)
        draw.arc([x + 8, y + 5, x + s - 8, y + 15], 180, 360, fill=c, width=2)
        draw.line([x + 6, y + 22, x + s - 6, y + 22], fill=c, width=2)
        draw.line([x + 10, y + 22, x + 8, y + 30], fill=c, width=2)
        draw.line([x + s - 10, y + 22, x + s - 8, y + 30], fill=c, width=2)
        draw.line([x + 2, y + 32, x + s - 2, y + 32], fill=(74, 107, 138), width=2)
    elif kind == "flame":  # factory fire
        draw.polygon([(x + s / 2, y + 1), (x + s - 3, y + 16),
                      (x + s - 6, y + 27), (x + s / 2 + 4, y + 33),
                      (x + s / 2 - 5, y + 33), (x + 3, y + 24),
                      (x + 8, y + 14)], fill=(196, 74, 32))
        draw.polygon([(x + s / 2, y + 15), (x + s - 9, y + 26),
                      (x + s / 2, y + 31), (x + 9, y + 26)], fill=(232, 164, 32))
    elif kind == "building":  # drone strike on a building
        draw.rectangle([x + 6, y + 12, x + s - 6, y + s - 2], outline=c, width=2)
        for wx in (x + 10, x + 19):
            for wy in (y + 17, y + 24):
                draw.rectangle([wx, wy, wx + 5, wy + 4], fill=c)
        draw.ellipse([x + 14, y, x + 22, y + 8], fill=GREY)
        draw.ellipse([x + 22, y - 2, x + 30, y + 6], fill=GREY)
    elif kind == "flags":  # bilateral talks
        draw.line([x + 8, y + 4, x + 8, y + s - 2], fill=c, width=2)
        draw.line([x + s - 8, y + 4, x + s - 8, y + s - 2], fill=c, width=2)
        draw.polygon([(x + 8, y + 4), (x + 20, y + 8), (x + 8, y + 13)], fill=RED)
        draw.polygon([(x + s - 8, y + 4), (x + s - 20, y + 8),
                      (x + s - 8, y + 13)], fill=(74, 107, 138))
    elif kind == "cap":  # minister / cabinet appointment
        draw.polygon([(x + s / 2, y + 8), (x + s - 2, y + 16),
                      (x + s / 2, y + 24), (x + 2, y + 16)], fill=(107, 90, 122))
        draw.arc([x + 10, y + 20, x + s - 10, y + 32], 0, 180, fill=c, width=2)
        draw.line([x + s - 2, y + 16, x + s - 2, y + 28], fill=c, width=2)
        draw.ellipse([x + s - 5, y + 27, x + s + 1, y + 33], fill=(179, 32, 44))
    elif kind == "scales":  # constitution / law
        draw.line([x + s / 2, y + 4, x + s / 2, y + s - 4], fill=c, width=2)
        draw.line([x + 5, y + 9, x + s - 5, y + 9], fill=c, width=2)
        draw.polygon([(x + 5, y + 9), (x + 12, y + 22), (x - 2, y + 22)],
                     outline=c, width=2)
        draw.polygon([(x + s - 5, y + 9), (x + s - 12, y + 22),
                      (x + s + 2, y + 22)], outline=c, width=2)
        draw.line([x + 8, y + s - 4, x + s - 8, y + s - 4], fill=c, width=2)
    elif kind == "star":  # arrest / capture
        draw.polygon(star_points(x + s / 2, y + s / 2, s / 2, s / 5),
                     fill=(122, 92, 46))
    elif kind == "flag":  # motor racing chequered flag
        for r in range(4):
            for col in range(4):
                if (r + col) % 2 == 0:
                    draw.rectangle([x + 4 + col * 7, y + 6 + r * 7,
                                    x + 10 + col * 7, y + 12 + r * 7], fill=c)
        draw.line([x + 4, y + 6, x + 4, y + s - 2], fill=c, width=2)
    elif kind == "bat":  # cricket
        draw.rectangle([x + 12, y + 12, x + 22, y + 30], outline=c, width=2)
        draw.line([x + 17, y + 2, x + 17, y + 12], fill=c, width=3)
        draw.ellipse([x + 24, y + 26, x + 31, y + 33], fill=RED)


STORIES = [
    # (headline, deck, region, pictogram)
    ("NATO sends AWACS to Poland",
     "After 3 Russian missiles land on its soil.", "EUROPE", "radar"),
    ("Indonesia fire search resumes",
     "24 body bags out; about 29 workers missing.", "ASIA", "flame"),
    ("Sudan drones kill 4 near Khartoum",
     "Strikes hit a UN building and the airport.", "AFRICA", "building"),
    ("India, Nepal sign 8 deals",
     "Rs15,000-crore package; new cross-border train.", "ASIA", "flags"),
    ("Seoul names new top diplomat",
     "Foreign minister and spy chief nominated.", "ASIA", "cap"),
    ("Armenia drafts new constitution",
     "Step toward peace with Azerbaijan.", "EUROPE", "scales"),
    ("Dhaka vows to arrest Hasina",
     "Ex-PM to face arrest if she returns.", "ASIA", "star"),
    ("Verstappen wins in Las Vegas",
     "Red Bull star takes the Grand Prix.", "SPORT", "flag"),
    ("India\u2013NZ Test ends in draw",
     "Pant's 128 sets a record for Asia.", "SPORT", "bat"),
]

TICKER = [
    "Trump warns Iran of 'very traumatic' outcome",
    "IRGC: 78 US drones shot down",
    "Israeli strikes kill 3 in Gaza, incl. UN worker",
    "Gaza children reach UK for treatment",
    "Two killed in US university shooting",
    "China sets 2030 care targets for elderly, kids",
    "EU plans 3% digital tax on Big Tech",
    "Ferrari unveils two new 296 models",
    "Sensex falls 1,484 pts; shut for Gurpurab",
    "SoftBank to invest $2bn in Intel",
    "Pakistan cuts petrol by Rs3 a litre",
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin
    right = W - mx

    # ---- Masthead ----
    d.text((W / 2, 20), "THE WORLD IN ONE PAGE", font=F_TITLE,
           fill=INK, anchor="ma")
    draw_spaced(d, W / 2, 96, "TUESDAY 24 NOVEMBER 2026", F_DATE, RED, spacing=5)
    d.line([(mx, 140), (right, 140)], fill=LINE, width=3)
    d.line([(mx, 146), (right, 146)], fill=LINE, width=1)

    # ---- Lead panel: Nvidia brings Huang back ----
    ly0, ly1 = 158, 348
    d.rectangle([mx, ly0, right, ly1], fill=PANEL_BG, outline=RED, width=3)
    tag_txt = "LEAD \u00b7 TECH"
    tag_w = int(d.textlength(tag_txt, font=F_LEAD_TAG)) + 16
    d.rectangle([mx + 10, ly0 + 10, mx + 10 + tag_w, ly0 + 38], fill=RED)
    d.text((mx + 16, ly0 + 13), tag_txt, font=F_LEAD_TAG,
           fill=(255, 255, 255))
    pictogram(d, "chip", right - 56, ly0 + 8, 44)
    head = "Huang is back at Nvidia"
    lines = wrap(d, head, F_LEAD_HEAD, right - mx - 24)
    y = ly0 + 54
    for ln in lines:
        d.text((mx + 12, y), ln, font=F_LEAD_HEAD, fill=INK)
        y += 60
    deck = ("Board reinstates Jensen Huang as CEO 11 days after he quit; "
            "shares jump a third and the Nasdaq rallies 6%.")
    for ln in wrap(d, deck, F_LEAD_DECK, right - mx - 24):
        d.text((mx + 12, y), ln, font=F_LEAD_DECK, fill=BODY)
        y += 24

    # ---- Grid of 9 story panels ----
    gx0, gy0 = mx, 360
    pw, ph, gap = 312, 136, 12
    for i, (head, deck, region, pic) in enumerate(STORIES):
        col, row = i % 3, i // 3
        x0 = gx0 + col * (pw + gap)
        y0 = gy0 + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=PANEL_LINE, width=1)
        rc = REGION_COLORS[region]
        d.text((x0 + 10, y0 + 8), region, font=F_TAG, fill=rc)
        d.line([(x0 + 10, y0 + 28), (x0 + 10 + d.textlength(region, font=F_TAG),
                 y0 + 28)], fill=rc, width=2)
        pictogram(d, pic, x1 - 40, y0 + 2, 26)
        hlines = wrap(d, head, F_HEAD, pw - 20)
        assert len(hlines) <= 2, (head, hlines)
        y = y0 + 30
        for ln in hlines[:2]:
            d.text((x0 + 10, y), ln, font=F_HEAD, fill=INK)
            y += 30
        dlines = wrap(d, deck, F_DECK, pw - 20)
        assert len(dlines) <= 2, (deck, dlines)
        for ln in dlines[:2]:
            d.text((x0 + 10, y), ln, font=F_DECK, fill=BODY)
            y += 22

    # ---- Ticker strip: stories 10-20 ----
    ty0 = gy0 + 3 * ph + 2 * gap + 14  # 806
    d.line([(mx, ty0), (right, ty0)], fill=LINE, width=2)
    d.text((mx, ty0 + 8), "ALSO TODAY", font=F_TICKER_HEAD, fill=RED)
    col_w = (right - mx - 24) // 2
    left, right_col = TICKER[:6], TICKER[6:]
    y = ty0 + 32
    for item in left:
        d.text((mx, y), "\u2022  " + item, font=F_TICKER, fill=INK)
        y += 24
    y = ty0 + 32
    for item in right_col:
        d.text((mx + col_w + 24, y), "\u2022  " + item, font=F_TICKER, fill=INK)
        y += 24

    # ---- Footer ----
    fy = 994
    d.line([(mx, fy), (right, fy)], fill=LINE, width=1)
    d.text((W / 2, fy + 8), "24 November 2026 \u00b7 21 stories",
           font=F_FOOT, fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
