#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Flat editorial illustration: a masthead naming the day, one lead story
(the Shenzhen trilateral summit) and six more of the day's most
consequential stories from five regions. Run: python3 draw.py
Writes entry.png next to this file. Deterministic: no randomness,
no network, fixed fonts.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 46)
NAVY = (20, 33, 61)
RED = (193, 39, 45)
GOLD = (232, 163, 23)
TEAL = (27, 127, 122)
BLUE = (46, 95, 163)
SKY = (220, 231, 240)
WHITE = (255, 255, 255)
GREY = (90, 96, 110)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(d, cx, y, text, fnt, fill):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=RED if i % 2 == 0 else WHITE)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=NAVY)
    for r in range(5):
        for c in range(6):
            sx = x + 4 + c * (cw - 8) / 5
            sy = y + 3 + r * (ch - 6) / 4
            d.ellipse([sx, sy, sx + 2.5, sy + 2.5], fill=WHITE)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=RED)
    d.ellipse([x + w * 0.06, y + h * 0.12, x + w * 0.22, y + h * 0.40],
              fill=GOLD)
    for fx, fy in [(0.34, 0.18), (0.42, 0.30), (0.42, 0.46), (0.34, 0.58)]:
        d.ellipse([x + w * fx, y + h * fy, x + w * (fx + 0.06),
                   y + h * (fy + 0.09)], fill=GOLD)


def flag_ru(d, x, y, w, h):
    for i, col in enumerate([WHITE, (0, 57, 166), RED]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def flag_pl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 2], fill=WHITE)
    d.rectangle([x, y + h / 2, x + w, y + h], fill=RED)


def skyline(d, x0, y_base, x1, color, seed_heights):
    """Dark tower silhouettes along y_base."""
    n = len(seed_heights)
    step = (x1 - x0) / n
    for i, hh in enumerate(seed_heights):
        bx = x0 + i * step
        bw = step * 0.72
        d.rectangle([bx, y_base - hh, bx + bw, y_base], fill=color)
        for wy in range(int(y_base - hh + 8), int(y_base - 6), 14):
            for wx in range(int(bx + 4), int(bx + bw - 4), 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)


def explosion(d, cx, cy, r, color):
    """Starburst: 12 spikes + core."""
    for k in range(12):
        a = math.pi * k / 6
        x2 = cx + math.cos(a) * r
        y2 = cy + math.sin(a) * r
        d.line([cx, cy, x2, y2], fill=color, width=5)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=color)
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
              fill=(255, 214, 64))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 104], fill=NAVY)
