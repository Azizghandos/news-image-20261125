#!/usr/bin/env python3
"""Draw 'The World in One Picture - Wednesday 25 November 2026'.

A 1024x1024 infographic of six verified news stories of 25 November 2026
(events of late 24 November still leading the wires on the 25th).
Every shape is drawn with Pillow primitives; no photos, no network.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (11, 22, 38)          # deep ink blue
PAPER = (247, 244, 236)     # warm paper
GOLD = (212, 168, 60)
WHITE = (255, 255, 255)
GREY = (90, 100, 114)
DARK = (24, 34, 50)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_tower(d, x, y, s, accent):
    """Skyscraper with lit windows and a small drone above it."""
    d.rectangle([x, y + 14 * s, x + 26 * s, y + 78 * s], fill=accent)
    d.polygon([(x + 13 * s, y), (x + 26 * s, y + 14 * s), (x, y + 14 * s)], fill=accent)
    for r in range(5):
        for c in range(2):
            wx = x + (4 + c * 12) * s
            wy = y + (20 + r * 11) * s
            d.rectangle([wx, wy, wx + 6 * s, wy + 5 * s], fill=(255, 235, 160))
    # drone + burst
    d.ellipse([x + 34 * s, y + 6 * s, x + 42 * s, y + 14 * s], fill=(235, 90, 70))
    for dx, dy in [(-6, 0), (6, 0), (0, -6), (0, 6)]:
        d.line([x + 38 * s, y + 10 * s, x + (38 + dx) * s, y + (10 + dy) * s],
               fill=(235, 90, 70), width=2)


def draw_ship(d, x, y, s, accent):
    """Warship on waves."""
    d.polygon([(x, y + 26 * s), (x + 58 * s, y + 26 * s), (x + 50 * s, y + 42 * s),
               (x + 8 * s, y + 42 * s)], fill=accent)
    d.rectangle([x + 20 * s, y + 12 * s, x + 34 * s, y + 26 * s], fill=accent)
    d.line([x + 27 * s, y + 2 * s, x + 27 * s, y + 12 * s], fill=accent, width=3)
    d.polygon([(x + 27 * s, y + 2 * s), (x + 40 * s, y + 8 * s), (x + 27 * s, y + 10 * s)],
              fill=(235, 90, 70))
    for i, wy in enumerate([52, 60]):
        for k in range(3):
            cx = x + (6 + k * 20) * s
            d.arc([cx, y + wy * s, cx + 14 * s, y + (wy + 8) * s], 0, 180,
                  fill=(120, 180, 220), width=3)


def draw_medal(d, x, y, s, accent):
    """Medal on a ribbon with a star."""
    d.polygon([(x + 8 * s, y), (x + 22 * s, y), (x + 30 * s, y + 26 * s),
               (x + 16 * s, y + 34 * s)], fill=(200, 60, 60))
    d.polygon([(x + 36 * s, y), (x + 50 * s, y), (x + 42 * s, y + 26 * s),
               (x + 28 * s, y + 34 * s)], fill=(60, 90, 180))
    d.ellipse([x + 6 * s, y + 28 * s, x + 52 * s, y + 74 * s], fill=accent,
              outline=(150, 110, 20), width=3)
    cx, cy, r = x + 29 * s, y + 51 * s, 12 * s
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))


def draw_chip(d, x, y, s, accent):
    """Microchip with pins and a gavel bar."""
    d.rectangle([x + 10 * s, y + 10 * s, x + 48 * s, y + 48 * s], fill=DARK,
                outline=accent, width=3)
    d.rectangle([x + 20 * s, y + 20 * s, x + 38 * s, y + 38 * s], fill=accent)
    for i in range(4):
        px = x + (16 + i * 9) * s
        d.line([px, y + 2 * s, px, y + 10 * s], fill=accent, width=3)
        d.line([px, y + 48 * s, px, y + 56 * s], fill=accent, width=3)
        py = y + (16 + i * 9) * s
        d.line([x + 2 * s, py, x + 10 * s, py], fill=accent, width=3)
        d.line([x + 48 * s, py, x + 56 * s, py], fill=accent, width=3)
    # gavel
    d.rectangle([x + 8 * s, y + 62 * s, x + 50 * s, y + 68 * s], fill=(150, 90, 40))
    d.rectangle([x + 26 * s, y + 56 * s, x + 32 * s, y + 68 * s], fill=(120, 70, 30))


def draw_shield(d, x, y, s, accent):
    """Shield with a crack and a keyhole."""
    d.polygon([(x + 6 * s, y), (x + 52 * s, y), (x + 52 * s, y + 34 * s),
               (x + 29 * s, y + 62 * s), (x + 6 * s, y + 34 * s)], fill=accent)
    d.polygon([(x + 29 * s, y + 2 * s), (x + 26 * s, y + 22 * s),
               (x + 33 * s, y + 34 * s), (x + 27 * s, y + 48 * s),
               (x + 31 * s, y + 60 * s)], fill=(255, 255, 255))
    d.ellipse([x + 24 * s, y + 20 * s, x + 34 * s, y + 30 * s], fill=WHITE)
    d.rectangle([x + 27 * s, y + 28 * s, x + 31 * s, y + 40 * s], fill=WHITE)


def draw_cricket(d, x, y, s, accent):
    """Cricket bat striking a ball."""
    d.line([x + 14 * s, y + 62 * s, x + 44 * s, y + 14 * s], fill=(190, 140, 70),
           width=9 * s)
    d.line([x + 44 * s, y + 14 * s, x + 52 * s, y + 4 * s], fill=(150, 100, 50),
           width=6 * s)
    d.ellipse([x + 44 * s, y + 52 * s, x + 62 * s, y + 70 * s], fill=(200, 60, 60),
              outline=WHITE, width=2)
    d.arc([x + 44 * s, y + 52 * s, x + 62 * s, y + 70 * s], 200, 340, fill=WHITE,
          width=2)
    for dx, dy in [(-8, -8), (-2, -12), (4, -10)]:
        d.line([x + 52 * s, y + 56 * s, x + (52 + dx) * s, y + (56 + dy) * s],
               fill=GOLD, width=2)


ICONS = {
    "tower": draw_tower,
    "ship": draw_ship,
    "medal": draw_medal,
    "chip": draw_chip,
    "shield": draw_shield,
    "cricket": draw_cricket,
}

STORIES = [
    {
        "tag": "MIDDLE EAST",
        "accent": (200, 70, 50),
        "icon": "tower",
        "headline": "Riyadh tower hit again",
        "body": "A Houthi drone strike hits Riyadh's tallest tower, the PIF Tower, for the second time in a week. Saudi civil defence says 11 people are wounded.",
    },
    {
        "tag": "UKRAINE · LIBYA",
        "accent": (60, 120, 200),
        "icon": "ship",
        "headline": "Kyiv sinks a Russian warship off Libya",
        "body": "Zelenskyy confirms Ukrainian sea drones sank the corvette Merkury at Benghazi and hit a cargo ship said to carry weapons.",
    },
    {
        "tag": "UNITED STATES",
        "accent": (180, 140, 30),
        "icon": "medal",
        "headline": "Medal of Freedom for Giuliani",
        "body": "Trump awards the nation's highest civilian honour to ex-mayor Rudy Giuliani, 82, in a private Oval Office ceremony.",
    },
    {
        "tag": "TECH & LAW",
        "accent": (90, 140, 90),
        "icon": "chip",
        "headline": "Huawei guilty on 10 counts",
        "body": "A Brooklyn jury convicts Huawei of fraud and trade-secret theft over its Iran business, but acquits it of racketeering.",
    },
    {
        "tag": "CYBER",
        "accent": (150, 90, 180),
        "icon": "shield",
        "headline": "CIA and ODNI systems breached",
        "body": "Hackers break into an unclassified network the CIA and ODNI use to analyse public information. No classified systems are hit.",
    },
    {
        "tag": "SPORT",
        "accent": (40, 150, 140),
        "icon": "cricket",
        "headline": "England crush Australia in T20",
        "body": "Aneurin Donald smashes 85 off 32 balls as England chase 185 in 13.1 overs to level the T20 series 1-1 on the Gold Coast.",
    },
]

MARGIN = 28
GAP = 16
HEADER_H = 168
FOOTER_H = 44
GRID_TOP = MARGIN + HEADER_H + GAP
GRID_H = H - GRID_TOP - FOOTER_H - MARGIN
PANEL_W = (W - 2 * MARGIN - 2 * GAP) // 3
PANEL_H = (GRID_H - GAP) // 2


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.line([MARGIN, MARGIN + 8, W - MARGIN, MARGIN + 8], fill=GOLD, width=3)
    d.text((MARGIN, MARGIN + 20), "THE WORLD IN ONE PICTURE",
           font=font(SERIF_B, 46), fill=WHITE)
    d.text((MARGIN, MARGIN + 82), "WEDNESDAY  25  NOVEMBER  2026",
           font=font(SANS_B, 34), fill=GOLD)
    d.text((MARGIN, MARGIN + 126),
           "Six stories from one day, verified from the world's wires",
           font=font(SANS, 22), fill=(200, 208, 220))
    d.line([MARGIN, MARGIN + HEADER_H - 6, W - MARGIN, MARGIN + HEADER_H - 6],
           fill=GOLD, width=3)

    # ---- story grid ----
    head_f = font(SANS_B, 25)
    body_f = font(SANS, 19)
    tag_f = font(SANS_B, 16)
    for i, st in enumerate(STORIES):
        row, col = divmod(i, 3)
        x0 = MARGIN + col * (PANEL_W + GAP)
        y0 = GRID_TOP + row * (PANEL_H + GAP)
        x1, y1 = x0 + PANEL_W, y0 + PANEL_H
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PAPER)
        # accent strip
        d.rounded_rectangle([x0, y0, x1, y0 + 34], radius=14, fill=st["accent"])
        d.rectangle([x0, y0 + 20, x1, y0 + 34], fill=st["accent"])
        d.text((x0 + 14, y0 + 7), st["tag"], font=tag_f, fill=WHITE)
        # icon, bottom-right corner of the panel (clear of the text)
        ICONS[st["icon"]](d, x1 - 92, y1 - 92, 1, st["accent"])
        # headline (full panel width)
        lines = wrap(d, st["headline"], head_f, PANEL_W - 28)
        hy = y0 + 46
        for ln in lines[:2]:
            d.text((x0 + 14, hy), ln, font=head_f, fill=DARK)
            hy += 30
        # body (up to 5 lines, full width)
        body_lines = wrap(d, st["body"], body_f, PANEL_W - 28)
        by = hy + 6
        for ln in body_lines[:5]:
            d.text((x0 + 14, by), ln, font=body_f, fill=(60, 70, 84))
            by += 25

    # ---- footer ----
    fy = H - MARGIN - FOOTER_H + 8
    d.text((MARGIN, fy), "Sources: Reuters · BBC · The New York Times · Associated Press · ESPNcricinfo",
           font=font(SANS, 17), fill=(170, 180, 195))
    d.text((MARGIN, fy + 24), "make.fun news-image-20261125  ·  The day's news, in one picture.",
           font=font(SANS, 17), fill=(170, 180, 195))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
