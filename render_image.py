#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261118.

Draws a 1024x1024 newspaper front page summing up the world news of
Wednesday 18 November 2026, using only PIL. No network, no AI generation:
every glyph is placed by this script so the text is exact and legible.
One flat illustration per story, each drawn proportionally to its panel
so nothing spills past its bounds.
Output: entry.png beside this file (1024x1024 PNG, <= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

PAPER = (250, 246, 236)      # warm newsprint
INK = (26, 26, 26)           # near-black
NAVY = (22, 35, 63)          # masthead / headlines
GRAY = (85, 85, 85)
LIGHT_RULE = (200, 192, 175)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
BURGUNDY = (157, 23, 77)
TEAL = (15, 118, 110)
OLIVE = (77, 124, 15)
ORANGE = (232, 89, 12)
SKY = (188, 214, 232)
SEA = (47, 110, 142)
SUN = (242, 201, 76)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_burning_tanker(draw, x0, y0, w, h):
    """Oil tanker on fire in the Strait of Hormuz — the lead panel."""
    sea_y = y0 + int(0.38 * h)
    draw.rectangle([x0, y0, x0 + w, sea_y], fill=SKY)
    draw.rectangle([x0, sea_y, x0 + w, y0 + h], fill=SEA)
    # sun and a cloud
    draw.ellipse([x0 + int(0.06 * w), y0 + int(0.06 * h),
                  x0 + int(0.15 * w), y0 + int(0.15 * h)], fill=SUN)
    draw.ellipse([x0 + int(0.68 * w), y0 + int(0.08 * h),
                  x0 + int(0.92 * w), y0 + int(0.16 * h)], fill=(255, 255, 255))
    # waves
    for wy in (sea_y + int(0.22 * h), sea_y + int(0.42 * h)):
        for wx in range(x0 + 8, x0 + w - 20, 44):
            draw.arc([wx, wy, wx + 36, wy + 14], 180, 360,
                     fill=(255, 255, 255), width=2)
    deck_y = y0 + int(0.46 * h)
    # hull, bow to the right
    draw.polygon([(x0 + int(0.04 * w), deck_y),
                  (x0 + int(0.82 * w), deck_y),
                  (x0 + int(0.96 * w), deck_y + int(0.10 * h)),
                  (x0 + int(0.04 * w), deck_y + int(0.10 * h))],
                 fill=(43, 43, 43))
    # burgundy stripe along the hull
    draw.polygon([(x0 + int(0.04 * w), deck_y + int(0.03 * h)),
                  (x0 + int(0.82 * w), deck_y + int(0.03 * h)),
                  (x0 + int(0.86 * w), deck_y + int(0.06 * h)),
                  (x0 + int(0.04 * w), deck_y + int(0.06 * h))],
                 fill=BURGUNDY)
    # superstructure at the stern (left) and funnel
    draw.rectangle([x0 + int(0.08 * w), deck_y - int(0.14 * h),
                    x0 + int(0.22 * w), deck_y], fill=(255, 255, 255))
    draw.rectangle([x0 + int(0.08 * w), deck_y - int(0.14 * h),
                    x0 + int(0.22 * w), deck_y - int(0.11 * h)], fill=BURGUNDY)
    draw.rectangle([x0 + int(0.26 * w), deck_y - int(0.17 * h),
                    x0 + int(0.31 * w), deck_y], fill=(58, 58, 58))
    # deck containers
    draw.rectangle([x0 + int(0.66 * w), deck_y - int(0.07 * h),
                    x0 + int(0.80 * w), deck_y], fill=(90, 90, 90))
    # flames rising from the mid-deck
    fx0, fx1 = x0 + int(0.40 * w), x0 + int(0.60 * w)
    draw.polygon([(fx0, deck_y), (fx0 + int(0.05 * w), deck_y - int(0.26 * h)),
                  (fx0 + int(0.10 * w), deck_y - int(0.10 * h)),
                  (fx0 + int(0.14 * w), deck_y - int(0.30 * h)),
                  (fx0 + int(0.18 * w), deck_y - int(0.08 * h)),
                  (fx1, deck_y)], fill=ORANGE)
    draw.polygon([(fx0 + int(0.04 * w), deck_y),
                  (fx0 + int(0.08 * w), deck_y - int(0.18 * h)),
                  (fx0 + int(0.12 * w), deck_y - int(0.06 * h)),
                  (fx0 + int(0.15 * w), deck_y - int(0.20 * h)),
                  (fx0 + int(0.17 * w), deck_y)], fill=RED)
    draw.polygon([(fx0 + int(0.07 * w), deck_y),
                  (fx0 + int(0.10 * w), deck_y - int(0.11 * h)),
                  (fx0 + int(0.13 * w), deck_y)], fill=SUN)
    # black smoke drifting right
    for sx, sy, sr in ((0.48, 0.10, 0.05), (0.56, 0.05, 0.06),
                       (0.66, 0.09, 0.05), (0.74, 0.04, 0.04)):
        draw.ellipse([x0 + int(sx * w), y0 + int(sy * h),
                      x0 + int((sx + sr) * w), y0 + int((sy + sr * 0.8) * h)],
                     fill=(70, 70, 70))
    # burning patch on the water
    draw.ellipse([x0 + int(0.52 * w), sea_y + int(0.30 * h),
                  x0 + int(0.72 * w), sea_y + int(0.38 * h)], fill=ORANGE)
    draw.ellipse([x0 + int(0.57 * w), sea_y + int(0.32 * h),
                  x0 + int(0.67 * w), sea_y + int(0.36 * h)], fill=(255, 220, 90))
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_bridge(draw, x0, y0, w, h):
    """Suspension bridge with a collapsed middle span — Crimea bridge.

    All coordinates are fractions of the panel size, so the same drawing
    works as a large lead panel or a small thumbnail.
    """
    sea_y = y0 + int(0.58 * h)
    deck_y = y0 + int(0.44 * h)
    draw.rectangle([x0, y0, x0 + w, sea_y], fill=SKY)
    draw.rectangle([x0, sea_y, x0 + w, y0 + h], fill=SEA)
    # sun
    draw.ellipse([x0 + int(0.08 * w), y0 + int(0.07 * h),
                  x0 + int(0.18 * w), y0 + int(0.17 * h)], fill=SUN)
    # waves
    for wy in (sea_y + int(0.10 * h), sea_y + int(0.24 * h)):
        for wx in range(x0 + 4, x0 + w - 10, 22):
            draw.arc([wx, wy, wx + 18, wy + 7], 180, 360,
                     fill=(255, 255, 255), width=2)
    # towers
    for tx in (int(0.28 * w), int(0.66 * w)):
        draw.rectangle([x0 + tx, y0 + int(0.12 * h),
                        x0 + tx + int(0.04 * w), deck_y], fill=(58, 58, 58))
    # cables
    for tx in (int(0.30 * w), int(0.68 * w)):
        draw.line([(x0 + tx, y0 + int(0.12 * h)), (x0 + int(0.02 * w), deck_y)],
                  fill=(90, 90, 90), width=2)
        draw.line([(x0 + tx, y0 + int(0.12 * h)), (x0 + int(0.98 * w), deck_y)],
                  fill=(90, 90, 90), width=2)
    # deck segments (gap in the middle: the collapsed span)
    draw.rectangle([x0 + int(0.02 * w), deck_y,
                    x0 + int(0.42 * w), deck_y + int(0.03 * h)], fill=(43, 43, 43))
    draw.rectangle([x0 + int(0.58 * w), deck_y,
                    x0 + int(0.98 * w), deck_y + int(0.03 * h)], fill=(43, 43, 43))
    # fallen span, tilted into the sea
    draw.polygon([(x0 + int(0.42 * w), deck_y),
                  (x0 + int(0.56 * w), deck_y + int(0.01 * h)),
                  (x0 + int(0.53 * w), deck_y + int(0.10 * h)),
                  (x0 + int(0.40 * w), deck_y + int(0.08 * h))],
                 fill=(43, 43, 43))
    # debris in the water
    for dx, dy in ((0.46, 0.62), (0.52, 0.66), (0.44, 0.68)):
        draw.rectangle([x0 + int(dx * w), y0 + int(dy * h),
                        x0 + int(dx * w) + 5, y0 + int(dy * h) + 2],
                       fill=(43, 43, 43))
    # smoke + flame at the break
    draw.ellipse([x0 + int(0.44 * w), deck_y - int(0.11 * h),
                  x0 + int(0.51 * w), deck_y - int(0.03 * h)], fill=(154, 165, 177))
    draw.ellipse([x0 + int(0.48 * w), deck_y - int(0.15 * h),
                  x0 + int(0.54 * w), deck_y - int(0.08 * h)], fill=(170, 180, 190))
    draw.polygon([(x0 + int(0.48 * w), deck_y),
                  (x0 + int(0.50 * w), deck_y - int(0.06 * h)),
                  (x0 + int(0.53 * w), deck_y)], fill=ORANGE)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_flags(draw, x0, y0, w, h):
    """Three small flags (US, China, Russia) on poles — trilateral talks."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    draw.rectangle([x0, y0 + h - 8, x0 + w, y0 + h], fill=(226, 220, 205))
    for px in (x0 + 10, x0 + 40, x0 + 70):
        draw.rectangle([px, y0 + 12, px + 2, y0 + h - 8], fill=(58, 58, 58))
        draw.ellipse([px - 2, y0 + 8, px + 4, y0 + 14], fill=SUN)
    fy, fw, fh = y0 + 12, 20, 15
    # US flag: stripes + blue canton
    fx = x0 + 14
    for i in range(5):
        draw.rectangle([fx, fy + i * 3, fx + fw, fy + i * 3 + 3],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, fy, fx + 10, fy + 8], fill=BLUE)
    for dx, dy in ((2, 2), (6, 2), (2, 5), (6, 5)):
        draw.ellipse([fx + dx, fy + dy, fx + dx + 1, fy + dy + 1],
                     fill=(255, 255, 255))
    # China flag: red field, yellow stars
    fx = x0 + 44
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    draw.ellipse([fx + 3, fy + 3, fx + 7, fy + 7], fill=(255, 222, 89))
    for dx, dy in ((12, 2), (16, 5), (12, 9), (17, 9)):
        draw.ellipse([fx + dx, fy + dy, fx + dx + 2, fy + dy + 2],
                     fill=(255, 222, 89))
    # Russia flag: white / blue / red bands
    fx = x0 + 74
    for i, c in enumerate(((255, 255, 255), BLUE, (222, 41, 16))):
        draw.rectangle([fx, fy + i * 5, fx + fw, fy + i * 5 + 5], fill=c)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_tent(draw, x0, y0, w, h):
    """A shelter tent in falling snow — Gaza's cold."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(203, 222, 236))
    # pale moon
    draw.ellipse([x0 + int(0.72 * w), y0 + int(0.08 * h),
                  x0 + int(0.86 * w), y0 + int(0.22 * h)], fill=(240, 240, 230))
    # snowy ground
    draw.rectangle([x0, y0 + int(0.68 * h), x0 + w, y0 + h], fill=(238, 240, 243))
    # tent: khaki triangle with a dark door
    draw.polygon([(x0 + int(0.50 * w), y0 + int(0.28 * h)),
                  (x0 + int(0.10 * w), y0 + int(0.74 * h)),
                  (x0 + int(0.90 * w), y0 + int(0.74 * h))],
                 fill=(176, 141, 87))
    draw.polygon([(x0 + int(0.50 * w), y0 + int(0.74 * h)),
                  (x0 + int(0.38 * w), y0 + int(0.74 * h)),
                  (x0 + int(0.50 * w), y0 + int(0.48 * h))],
                 fill=(101, 67, 33))
    draw.line([(x0 + int(0.50 * w), y0 + int(0.28 * h)),
               (x0 + int(0.50 * w), y0 + int(0.48 * h))],
              fill=(140, 110, 65), width=2)
    # snowflakes: small white asterisks
    for sx, sy in ((0.16, 0.18), (0.30, 0.10), (0.62, 0.14),
                   (0.84, 0.40), (0.12, 0.44), (0.70, 0.60)):
        cx, cy = x0 + int(sx * w), y0 + int(sy * h)
        for dx, dy in ((0, -4), (0, 4), (-4, 0), (4, 0), (-3, -3), (3, 3)):
            draw.line([(cx, cy), (cx + dx, cy + dy)],
                      fill=(255, 255, 255), width=1)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def draw_globe(draw, x0, y0, w, h):
    """A warming globe under a hot sun — COP31 climate talks."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    # sun
    draw.ellipse([x0 + int(0.70 * w), y0 + int(0.07 * h),
                  x0 + int(0.88 * w), y0 + int(0.25 * h)], fill=SUN)
    for ang in range(0, 360, 45):
        import math
        cx, cy = x0 + int(0.79 * w), y0 + int(0.16 * h)
        r1, r2 = int(0.11 * w), int(0.15 * w)
        x1 = cx + int(r1 * math.cos(math.radians(ang)))
        y1 = cy + int(r1 * math.sin(math.radians(ang)))
        x2 = cx + int(r2 * math.cos(math.radians(ang)))
        y2 = cy + int(r2 * math.sin(math.radians(ang)))
        draw.line([(x1, y1), (x2, y2)], fill=SUN, width=2)
    # globe
    gx, gy, gr = x0 + int(0.46 * w), y0 + int(0.56 * h), int(0.30 * w)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=SEA)
    # land blobs
    draw.ellipse([gx - int(0.22 * w), gy - int(0.20 * h),
                  gx - int(0.02 * w), gy - int(0.02 * h)], fill=OLIVE)
    draw.ellipse([gx + int(0.02 * w), gy + int(0.02 * h),
                  gx + int(0.24 * w), gy + int(0.20 * h)], fill=OLIVE)
    draw.ellipse([gx - int(0.06 * w), gy + int(0.12 * h),
                  gx + int(0.10 * w), gy + int(0.24 * h)], fill=(111, 148, 45))
    # clouds over the globe
    draw.arc([gx - int(0.26 * w), gy - int(0.08 * h),
              gx + int(0.10 * w), gy + int(0.06 * h)], 180, 360,
             fill=(255, 255, 255), width=2)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 110], fill=NAVY)
    f_mast = font(SERIF_BOLD, 56)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 20), t, font=f_mast,
           fill=(255, 255, 255))
    f_sub = font(SANS, 16)
    s = "WORLD NEWS  ·  SUMMED UP IN A SINGLE IMAGE"
    d.text(((W - d.textlength(s, font=f_sub)) / 2, 82), s, font=f_sub,
           fill=(201, 210, 224))

    # ---- date strip ----------------------------------------------------
    f_date = font(SANS_BOLD, 27)
    dt = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 120), dt, font=f_date,
           fill=NAVY)
    d.line([(0, 152), (W, 152)], fill=INK, width=3)
    d.line([(0, 157), (W, 157)], fill=INK, width=1)

    # ---- lead story ----------------------------------------------------
    f_tag = font(SANS_BOLD, 17)
    tag = "MIDDLE EAST"
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([MARGIN, 172, MARGIN + tw + 22, 172 + 30], fill=BURGUNDY)
    d.text((MARGIN + 11, 177), tag, font=f_tag, fill=(255, 255, 255))

    f_head = font(SANS_BOLD, 38)
    head = "US–Iran tit-for-tat in Hormuz: Qeshm struck, tankers burn"
    lines = wrap(d, head, f_head, 600)
    y = 212
    for ln in lines:
        d.text((MARGIN, y), ln, font=f_head, fill=NAVY)
        y += 46

    f_sum = font(SANS, 20)
    summ = ("US hit an IRGC missile site on Qeshm; Iran's drones on Bahrain's "
            "US radar were intercepted. Tanker Tara Gas evacuated, one crew "
            "unaccounted; a third US carrier arrived. Trump is 'looking into' "
            "unverified dirty-bomb reports.")
    for ln in wrap(d, summ, f_sum, 600):
        d.text((MARGIN, y), ln, font=f_sum, fill=(51, 51, 51))
        y += 27

    # burning tanker illustration, right of the lead text
    draw_burning_tanker(d, 664, 168, 324, 260)

    # ---- double rule ---------------------------------------------------
    d.line([(0, 444), (W, 444)], fill=INK, width=3)
    d.line([(0, 449), (W, 449)], fill=INK, width=1)

    # ---- supporting stories --------------------------------------------
    stories = [
        ("UKRAINE", RED, draw_bridge,
         "Ukraine cripples Crimea bridge a second day",
         "Main road arch crumbles into the sea; 2 killed, traffic halted. "
         "Russia claims a record 1,441 drones downed; Moscow hits Kyiv's "
         "bridges in reply."),
        ("DIPLOMACY", BLUE, draw_flags,
         "Trump in Manila for Quad talks, ahead of China visit",
         "Xi calls for free and open trade at APEC; Putin lands overnight. "
         "The three meet Thursday to talk Iran and Ukraine."),
        ("GAZA", OLIVE, draw_tent,
         "Gaza: UN warns of deaths from the cold",
         "About 1.7m displaced; Australia, Canada, Italy and the UK urge "
         "aid access. Strikes continue despite the ceasefire."),
        ("CLIMATE", TEAL, draw_globe,
         "COP31 Antalya: draft deal still split as talks close Friday",
         "Heat and cooling roadmap backed; ocean measures make the draft text."),
    ]
    f_stag = font(SANS_BOLD, 15)
    f_sh = font(SANS_BOLD, 22)
    f_ss = font(SANS, 17)
    THUMB_W, THUMB_H = 96, 96
    THUMB_X = W - MARGIN - THUMB_W
    TEXT_W = THUMB_X - 12 - (MARGIN + 24)
    ROW_H = 120
    y = 464
    for i, (tag, color, illus, head, summ) in enumerate(stories):
        d.rectangle([MARGIN, y, MARGIN + 8, y + 96], fill=color)
        d.text((MARGIN + 24, y), tag, font=f_stag, fill=color)
        hy = y + 21
        for ln in wrap(d, head, f_sh, TEXT_W):
            d.text((MARGIN + 24, hy), ln, font=f_sh, fill=INK)
            hy += 26
        for ln in wrap(d, summ, f_ss, TEXT_W):
            d.text((MARGIN + 24, hy), ln, font=f_ss, fill=GRAY)
            hy += 21
        # thumbnail: render on a temp image so nothing can spill past
        # the panel bounds, then paste it into the row
        thumb = Image.new("RGB", (THUMB_W, THUMB_H), PAPER)
        td = ImageDraw.Draw(thumb)
        illus(td, 0, 0, THUMB_W, THUMB_H)
        img.paste(thumb, (THUMB_X, y + 12))
        if i < len(stories) - 1:
            d.line([(MARGIN, y + ROW_H - 12), (W - MARGIN, y + ROW_H - 12)],
                   fill=LIGHT_RULE, width=1)
        y += ROW_H

    # ---- footer: also strip + sources ----------------------------------
    d.line([(0, 944), (W, 944)], fill=INK, width=2)
    f_also_tag = font(SANS_BOLD, 16)
    f_also = font(SANS, 16)
    also = ("Russian An-12 military plane crashes in Siberia — 19 dead. "
            "Nvidia Q3 revenue $115.8bn, first earnings without Jensen Huang, "
            "guides $130bn.")
    d.text((MARGIN, 954), "ALSO", font=f_also_tag, fill=RED)
    ax = MARGIN + 58
    ay = 954
    for ln in wrap(d, also, f_also, W - MARGIN - ax):
        d.text((ax, ay), ln, font=f_also, fill=(51, 51, 51))
        ay += 21
    f_src = font(SANS, 14)
    src = "Sources: Reuters  ·  RFE/RL  ·  UN News  ·  CNN  ·  Al Jazeera  —  18 November 2026"
    d.text(((W - d.textlength(src, font=f_src)) / 2, 1000), src, font=f_src,
           fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
