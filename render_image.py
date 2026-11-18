#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261118 (v2).

A real newspaper front page summing up the world news of Wednesday
18 November 2026, in the style of a broadsheet front page (masthead,
full-width lead headline, varied multi-column grid below).

PHOTOS ARE REAL, freely licensed, verified against their source pages:
  lead_carrier.jpg  - US Navy ships in formation, RIMPAC 2026
                      (US Navy photo, public domain)
  bridge_collapse.jpg - Crimean Bridge after the 17 Nov 2026 strikes
                      (Security Service of Ukraine, CC BY 4.0)
  cop31.jpg         - COP31, Chris Bowen & Dan Jorgensen, Antalya 10 Nov 2026
                      (European Union / EC Audiovisual Service, CC BY 4.0)
  gaza_tents.jpg    - Flooded tents, Deir el-Balah, Gaza, Jan 2025
                      (UNRWA / Ashraf Amra, CC BY-SA 3.0 IGO)
The Diplomacy story is text-only: no freely licensed photo of the
17 Nov Manila Quad meeting was available in time (the group photo
is AP-copyrighted; Wikimedia had not indexed a White House photo yet).
Photos are cropped to fill their frames (no distortion); text sits on
plain paper, never on top of a photo.
Output: entry.png beside this file (1024x1024 PNG, <= 1 MiB).
No network, deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1024
MARGIN = 28

PAPER = (250, 246, 236)      # warm newsprint
INK = (26, 26, 26)           # near-black
NAVY = (22, 35, 63)          # masthead / headlines
GRAY = (85, 85, 85)
LIGHT_RULE = (200, 192, 175)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
OLIVE = (77, 124, 15)
BURGUNDY = (157, 23, 77)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")


def font(path, size):
    return ImageFont.truetype(path, size)


def italic(size):
    if os.path.exists(SERIF_ITALIC):
        return ImageFont.truetype(SERIF_ITALIC, size)
    return ImageFont.truetype(SANS_ITALIC, size)


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


def draw_text_block(d, x, y, text, fnt, max_w, lh, fill):
    """Draw wrapped text; returns the y just below the last line."""
    for ln in wrap(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def place_photo(img, path, x, y, w, h):
    """Crop-to-fill a real photo into its frame, thin navy border."""
    im = Image.open(os.path.join(PHOTOS, path)).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.5))
    img.paste(im, (x, y))
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)


def caption(d, x, y, text, max_w, size=11):
    """Small grey caption, wrapped; returns y below it."""
    fnt = font(SANS, size)
    return draw_text_block(d, x, y, text, fnt, max_w, size + 2, GRAY)


