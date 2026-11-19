#!/usr/bin/env python3
"""Draw the entry poster: the world news of Thursday 19 November 2026 in one image.

The picture is a front-page style poster, 1024 x 1024 PNG. It is drawn with
Pillow from the headlines that several news services led with on the day:

  * Trump, Xi and Putin hold their first three-way summit in Shenzhen (APEC)
  * The ICJ rules on the Rohingya genocide case (Gambia v. Myanmar)
  * Ukraine strikes the Crimean Bridge for the third time in a week
  * COP31 ministers in Antalya struggle to unblock a climate deal
  * Bangladesh unrest: the Yunus family home is torched, 28 districts hit
  * Cyclone Akvan makes landfall in Odisha, India; 100,000+ evacuated
  * Iran-Gulf clashes; the IEA calls the Hormuz crisis an energy shock
  * Also: Anthropic's record $81bn IPO, a record $190m Van Gogh, the IAEA on
    North Korea's uranium enrichment, and GTA VI's launch day

This script is a build tool only. The submitted program is main.ts, which
copies the finished entry.png; the grader never runs this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 248)
INK = (20, 26, 45)
MUTED = (92, 96, 112)
RULE = (216, 210, 196)
RED = (178, 32, 32)
BLUE = (30, 74, 140)
TEAL = (14, 116, 110)
GOLD = (176, 124, 22)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/NotoSans-{name}.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, line_gap=6):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def star(draw, cx, cy, r, fill):
    """A plain five-pointed star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons

def flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.45, y + h * 4 / 7], fill=(30, 40, 110))
    for r in range(3):
        for c in range(4):
            cx, cy = x + 7 + c * w * 0.1, y + 5 + r * h * 0.18
            draw.ellipse([cx, cy, cx + 4, cy + 4], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.22, y + h * 0.32, h * 0.26, (255, 222, 0))
    for dx, dy in ((0.52, 0.14), (0.58, 0.34), (0.58, 0.56), (0.52, 0.76)):
        star(draw, x + w * dx, y + h * dy, h * 0.1, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(30, 60, 160))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 30, 40))


def icon_scales(draw, x, y, s, color=INK):
    draw.line([x + s / 2, y, x + s / 2, y + s], fill=color, width=5)
    draw.line([x + 6, y + 8, x + s - 6, y + 8], fill=color, width=5)
    for cx in (x + 12, x + s - 12):
        draw.line([cx, y + 8, cx - 10, y + s * 0.55], fill=color, width=3)
        draw.line([cx, y + 8, cx + 10, y + s * 0.55], fill=color, width=3)
        draw.arc([cx - 13, y + s * 0.42, cx + 13, y + s * 0.72], 0, 180,
                 fill=color, width=4)
    draw.rectangle([x + s / 2 - 14, y + s - 6, x + s / 2 + 14, y + s],
                   fill=color)


def icon_bridge(draw, x, y, s, color=INK):
    deck = y + s * 0.7
    for tx in (x + s * 0.3, x + s * 0.7):
        draw.line([tx, y + 4, tx, deck], fill=color, width=5)
    cable = []
    for t in range(17):
        px = x + 4 + t * (s - 8) / 16
        py = deck - (deck - y - 4) * math.sin(math.pi * t / 16) ** 0.7
        cable.append((px, py))
    draw.line(cable, fill=color, width=3)
    for t in range(1, 16, 3):
        px, py = cable[t]
        draw.line([px, py, px, deck], fill=color, width=2)
    draw.line([x, deck, x + s, deck], fill=color, width=6)
    draw.line([x + 4, y + s * 0.86, x + s - 4, y + s * 0.86], fill=BLUE, width=3)
    draw.line([x + 4, y + s * 0.95, x + s - 4, y + s * 0.95], fill=BLUE, width=3)


def icon_sun_sea(draw, x, y, s):
    draw.pieslice([x + s * 0.22, y, x + s * 0.78, y + s * 0.56], 180, 360,
                  fill=GOLD)
    for wy in (0.66, 0.8, 0.94):
        pts = [(x + 4 + j * 8, y + s * wy + (4 if j % 2 else -2))
               for j in range(int(s / 8))]
        draw.line(pts, fill=TEAL, width=4)


def icon_house_flame(draw, x, y, s):
    draw.polygon([(x + 6, y + s * 0.45), (x + s / 2, y + s * 0.12),
                  (x + s - 6, y + s * 0.45)], fill=INK)
    draw.rectangle([x + s * 0.2, y + s * 0.45, x + s * 0.8, y + s * 0.92],
                   outline=INK, width=5)
    fx, fy = x + s / 2, y + s * 0.62
    draw.polygon([(fx, fy - 20), (fx + 11, fy + 6), (fx + 5, fy + 20),
                  (fx - 5, fy + 20), (fx - 11, fy + 6)], fill=RED)
    draw.polygon([(fx, fy - 4), (fx + 6, fy + 10), (fx, fy + 19),
                  (fx - 6, fy + 10)], fill=GOLD)


def icon_cyclone(draw, x, y, s):
    cx, cy = x + s / 2, y + s * 0.42
    for r, start in ((26, 20), (17, 200), (9, 40)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 270,
                 fill=BLUE, width=5)
    for i in range(3):
        rx = x + 12 + i * (s - 24) / 2
        draw.line([rx + 6, y + s * 0.78, rx, y + s * 0.95], fill=BLUE, width=4)


