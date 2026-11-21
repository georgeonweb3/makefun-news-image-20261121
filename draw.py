#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a one-page newspaper front page
summing up world news of Saturday 21 November 2026.

The hero is the third straight night of Houthi missiles aimed at
Riyadh, all three intercepted before dawn -- drawn as a night sky over
the Riyadh skyline with interceptor streaks meeting the incoming
missiles. Six more stories sit in two rows of three cards below, and
an "Also today" strip closes the page. Every pixel is drawn with
Pillow; no photos, no scraped images, no logos.
Run:  python3 draw.py  ->  writes entry.png (1024x1024, < 1 MiB).

Stories (verified against 2+ reputable outlets each; see README.md):
  Lead  Houthi missiles target Riyadh a third straight night; Saudi
        air defences intercept all three before dawn on 21 Nov.
  1     COP31 climate talks in Turkiye drag into overtime as the
        fossil-fuel wording deadlocks the deal.
  2     Trump threatens Iran with war over a rumoured "dirty bomb"
        plot on Washington (20 Nov press conference).
  3     Denmark expels its Russian defence attache over an alleged
        plot to kill a US-Ukrainian on Danish soil (announced 20 Nov).
  4     Nasdaq wipes out all its 2026 gains as the AI sell-off sinks
        Anthropic's IPO bounce (20 Nov close).
  5     FBI investigating a suspected hack of its national crime
        database, the NCIC (reported 21 Nov).
  6     Qatar pledges EUR 15bn more investment in Germany during the
        emir's Berlin visit (20 Nov).
  Also   Basra gas blast (toll disputed); Iran claims a 58th US MQ-9
        downed; Europe youth protests roll on; Peru 6.7 quake;
        pancreatic cancer pill trial; UEFA fines England EUR 15,000.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 232)
INK = (22, 22, 22)
SOFT = (62, 62, 62)
NAVY = (14, 32, 58)
NIGHT = (8, 18, 40)
RED = (178, 38, 28)
GOLD = (214, 158, 58)
PANEL = (255, 253, 247)
BORDER = (204, 196, 176)
TEAL = (16, 90, 94)
GREEN = (30, 108, 56)
ORANGE = (212, 94, 18)
STEEL = (50, 82, 120)
CRIMSON = (138, 26, 26)
SKY_TOP = (10, 22, 52)
SKY_BOT = (46, 78, 128)

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FN + "NotoSans-Bold.ttf"
SANS_R = FN + "NotoSans-Regular.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    """Greedy word wrap to pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 124], fill=NAVY)
d.text((W // 2, 12), "ONE DAY  \u00b7  ONE PICTURE  \u00b7  THE WORLD",
       font=font(SANS_B, 18), fill=GOLD, anchor="ma")
d.text((W // 2, 36), "THE WORLD IN ONE DAY",
       font=font(SERIF_B, 52), fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 94), "SATURDAY  21  NOVEMBER  2026",
       font=font(SANS_B, 26), fill=(255, 255, 255), anchor="ma")
d.rectangle([0, 124, W, 130], fill=RED)

M, G = 34, 14
X0, X1 = M, W - M
CW = X1 - X0  # 956


def panel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER, width=2)


# ---------------------------------------------------------------- icons
def icon_globe_flame(cx, cy, s=16, col=GREEN):
    # globe (circle + meridians) with a small flame licking the top
    d.ellipse([cx - s, cy - s + 6, cx + s, cy + s + 4],
              outline=col, width=4)
    d.line([(cx, cy - s + 6), (cx, cy + s + 4)], fill=col, width=3)
    d.line([(cx - s, cy + 5), (cx + s, cy + 5)], fill=col, width=3)
    d.arc([cx - s + 5, cy - s + 6, cx + s - 5, cy + s + 4],
          270, 90, fill=col, width=3)
    # flame: two teardrop polygons above the globe
    d.polygon([(cx + 8, cy - s - 2), (cx + 14, cy - s - 14),
               (cx + 20, cy - s - 2)], fill=ORANGE)
    d.polygon([(cx + 12, cy - s - 2), (cx + 16, cy - s - 10),
               (cx + 20, cy - s - 2)], fill=GOLD)