def kicker(d, x, y, text, color, size=15):
    fnt = font(SANS_BOLD, size)
    d.text((x, y), text, font=fnt, fill=color)
    return y + size + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    f_mast = font(SERIF_BOLD, 54)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 14), t, font=f_mast,
           fill=(255, 255, 255))
    f_sub = font(SANS, 15)
    s = "WORLD NEWS  ·  SUMMED UP IN A SINGLE IMAGE"
    d.text(((W - d.textlength(s, font=f_sub)) / 2, 72), s, font=f_sub,
           fill=(201, 210, 224))

    # ---- date strip ----------------------------------------------------
    f_date = font(SANS_BOLD, 26)
    dt = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 104), dt, font=f_date,
           fill=NAVY)
    d.line([(0, 138), (W, 138)], fill=INK, width=3)
    d.line([(0, 143), (W, 143)], fill=INK, width=1)

    # ---- lead story ----------------------------------------------------
    f_tag = font(SANS_BOLD, 17)
    tag = "MIDDLE EAST"
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([MARGIN, 152, MARGIN + tw + 22, 152 + 30], fill=BURGUNDY)
    d.text((MARGIN + 11, 157), tag, font=f_tag, fill=(255, 255, 255))

    f_head = font(SANS_BOLD, 40)
    head = "US–Iran tit-for-tat in Hormuz: Qeshm struck, tankers burn"
    y = 190
    for ln in wrap(d, head, f_head, W - 2 * MARGIN):
        d.text((MARGIN, y), ln, font=f_head, fill=NAVY)
        y += 48

    # lead body, left column
    f_body = font(SANS, 19)
    body = ("US forces hit an IRGC missile site on Qeshm Island after Iran's "
            "drones targeted the US radar in Bahrain and were intercepted. "
            "Tanker Tara Gas was hit twice; her crew evacuated, one seafarer "
            "unaccounted for. A third US carrier has arrived.")
    yb = draw_text_block(d, MARGIN, 294, body, f_body, 468, 26, (51, 51, 51))
    quote = ("Trump says he is 'looking into' unverified reports of an "
             "Iranian dirty-bomb plot.")
    draw_text_block(d, MARGIN, yb + 14, quote, italic(18), 468, 24, INK)

    # lead photo, right
    place_photo(img, "lead_carrier.jpg", 520, 294, 476, 206)
    caption(d, 520, 506,
            "US Navy ships sail in formation during RIMPAC 2026 (US Navy photo)",
            476)

    # ---- double rule ---------------------------------------------------
    d.line([(0, 534), (W, 534)], fill=INK, width=3)
    d.line([(0, 539), (W, 539)], fill=INK, width=1)

    # ---- row 1: Ukraine (photo) + Diplomacy (text-only) ---------------
    # Ukraine, left wide column
    y = 548
    y = kicker(d, MARGIN, y, "UKRAINE", RED)
    f_h1 = font(SANS_BOLD, 26)
    d.text((MARGIN, y), "Ukraine cripples Crimea bridge a second day",
           font=f_h1, fill=INK)
    place_photo(img, "bridge_collapse.jpg", MARGIN, 606, 312, 146)
    caption(d, MARGIN, 758,
            "The Crimean Bridge after the 17 Nov. strikes (SBU, CC BY 4.0)",
            312, size=10)
    f_b1 = font(SANS, 17)
    draw_text_block(d, 356, 606,
                    "The main road arch crumbled into the sea; 2 killed, "
                    "traffic halted. Russia claims a record 1,441 drones "
                    "downed; Moscow hit Kyiv's bridges in reply.",
                    f_b1, 264, 22, GRAY)
    # vertical divider
    d.line([(632, 548), (632, 776)], fill=LIGHT_RULE, width=1)

    # Diplomacy, right narrow column, text-only
    y = 548
    y = kicker(d, 648, y, "DIPLOMACY", BLUE)
    f_h2 = font(SANS_BOLD, 24)
    y = draw_text_block(d, 648, y,
                        "Trump in Manila for Quad talks, ahead of China visit",
                        f_h2, 348, 29, INK)
    draw_text_block(d, 648, y + 8,
                    "Trump opened his Asia trip with the first Quad leaders' "
                    "meeting in two years. Xi calls for free and open trade "
                    "at APEC in Shenzhen; Putin landed overnight. The three "
                    "meet Thursday to talk Iran and Ukraine.",
                    f_b1, 348, 22, GRAY)
    # Thursday box
    d.rectangle([648, 752, 996, 776], outline=NAVY, width=1)
    f_box = font(SANS_BOLD, 14)
    bx = "THURSDAY: Trump, Xi and Putin meet in Shenzhen"
    d.text((648 + (348 - d.textlength(bx, font=f_box)) / 2, 758), bx,
           font=f_box, fill=NAVY)

    # ---- rule ----------------------------------------------------------
    d.line([(0, 786), (W, 786)], fill=INK, width=2)

    # ---- row 2: Gaza + COP31, horizontal strips ------------------------
    # Gaza, left
    y = 794
    place_photo(img, "gaza_tents.jpg", MARGIN, 794, 158, 110)
    caption(d, MARGIN, 908,
            "Flooded tents, Deir el-Balah, Jan. 2025 (UNRWA)",
            158, size=10)
    kicker(d, 202, y, "GAZA", OLIVE, size=14)
    f_h3 = font(SANS_BOLD, 20)
    yy = draw_text_block(d, 202, 812,
                         "Gaza: UN warns of deaths from the cold",
                         f_h3, 310, 24, INK)
    draw_text_block(d, 202, yy + 4,
                    "About 1.7m displaced; Australia, Canada, Italy and the "
                    "UK urge aid access. Strikes continue despite the "
                    "ceasefire.",
                    font(SANS, 16), 310, 20, GRAY)
    # vertical divider
    d.line([(520, 794), (520, 938)], fill=LIGHT_RULE, width=1)

    # COP31, right
    place_photo(img, "cop31.jpg", 536, 794, 158, 110)
    caption(d, 536, 908,
            "Bowen (left) and Jorgensen, Antalya (EU, CC BY 4.0)",
            158, size=10)
    kicker(d, 710, y, "CLIMATE", TEAL, size=14)
    yy = draw_text_block(d, 710, 812,
                         "COP31: draft deal still split",
                         f_h3, 286, 24, INK)
    draw_text_block(d, 710, yy + 4,
                    "Antalya talks close Friday. Heat and cooling roadmap "
                    "backed; ocean measures make the draft text.",
                    font(SANS, 16), 286, 20, GRAY)

    # ---- footer: also strip + sources ----------------------------------
    d.line([(0, 948), (W, 948)], fill=INK, width=2)
    f_also_tag = font(SANS_BOLD, 16)
    f_also = font(SANS, 16)
    d.text((MARGIN, 956), "ALSO", font=f_also_tag, fill=RED)
    draw_text_block(d, MARGIN + 58, 956,
                    "Russian An-12 military plane crashes in Siberia — 19 "
                    "dead. Nvidia Q3 revenue $115.8bn, first earnings without "
                    "Jensen Huang, guides $130bn.",
                    f_also, W - MARGIN - (MARGIN + 58), 21, (51, 51, 51))
    f_src = font(SANS, 13)
    src = ("Sources: Reuters  ·  RFE/RL  ·  UN News  ·  CNN  ·  Al Jazeera  "
           "—  18 November 2026")
    d.text(((W - d.textlength(src, font=f_src)) / 2, 1004), src, font=f_src,
           fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