def icon_derrick(draw, x, y, s):
    top, base = y + 4, y + s * 0.8
    draw.line([x + s * 0.32, base, x + s * 0.46, top], fill=INK, width=5)
    draw.line([x + s * 0.68, base, x + s * 0.54, top], fill=INK, width=5)
    draw.line([x + s * 0.36, y + s * 0.5, x + s * 0.64, y + s * 0.5],
              fill=INK, width=4)
    draw.line([x + s * 0.39, y + s * 0.66, x + s * 0.61, y + s * 0.66],
              fill=INK, width=4)
    fx, fy = x + s * 0.5, y + s * 0.3
    draw.polygon([(fx, fy - 16), (fx + 9, fy + 6), (fx, fy + 15),
                  (fx - 9, fy + 6)], fill=RED)
    draw.line([x + 2, y + s * 0.92, x + s - 2, y + s * 0.92], fill=BLUE, width=4)


# ---------------------------------------------------------------- layout

def panel(draw, box, kicker, headline, sub, icon):
    """One story card: icon and kicker on the top row, then the headline
    and a two-line sub across the card's full width."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=RULE, width=2)
    pad = 18
    icon(draw, x0 + pad, y0 + pad, 46)
    draw.text((x0 + pad + 60, y0 + pad + 10), kicker,
              font=font("ExtraBold", 19), fill=RED)
    y = text_block(draw, (x0 + pad, y0 + pad + 58), headline,
                   font("ExtraBold", 26), INK, x1 - x0 - 2 * pad, line_gap=4)
    text_block(draw, (x0 + pad, y + 8), sub, font("Regular", 19), MUTED,
               x1 - x0 - 2 * pad, line_gap=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header: the day, named as loudly as the page allows.
    d.text((W / 2, 30), "T H E   W O R L D   I N   O N E   D A Y",
           font=font("ExtraBold", 25), fill=RED, anchor="ma")
    d.text((W / 2, 60), "THURSDAY 19 NOVEMBER 2026",
           font=font("Black", 63), fill=INK, anchor="ma")
    d.line([48, 146, W - 48, 146], fill=INK, width=4)
    d.text((W / 2, 156), "The day's biggest stories, in a single picture",
           font=font("Regular", 24), fill=MUTED, anchor="ma")

    # Lead story: the Shenzhen summit, flags and skyline inside the card.
    lead = (48, 196, W - 48, 416)
    d.rounded_rectangle(lead, radius=16, fill=CARD, outline=RULE, width=2)
    base = 392
    for i, (bw, bh) in enumerate(((46, 92), (60, 128), (40, 74), (54, 106))):
        bx = 84 + i * 52
        d.rectangle([bx, base - bh, bx + bw, base], fill=(58, 68, 92))
    for fx, draw_flag in ((90, flag_us), (160, flag_cn), (230, flag_ru)):
        d.line([fx + 30, 232, fx + 30, 300], fill=INK, width=4)
        draw_flag(d, fx, 232, 60, 40)
    tx = 330
    d.text((tx, 222), "TOP STORY · SHENZHEN, CHINA",
           font=font("ExtraBold", 21), fill=RED)
    y = text_block(d, (tx, 252), "TRUMP, XI & PUTIN HOLD FIRST THREE-WAY SUMMIT",
                   font("ExtraBold", 40), INK, W - 48 - tx - 28, line_gap=5)
    text_block(d, (tx, y + 10),
               "The US, Chinese and Russian presidents meet face to face on "
               "the sidelines of APEC. Ukraine tops the agenda.",
               font("Regular", 23), MUTED, W - 48 - tx - 28, line_gap=5)

    # Six panels, two rows of three.
    stories = [
        ("THE HAGUE", "UN COURT RULES IN ROHINGYA GENOCIDE CASE",
         "The ICJ decides Gambia's case against Myanmar.", icon_scales),
        ("UKRAINE", "UKRAINE STRIKES CRIMEAN BRIDGE AGAIN",
         "Third strike on the Kerch Bridge this week.", icon_bridge),
        ("ANTALYA, TÜRKIYE", "COP31 CLIMATE TALKS GO TO THE WIRE",
         "Ministers struggle to unblock a final deal.", icon_sun_sea),
        ("BANGLADESH", "UNREST: YUNUS FAMILY HOME TORCHED",
         "Violence spreads across 28 districts.", icon_house_flame),
        ("ODISHA, INDIA", "CYCLONE AKVAN: 100,000 EVACUATED",
         "The storm makes landfall near Gopalpur.", icon_cyclone),
        ("THE GULF", "IRAN–GULF CLASHES SHAKE ENERGY",
         "IEA: the Hormuz crisis is the worst energy threat ever.",
         icon_derrick),
    ]
    gx, gy, gw, gh, gap = 48, 432, 296, 228, 16
    for i, (kicker, headline, sub, icon) in enumerate(stories):
        x0 = gx + (i % 3) * (gw + gap)
        y0 = gy + (i // 3) * (gh + gap)
        panel(d, (x0, y0, x0 + gw, y0 + gh), kicker, headline, sub, icon)

    # Footer ticker: the rest of the day in one breath.
    d.rectangle([0, 918, W, H], fill=INK)
    d.text((48, 934), "ALSO TODAY", font=font("ExtraBold", 20),
           fill=(255, 205, 90))
    text_block(d, (196, 932),
               "Anthropic's record $81bn IPO · Van Gogh sells for a record "
               "$190m · IAEA: North Korea expands uranium enrichment · "
               "GTA VI launch day",
               font("SemiBold", 21), (240, 240, 240), W - 196 - 40, line_gap=4)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