def icon_capitol(cx, cy, s=16, col=STEEL):
    # domed capitol: stepped base, columned drum, dome, flag pole
    d.rectangle([cx - s - 6, cy + s - 2, cx + s + 6, cy + s + 4], fill=col)
    d.rectangle([cx - s - 2, cy + 2, cx + s + 2, cy + s - 2], fill=col)
    for cxx in (cx - 12, cx - 4, cx + 4, cx + 12):
        d.rectangle([cxx - 2, cy + 4, cxx + 2, cy + s - 2],
                    fill=PANEL)
    d.pieslice([cx - 12, cy - s - 2, cx + 12, cy + 2], 180, 360, fill=col)
    d.rectangle([cx - 2, cy - s - 12, cx + 2, cy - s - 2], fill=col)
    d.polygon([(cx + 2, cy - s - 12), (cx + 12, cy - s - 9),
               (cx + 2, cy - s - 6)], fill=RED)


def icon_shield(cx, cy, s=16, col=CRIMSON):
    # shield outline with a five-point star in the middle
    d.polygon([(cx - s, cy - s + 2), (cx + s, cy - s + 2),
               (cx + s, cy + 2), (cx, cy + s + 4),
               (cx - s, cy + 2)], fill=col)
    d.polygon([(cx, cy - s + 8), (cx + 3, cy - s + 14),
               (cx + 9, cy - s + 14), (cx + 4, cy - s + 18),
               (cx + 6, cy - s + 24), (cx, cy - s + 20),
               (cx - 6, cy - s + 24), (cx - 4, cy - s + 18),
               (cx - 9, cy - s + 14), (cx - 3, cy - s + 14)],
              fill=GOLD)


def icon_chart_down(cx, cy, s=16, col=CRIMSON):
    # axes plus a line plunging down-right, arrowhead at the end
    d.line([(cx - s - 4, cy + s), (cx + s + 6, cy + s)], fill=col, width=4)
    d.line([(cx - s - 4, cy + s), (cx - s - 4, cy - s)], fill=col, width=4)
    pts = [(cx - s, cy - s + 4), (cx - 6, cy - 2),
           (cx + 4, cy + 4), (cx + s, cy + s - 2)]
    d.line(pts, fill=col, width=5, joint="curve")
    d.polygon([(cx + s, cy + s - 2), (cx + s - 2, cy + s - 14),
               (cx + s + 12, cy + s - 4)], fill=col)


def icon_lock(cx, cy, s=16, col=STEEL):
    # padlock: shackle arc, body, keyhole
    d.arc([cx - 10, cy - s - 2, cx + 10, cy + 2], 180, 360,
          fill=col, width=5)
    d.rounded_rectangle([cx - s - 2, cy - 2, cx + s + 2, cy + s + 4],
                        radius=5, fill=col)
    d.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=GOLD)
    d.rectangle([cx - 1, cy + 7, cx + 1, cy + 13], fill=GOLD)


def icon_bank(cx, cy, s=16, col=TEAL):
    # classical bank front: pediment, three columns, steps
    d.polygon([(cx - s - 6, cy - s + 4), (cx + s + 6, cy - s + 4),
               (cx, cy - s - 8)], fill=col)
    for cxx in (cx - 14, cx, cx + 14):
        d.rectangle([cxx - 3, cy - s + 8, cxx + 3, cy + s - 4], fill=col)
    d.rectangle([cx - s - 6, cy + s - 4, cx + s + 6, cy + s + 2], fill=col)
    d.rectangle([cx - s - 10, cy + s + 2, cx + s + 10, cy + s + 6],
                fill=col)
    d.text((cx, cy - s - 24), "\u20ac", font=font(SANS_B, 15),
           fill=GOLD, anchor="ma")


# ---------------------------------------------------------------- hero
LY = 140
LH = 406
panel(X0, LY, CW, LH)
# kicker + headline + deck (left column)
lx, lw = X0 + 24, 540
d.text((lx, LY + 20), "RIYADH  \u00b7  THIRD NIGHT IN A ROW  \u2014  LEAD STORY",
       font=font(SANS_B, 19), fill=RED)