center_text(d, W // 2, 10, "THE WORLD IN ONE PICTURE", font(F_B, 20), GOLD)
center_text(d, W // 2, 38, "SATURDAY, 21 NOVEMBER 2026", font(F_B, 52), WHITE)
d.rectangle([0, 104, W, 110], fill=RED)

# ---- lead story: Shenzhen trilateral summit ----
LX0, LY0, LX1, LY1 = 16, 118, 1008, 452
d.rounded_rectangle([LX0, LY0, LX1, LY1], radius=10, fill=SKY,
                    outline=NAVY, width=2)
# skyline along the bottom of the illustration zone
skyline(d, LX0 + 30, 348, LX1 - 30, NAVY,
        [70, 120, 90, 150, 80, 130, 100, 160, 85, 120, 95, 140, 75, 110])
# three flag poles with the US, Chinese and Russian flags
for i, fl in enumerate([flag_us, flag_cn, flag_ru]):
    px = 300 + i * 210
    d.line([px, 170, px, 348], fill=INK, width=4)
    d.ellipse([px - 5, 164, px + 5, 174], fill=GOLD)
    fl(d, px + 4, 176, 92, 58)
# headline strip
d.rectangle([LX0, 356, LX1, LY1], fill=WHITE)
center_text(d, W // 2, 366, "TRUMP, XI & PUTIN MEET IN SHENZHEN",
            font(F_B, 34), INK)
center_text(d, W // 2, 408,
            "Trilateral summit at APEC  •  nuclear-risk talks agreed",
            font(F_R, 20), GREY)

# ---- six story panels, 3 x 2 grid ----
PANELS = [
    # (bg, headline, subline, draw key)
    ((235, 238, 245), "RUSSIA HITS KYIV BRIDGES",
     "Missiles cross into Poland — NATO: grave violation", "kyiv"),
    ((245, 232, 214), "SAUDI DOWNS 3 MISSILES",
     "Houthi attack intercepted over Riyadh", "riyadh"),
    ((255, 255, 255), "AI SELL-OFF SINKS MARKETS",
     "S&P, Dow fall into correction — S&P −3.7%", "markets"),
    ((219, 238, 235), "COP31 IN OVERTIME",
     "Fossil-fuel row deadlocks Antalya talks", "cop"),
    ((232, 228, 240), "ICJ RULES ON MYANMAR",
     "Rohingya genocide case: 'crucial step'", "icj"),
    ((240, 245, 232), "CANCER PILL BREAKTHROUGH",
     "Tumours undetectable in 1 in 12 patients", "pill"),
]
COLS_X = [16, 352, 688]
ROWS_Y = [464, 736]
PW, PH = 320, 260


def panel_art(key, x0, y0):
    """Flat illustration inside the top ~140 px of a panel."""
    cx = x0 + PW // 2
    if key == "kyiv":
        d.rectangle([x0, y0 + 96, x0 + PW, y0 + 140], fill=(120, 170, 220))
        d.arc([x0 + 40, y0 + 40, x0 + PW - 40, y0 + 150], 180, 360,
              fill=INK, width=8)
        d.line([x0 + 40, y0 + 96, x0 + PW - 40, y0 + 96], fill=INK, width=6)
        explosion(d, cx - 40, y0 + 52, 22, (255, 122, 26))
        explosion(d, cx + 55, y0 + 70, 15, (255, 122, 26))
        flag_pl(d, x0 + PW - 52, y0 + 12, 40, 26)
        d.rectangle([x0 + PW - 52, y0 + 12, x0 + PW - 12, y0 + 38],
                    outline=INK, width=2)
    elif key == "riyadh":
        d.rectangle([x0, y0 + 110, x0 + PW, y0 + 140], fill=(222, 196, 138))
        for tx, th in [(60, 90), (120, 70), (190, 100), (250, 60)]:
            d.rectangle([x0 + tx, y0 + 140 - th, x0 + tx + 26, y0 + 140],
                        fill=(90, 70, 50))
        d.line([x0 + 60, y0 + 30, x0 + 120, y0 + 90], fill=NAVY, width=4)
        d.line([x0 + 260, y0 + 26, x0 + 200, y0 + 86], fill=NAVY, width=4)
        explosion(d, cx, y0 + 96, 18, GOLD)
    elif key == "markets":
        pts = [(x0 + 16, y0 + 40), (x0 + 70, y0 + 60), (x0 + 120, y0 + 52),
               (x0 + 170, y0 + 84), (x0 + 220, y0 + 78), (x0 + 270, y0 + 116),
               (x0 + 304, y0 + 128)]
        d.line(pts, fill=RED, width=6, joint="curve")
        d.polygon([(x0 + 292, y0 + 116), (x0 + 316, y0 + 120),
                   (x0 + 300, y0 + 140)], fill=RED)
        d.text((x0 + 18, y0 + 96), "-3.7%", font=font(F_B, 34), fill=RED)
    elif key == "cop":
        d.ellipse([cx - 52, y0 + 18, cx + 52, y0 + 122], fill=TEAL)
        d.ellipse([cx - 30, y0 + 36, cx - 6, y0 + 62], fill=(110, 200, 120))
        d.ellipse([cx + 8, y0 + 70, cx + 34, y0 + 100], fill=(110, 200, 120))
        d.ellipse([cx - 34, y0 + 78, cx - 10, y0 + 100], fill=(110, 200, 120))
        d.text((x0 + 18, y0 + 126), "DAY 2 OVERTIME", font=font(F_B, 15),
               fill=INK)
    elif key == "icj":
        d.line([cx, y0 + 22, cx, y0 + 118], fill=GOLD, width=6)
        d.line([cx - 62, y0 + 40, cx + 62, y0 + 40], fill=GOLD, width=5)
        for sx in (cx - 62, cx + 62):
            d.line([sx, y0 + 40, sx, y0 + 66], fill=GOLD, width=3)
            d.arc([sx - 26, y0 + 58, sx + 26, y0 + 106], 0, 180,
                  fill=GOLD, width=5)
        d.rectangle([cx - 34, y0 + 118, cx + 34, y0 + 130], fill=GOLD)
        d.rectangle([cx - 4, y0 + 96, cx + 4, y0 + 118], fill=GOLD)
    elif key == "pill":
        d.rounded_rectangle([cx - 78, y0 + 48, cx + 78, y0 + 96], radius=24,
                            fill=RED)
        d.rounded_rectangle([cx - 78, y0 + 48, cx, y0 + 96], radius=24,
                            fill=WHITE, outline=RED, width=2)
        for ox, oy, r in [(cx - 100, y0 + 112, 9), (cx - 70, y0 + 124, 7),
                          (cx + 88, y0 + 110, 8), (cx + 64, y0 + 126, 6)]:
            d.ellipse([ox - r, oy - r, ox + r, oy + r],
                      outline=TEAL, width=3)


for i, (bg, head, sub, key) in enumerate(PANELS):
    x0 = COLS_X[i % 3]
    y0 = ROWS_Y[i // 3]
    d.rounded_rectangle([x0, y0, x0 + PW, y0 + PH], radius=10, fill=WHITE,
                        outline=(200, 200, 200), width=2)
    panel_art(key, x0, y0)
    hl = wrap(d, head, font(F_B, 21), PW - 24)
    hy = y0 + 148
    for ln in hl[:2]:
        center_text(d, x0 + PW // 2, hy, ln, font(F_B, 21), INK)
        hy += 24
    sl = wrap(d, sub, font(F_R, 15), PW - 24)
    for ln in sl[:2]:
        center_text(d, x0 + PW // 2, hy + 4, ln, font(F_R, 15), GREY)
        hy += 19

# ---- footer ----
center_text(d, W // 2, 1004,
            "21 NOVEMBER 2026  •  SUMMED UP FROM WORLD NEWS REPORTS OF THE DAY",
            font(F_R, 14), GREY)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
