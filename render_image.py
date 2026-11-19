#!/usr/bin/env python3
"""Render the entry image for make.fun news-image-20261118 (v3).

A real newspaper front page summing up the world news of Wednesday
18 November 2026, in the style of a broadsheet front page (masthead,
full-width lead headline, varied multi-column grid below).

v3: same stories, same text and same broadsheet layout as v2, but MORE
real photos -- every main story now has one. The Diplomacy story gains
a real photo (the Quad leaders in Manila); the layout is tightened
(shorter lead photo, smaller Diplomacy body type) to fit it in.
Positions below the lead are computed from the content (flow-based),
so nothing overlaps.

PHOTOS ARE REAL, freely licensed, verified against their source pages:
  lead_carrier.jpg  - US Navy ships in formation, RIMPAC 2026
                      (US Navy photo, public domain)
  bridge_collapse.jpg - Crimean Bridge after the 17 Nov 2026 strikes
                      (Security Service of Ukraine, CC BY 4.0)
  quad_manila.jpg   - Quad leaders (Takaichi, Modi, Trump, Albanese)
                      pose in Manila, 17 Nov 2026. Still from the
                      White House video "President Trump Greets Quad
                      Leaders and Participates in a Photo Opportunity"
                      (The White House, public domain); the video's
                      lower-third banner was cropped out, nothing
                      else altered.
                      Source: https://commons.wikimedia.org/wiki/File:President_Trump_Greets_Quad_Leaders_and_Participates_in_a_Photo_Opportunity.webm
  cop31.jpg         - COP31, Chris Bowen & Dan Jorgensen, Antalya 10 Nov 2026
                      (European Union / EC Audiovisual Service, CC BY 4.0)
  gaza_tents.jpg    - Flooded tents, Deir el-Balah, Gaza, Jan 2025
                      (UNRWA / Ashraf Amra, CC BY-SA 3.0 IGO)
The ALSO strip stays text-only by design.
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

    # lead body, left column (slightly tighter than v2 to make room below)
    f_body = font(SANS, 18)
    body = ("US forces hit an IRGC missile site on Qeshm Island after Iran's "
            "drones targeted the US radar in Bahrain and were intercepted. "
            "Tanker Tara Gas was hit twice; her crew evacuated, one seafarer "
            "unaccounted for. A third US carrier has arrived.")
    yb = draw_text_block(d, MARGIN, 294, body, f_body, 468, 25, (51, 51, 51))
    quote = ("Trump says he is 'looking into' unverified reports of an "
             "Iranian dirty-bomb plot.")
    yq = draw_text_block(d, MARGIN, yb + 14, quote, italic(17), 468, 23, INK)

    # lead photo, right (shorter than v2)
    place_photo(img, "lead_carrier.jpg", 520, 294, 476, 175)
    cap_end = caption(d, 520, 475,
                      "US Navy ships sail in formation during RIMPAC 2026 (US Navy photo)",
                      476)

    # ---- double rule (below whichever lead element ends lower) --------
    lead_bottom = max(yq, cap_end)
    rule_y = lead_bottom + 24
    d.line([(0, rule_y), (W, rule_y)], fill=INK, width=3)
    d.line([(0, rule_y + 5), (W, rule_y + 5)], fill=INK, width=1)

    # ---- row 1: Ukraine (photo) + Diplomacy (photo, new in v3) --------
    y0 = rule_y + 13
    # Ukraine, left wide column
    y = y0
    y = kicker(d, MARGIN, y, "UKRAINE", RED)
    f_h1 = font(SANS_BOLD, 26)
    d.text((MARGIN, y), "Ukraine cripples Crimea bridge a second day",
           font=f_h1, fill=INK)
    place_photo(img, "bridge_collapse.jpg", MARGIN, y0 + 53, 312, 146)
    uk_cap = caption(d, MARGIN, y0 + 53 + 146 + 6,
                     "The Crimean Bridge after the 17 Nov. strikes (SBU, CC BY 4.0)",
                     312, size=10)
    f_b1 = font(SANS, 17)
    uk_body = draw_text_block(d, 356, y0 + 53,
                              "The main road arch crumbled into the sea; 2 killed, "
                              "traffic halted. Russia claims a record 1,441 drones "
                              "downed; Moscow hit Kyiv's bridges in reply.",
                              f_b1, 264, 22, GRAY)
    uk_bottom = max(uk_cap, uk_body)

    # Diplomacy, right narrow column, now with a real photo
    y = y0
    y = kicker(d, 648, y, "DIPLOMACY", BLUE)
    place_photo(img, "quad_manila.jpg", 648, y0 + 22, 348, 88)
    dip_cap = caption(d, 648, y0 + 22 + 88 + 2,
                      "Quad leaders pose in Manila, 17 Nov. (White House, public domain)",
                      348, size=10)
    f_h2 = font(SANS_BOLD, 22)
    y = draw_text_block(d, 648, dip_cap + 4,
                        "Trump in Manila for Quad talks, ahead of China visit",
                        f_h2, 348, 25, INK)
    dip_body = draw_text_block(d, 648, y + 4,
                               "Trump opened his Asia trip with the first Quad leaders' "
                               "meeting in two years. Xi calls for free and open trade "
                               "at APEC in Shenzhen; Putin landed overnight. The three "
                               "meet Thursday to talk Iran and Ukraine.",
                               font(SANS, 13), 348, 17, GRAY)
    # Thursday box, just below the body (no overlap by construction)
    box_top = dip_body + 4
    d.rectangle([648, box_top, 996, box_top + 24], outline=NAVY, width=1)
    f_box = font(SANS_BOLD, 14)
    bx = "THURSDAY: Trump, Xi and Putin meet in Shenzhen"
    d.text((648 + (348 - d.textlength(bx, font=f_box)) / 2, box_top + 6), bx,
           font=f_box, fill=NAVY)
    dip_bottom = box_top + 24

    # vertical divider between the two columns
    row1_bottom = max(uk_bottom, dip_bottom)
    d.line([(632, y0), (632, row1_bottom)], fill=LIGHT_RULE, width=1)

    # ---- rule ----------------------------------------------------------
    rule2_y = row1_bottom + 8
    d.line([(0, rule2_y), (W, rule2_y)], fill=INK, width=2)

    # ---- row 2: Gaza + COP31, horizontal strips ------------------------
    y2 = rule2_y + 8
    # Gaza, left
    place_photo(img, "gaza_tents.jpg", MARGIN, y2, 158, 85)
    gz_cap = caption(d, MARGIN, y2 + 85 + 2,
                     "Flooded tents, Deir el-Balah, Jan. 2025 (UNRWA)",
                     158, size=10)
    kicker(d, 202, y2, "GAZA", OLIVE, size=14)
    f_h3 = font(SANS_BOLD, 19)
    yy = draw_text_block(d, 202, y2 + 16,
                         "Gaza: UN warns of deaths from the cold",
                         f_h3, 310, 24, INK)
    gz_body = draw_text_block(d, 202, yy + 4,
                              "About 1.7m displaced; Australia, Canada, Italy and the "
                              "UK urge aid access. Strikes continue despite the "
                              "ceasefire.",
                              font(SANS, 13), 310, 17, GRAY)
    gz_bottom = max(gz_cap, gz_body)
    # vertical divider
    d.line([(520, y2), (520, gz_bottom)], fill=LIGHT_RULE, width=1)

    # COP31, right
    place_photo(img, "cop31.jpg", 536, y2, 158, 85)
    cp_cap = caption(d, 536, y2 + 85 + 2,
                     "Bowen (left) and Jorgensen, Antalya (EU, CC BY 4.0)",
                     158, size=10)
    kicker(d, 710, y2, "CLIMATE", TEAL, size=14)
    yy = draw_text_block(d, 710, y2 + 16,
                         "COP31: draft deal still split",
                         f_h3, 286, 24, INK)
    cp_body = draw_text_block(d, 710, yy + 4,
                              "Antalya talks close Friday. Heat and cooling roadmap "
                              "backed; ocean measures make the draft text.",
                              font(SANS, 13), 286, 17, GRAY)
    cp_bottom = max(cp_cap, cp_body)

    row2_bottom = max(gz_bottom, cp_bottom)

    # ---- footer: also strip + sources ----------------------------------
    ftr_y = row2_bottom + 8
    d.line([(0, ftr_y), (W, ftr_y)], fill=INK, width=2)
    f_also_tag = font(SANS_BOLD, 15)
    f_also = font(SANS, 15)
    d.text((MARGIN, ftr_y + 8), "ALSO", font=f_also_tag, fill=RED)
    also_end = draw_text_block(d, MARGIN + 58, ftr_y + 8,
                               "Russian An-12 military plane crashes in Siberia — 19 "
                               "dead. Nvidia Q3 revenue $115.8bn, first earnings without "
                               "Jensen Huang, guides $130bn.",
                               f_also, W - MARGIN - (MARGIN + 58), 20, (51, 51, 51))
    f_src = font(SANS, 12)
    src = ("Sources: Reuters  ·  RFE/RL  ·  UN News  ·  CNN  ·  Al Jazeera  "
           "—  18 November 2026")
    d.text(((W - d.textlength(src, font=f_src)) / 2, also_end + 4), src,
           font=f_src, fill=GRAY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