hl = wrap("HOUTHI MISSILES TARGET RIYADH, THIRD NIGHT",
          font(SERIF_B, 46), lw)
assert len(hl) <= 3, hl
y = text_block(lx, LY + 54, hl, font(SERIF_B, 46), INK, 54)
d.rectangle([lx, y + 8, lx + 120, y + 13], fill=GOLD)
deck = wrap("Saudi air defences intercept all three ballistic missiles "
            "in a pre-dawn attack; the capital is on alert for a third "
            "night running, two days after a strike damaged the "
            "PIF Tower.", font(SANS_R, 23), lw)
assert len(deck) <= 4, deck
y = text_block(lx, y + 28, deck, font(SANS_R, 23), SOFT, 30)
assert y <= LY + LH - 16, y

# hero illustration: night sky over Riyadh -- crescent moon, stars,
# skyline with the tall PIF Tower, and three interceptor streaks
# climbing to meet the incoming missiles in bright bursts
ix0, ix1 = X0 + 600, X1 - 24
iy0, iy1 = LY + 18, LY + LH - 18
for yy in range(iy0, iy1):
    t = (yy - iy0) / max(1, iy1 - iy0)
    c = tuple(int(SKY_BOT[i] + (SKY_TOP[i] - SKY_BOT[i]) * t)
              for i in range(3))
    d.line([(ix0, yy), (ix1, yy)], fill=c)
# stars (seeded, deterministic)
random.seed(21)
for _ in range(46):
    sx = random.randint(ix0 + 6, ix1 - 6)
    sy = random.randint(iy0 + 6, iy1 - 170)
    r = random.choice((1, 1, 2))
    d.ellipse([sx - r, sy - r, sx + r, sy + r],
              fill=(235, 238, 250))
# crescent moon, top right
mx, my = ix1 - 66, iy0 + 34
d.ellipse([mx - 26, my - 26, mx + 26, my + 26], fill=(248, 240, 200))
d.ellipse([mx - 14, my - 30, mx + 34, my + 20], fill=SKY_TOP)
# skyline silhouettes with lit windows
bx = ix0
while bx < ix1 - 10:
    bw = random.randint(22, 38)
    bh = random.randint(56, 150)
    d.rectangle([bx, iy1 - bh - 84, bx + bw, iy1 - 84], fill=NIGHT)
    for _ in range(bw // 9):
        wx = bx + random.randint(3, max(4, bw - 6))
        wy = iy1 - bh - 84 + random.randint(8, max(9, bh - 12))
        d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    bx += bw + 3
# the PIF Tower: tallest, twisted crown, centre-left of the frame
tx0 = ix0 + 52
d.rectangle([tx0, iy1 - 252, tx0 + 30, iy1 - 84], fill=NIGHT)
d.polygon([(tx0 + 15, iy1 - 288), (tx0 + 8, iy1 - 252),
           (tx0 + 22, iy1 - 252)], fill=NIGHT)
for wy in range(iy1 - 244, iy1 - 104, 20):
    d.rectangle([tx0 + 4, wy, tx0 + 8, wy + 7], fill=GOLD)
    d.rectangle([tx0 + 21, wy, tx0 + 25, wy + 7], fill=GOLD)
# ground band
d.rectangle([ix0, iy1 - 84, ix1, iy1], fill=(6, 12, 28))
d.rectangle([ix0, iy1 - 84, ix1, iy1 - 80], fill=GOLD)
# three interceptor streaks: bright lines rising from the ground to
# starburst intercepts high in the sky
for gx, bx_, by_ in ((ix0 + 78, ix0 + 128, iy0 + 92),
                     (ix0 + 178, ix0 + 208, iy0 + 62),
                     (ix0 + 262, ix0 + 296, iy0 + 104)):
    d.line([(gx, iy1 - 84), (bx_, by_)], fill=(255, 214, 120), width=4)
    d.line([(gx, iy1 - 84), (bx_, by_)], fill=(255, 255, 255), width=2)
    # starburst at the intercept point
    for ang in range(0, 360, 45):
        ex = bx_ + int(16 * math.cos(math.radians(ang)))
        ey = by_ + int(16 * math.sin(math.radians(ang)))
        d.line([(bx_, by_), (ex, ey)], fill=(255, 226, 140), width=2)
    d.ellipse([bx_ - 6, by_ - 6, bx_ + 6, by_ + 6],
              fill=(255, 244, 190))
d.rectangle([ix0, iy0, ix1, iy1], outline=BORDER, width=2)


# ---------------------------------------------------------------- story rows
stories = [
    ("T\u00dcRKIYE  \u00b7  CLIMATE  \u2014  TODAY", GREEN, icon_globe_flame,
     "COP31 TALKS DRAG INTO OVERTIME",
     "Fossil-fuel wording deadlocks the deal as talks run an extra "
     "day."),
    ("WASHINGTON  \u00b7  20 NOV", STEEL, icon_capitol,
     "TRUMP THREATENS IRAN WITH WAR",
     "Warns of war over a rumoured \u201cdirty bomb\u201d plot on "
     "Washington; no plot confirmed."),
    ("COPENHAGEN  \u00b7  20 NOV", CRIMSON, icon_shield,
     "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Envoy ordered out in 7 days over an alleged plot to kill a "
     "US-Ukrainian on Danish soil."),
    ("WALL STREET  \u00b7  20 NOV CLOSE", CRIMSON, icon_chart_down,
     "NASDAQ WIPES OUT 2026 GAINS",
     "AI sell-off sinks Anthropic\u2019s IPO bounce; Nasdaq 100 down "
     "5.61% on Friday."),
    ("WASHINGTON  \u00b7  TODAY", STEEL, icon_lock,
     "FBI PROBES HACK OF CRIME DATABASE",
     "Suspected intrusion into the NCIC, the national database US "
     "police use daily."),
    ("BERLIN  \u00b7  20 NOV", TEAL, icon_bank,
     "QATAR PLEDGES \u20ac15BN TO GERMANY",
     "Emir\u2019s Berlin visit seals a \u201c360-degree partnership\u201d "
     "and two defence deals."),
]

PW = (CW - 2 * G) // 3  # 309
PH = 184
for row in range(2):
    ry = 560 + row * (PH + G)
    for col in range(3):
        kicker, kcol, icon, headline, deck = stories[row * 3 + col]
        px = X0 + col * (PW + G)
        panel(px, ry, PW, PH)
        icon(px + 28, ry + 24, s=16, col=kcol)
        klines = wrap(kicker, font(SANS_B, 14), PW - 78)
        assert len(klines) <= 1, (kicker, klines)
        text_block(px + 64, ry + 14, klines, font(SANS_B, 14), kcol, 18)
        hlines = wrap(headline, font(SERIF_B, 20), PW - 28)
        y = text_block(px + 14, ry + 54, hlines, font(SERIF_B, 20), INK, 24)
        dlines = wrap(deck, font(SANS_R, 14), PW - 28)
        y = text_block(px + 14, y + 6, dlines, font(SANS_R, 14), SOFT, 17)
        assert len(hlines) <= 3 and len(dlines) <= 3, (headline, hlines, dlines)
        assert y <= ry + PH - 6, (headline, y, ry + PH)

# ---------------------------------------------------------------- footer
FY = 950
d.rectangle([0, FY, W, H], fill=NAVY)
d.text((M, FY + 8), "ALSO TODAY \u2014 21 NOV 2026",
       font=font(SANS_B, 19), fill=GOLD)
items = ("Basra gas blast: several killed, 30+ injured, toll disputed  "
         "\u00b7  Iran claims 58th US MQ-9 downed  \u00b7  Europe youth "
         "protests roll on  \u00b7  Peru 6.7 quake  \u00b7  Cancer pill "
         "shrinks tumours in 60.7% of patients  \u00b7  UEFA fines "
         "England \u20ac15,000")
flines = wrap(items, font(SANS_R, 15), W - 2 * M)
assert len(flines) <= 2, flines
text_block(M, FY + 32, flines, font(SANS_R, 15), (255, 255, 255), 19)

img.save("entry.png", optimize=True)
print("saved entry.png")
