#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no timestamps, no randomness, no network. Running this
script any number of times writes byte-identical entry.png.
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
GREY = (90, 86, 76)
LIGHT = (226, 219, 200)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text, return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_flags(draw, x, y, w, h):
    """Three small national flags: US, China, Russia, in a row."""
    fw, fh = w // 3, h
    # United States: stripes + blue canton
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * fh // 7, x + fw - 8, y + (i + 1) * fh // 7], fill=col)
    draw.rectangle([x, y, x + int(fw * 0.42), y + fh * 4 // 7], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            px = x + 6 + c * 11
            py = y + 5 + r * 11
            draw.ellipse([px, py, px + 4, py + 4], fill=(255, 255, 255))
    # China: red field, one big + four small yellow stars
    cx = x + fw
    draw.rectangle([cx, y, cx + fw - 8, y + fh], fill=(222, 41, 16))
    draw.ellipse([cx + 8, y + 8, cx + 24, y + 24], fill=(255, 222, 0))
    for sx, sy in [(cx + 30, y + 8), (cx + 36, y + 18), (cx + 36, y + 30), (cx + 28, y + 38)]:
        draw.ellipse([sx, sy, sx + 7, sy + 7], fill=(255, 222, 0))
    # Russia: white / blue / red horizontal bands
    rx = x + 2 * fw
    bands = [(255, 255, 255), (0, 57, 166), (213, 0, 50)]
    for i, col in enumerate(bands):
        draw.rectangle([rx, y + i * fh // 3, rx + fw - 8, y + (i + 1) * fh // 3], fill=col)
    # thin gold frame around the trio
    draw.rectangle([x - 2, y - 2, x + w - 10, y + fh + 2], outline=(150, 120, 40), width=2)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels, three marked cities."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(210, 228, 240),
                 outline=BLUE, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    for dy in (-r // 2, r // 2):
        w2 = int((r * r - dy * dy) ** 0.5)
        draw.line([(cx - w2, cy + dy), (cx + w2, cy + dy)], fill=BLUE, width=2)
    # three cities: Shenzhen, Washington, Moscow
    for dx, dy, label in [(-r // 2, r // 3, "SHENZHEN"), (r // 2, -r // 4, "WASHINGTON"),
                          (0, -r // 2, "MOSCOW")]:
        px, py = cx + dx, cy + dy
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=(255, 255, 255), width=2)


def draw_missile(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(235, 230, 215), outline=INK, width=2)
    # rising rocket: body, nose, fins, trail
    draw.polygon([(x + s // 2, y + 12), (x + s // 2 - 10, y + 48),
                  (x + s // 2 + 10, y + 48)], fill=RED)
    draw.rectangle([x + s // 2 - 10, y + 48, x + s // 2 + 10, y + 66], fill=GREY)
    draw.polygon([(x + s // 2 - 10, y + 66), (x + s // 2 - 18, y + 78),
                  (x + s // 2 - 10, y + 70)], fill=INK)
    draw.polygon([(x + s // 2 + 10, y + 66), (x + s // 2 + 18, y + 78),
                  (x + s // 2 + 10, y + 70)], fill=INK)
    draw.line([(x + s // 2 - 12, y + 82), (x + s // 2 + 12, y + 82)], fill=BLUE, width=3)


def draw_chart(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(235, 230, 215), outline=INK, width=2)
    bars = [18, 30, 24, 42, 56]
    bw = 12
    for i, bh in enumerate(bars):
        bx = x + 10 + i * 16
        draw.rectangle([bx, y + s - 10 - bh, bx + bw, y + s - 10], fill=BLUE)
    draw.line([(x + 8, y + s - 14 - 56), (x + s - 8, y + 14)], fill=RED, width=4)
    draw.polygon([(x + s - 8, y + 14), (x + s - 20, y + 14), (x + s - 8, y + 26)], fill=RED)


def draw_probe(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(20, 24, 48), outline=INK, width=2)
    for sx, sy in [(x + 12, y + 14), (x + 34, y + 30), (x + 62, y + 12),
                   (x + 76, y + 44), (x + 20, y + 62), (x + 58, y + 70)]:
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # probe body + dish + antenna
    draw.rectangle([x + 30, y + 44, x + 52, y + 58], fill=(200, 200, 200), outline=INK, width=2)
    draw.polygon([(x + 52, y + 44), (x + 74, y + 30), (x + 74, y + 52)], fill=(230, 230, 230),
                 outline=INK)
    draw.line([(x + 41, y + 44), (x + 41, y + 26)], fill=(200, 200, 200), width=3)
    draw.ellipse([x + 37, y + 20, x + 45, y + 28], fill=RED)


def draw_bridge(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(235, 230, 215), outline=INK, width=2)
    # water
    draw.rectangle([x + 6, y + s - 22, x + s - 6, y + s - 6], fill=(120, 170, 210))
    # deck with a gap in the middle
    draw.line([(x + 6, y + 44), (x + s // 2 - 12, y + 44)], fill=INK, width=5)
    draw.line([(x + s // 2 + 12, y + 44), (x + s - 6, y + 44)], fill=INK, width=5)
    # arch + towers
    draw.arc([x + 10, y + 18, x + s - 10, y + 66], start=200, end=340, fill=RED, width=4)
    draw.line([(x + 16, y + 20), (x + 16, y + 44)], fill=INK, width=4)
    draw.line([(x + s - 16, y + 20), (x + s - 16, y + 44)], fill=INK, width=4)
    # falling fragment
    draw.polygon([(x + s // 2 - 6, y + 50), (x + s // 2 + 6, y + 50),
                  (x + s // 2, y + 62)], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    rx = W - mx

    # ---- masthead ----
    f_mast = font(SANS_B, 19)
    d.text((W // 2, 30), "THE WORLD IN ONE IMAGE", font=f_mast, fill=INK, anchor="ma")
    f_date = font(SERIF_B, 46)
    d.text((W // 2, 56), "THURSDAY 19 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
    rule(d, mx, rx, 116, 3)
    rule(d, mx, rx, 122, 1)

    # ---- lead story ----
    ly = 138
    f_kick = font(SANS_B, 16)
    d.text((mx, ly), "SHENZHEN  ·  THE FIRST TRILATERAL SUMMIT", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 47)
    d.text((mx, ly + 28), "TRUMP, XI AND PUTIN", font=f_head, fill=INK)
    d.text((mx, ly + 82), "MEET IN SHENZHEN", font=f_head, fill=INK)
    f_deck = font(SERIF, 21)
    deck = ("Xi Jinping hugs Donald Trump on the tarmac as the three leaders "
            "gather in China — with trade, technology and the wars in Ukraine "
            "and the Gulf on the agenda.")
    para(d, mx, ly + 148, deck, f_deck, 600, 28)
    f_src = font(SANS, 13)
    d.text((mx, ly + 148 + 84), "The New York Times  ·  Reuters", font=f_src, fill=GREY)
    # lead art: flags + globe, right column
    draw_flags(d, 668, ly + 30, 300, 84)
    d.text((668, ly + 128), "THREE LEADERS, ONE TABLE", font=font(SANS_B, 14), fill=BLUE)
    draw_globe(d, 818, ly + 218, 62)
    rule(d, mx, rx, 448, 2)

    # ---- secondary stories: 2 x 2 grid ----
    cells = [
        ("GULF ON EDGE",
         "US forces strike an Iranian missile site; Tehran hits a US base in "
         "Kuwait and Bahrain again. Three American carriers are now in the region.",
         "Reuters", draw_missile),
        ("ANTHROPIC'S $81.3BN IPO",
         "The AI firm prices shares at $83 in the biggest stock-market debut "
         "in history.",
         "Al Jazeera", draw_chart),
        ("VOYAGER 1, ONE LIGHT-DAY OUT",
         "Fifty years after launch, NASA's probe reaches a record distance "
         "from Earth.",
         "Al Jazeera", draw_probe),
        ("CRIMEA BRIDGE HIT AGAIN",
         "Traffic is suspended after a fresh attack on the link to mainland "
         "Russia, its head says.",
         "BBC", draw_bridge),
    ]
    f_cell_h = font(SERIF_B, 22)
    f_cell_d = font(SERIF, 16)
    f_cell_s = font(SANS, 11)
    gy0, gh, gw = 468, 140, 466
    for i, (head, deck2, src, icon) in enumerate(cells):
        cx = mx + (i % 2) * (gw + 20)
        cy = gy0 + (i // 2) * (gh + 16)
        icon(d, cx, cy + 4, 92)
        tx = cx + 106
        tw = gw - 106
        y = cy + 2
        for line in wrap(d, head, f_cell_h, tw):
            d.text((tx, y), line, font=f_cell_h, fill=INK)
            y += 26
        y = para(d, tx, y + 2, deck2, f_cell_d, tw, 21)
        d.text((tx, cy + gh - 16), src, font=f_cell_s, fill=GREY)
        if i % 2 == 0:
            d.line([(cx + gw + 10, cy), (cx + gw + 10, cy + gh)], fill=LIGHT, width=2)
    rule(d, mx, rx, 780, 2)

    # ---- also strip ----
    ay = 798
    d.text((mx, ay), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)
    also = [
        ("GAZA", "Israeli troops launch a rare ground operation beyond the ceasefire line.", "Sky News"),
        ("VICE CITY", "Grand Theft Auto VI begins its global rollout.", "BBC"),
        ("WASHINGTON", "Democrats nominate Hakeem Jeffries for Speaker, a first for a Black American.", "BBC"),
        ("ART", "A Van Gogh sells for a record $190.4m after a row over its Nazi-era past.", "BBC"),
        ("CARACAS", "The US and Venezuela sign a deal to restore military ties, says Hegseth.", "AP"),
    ]
    f_also_b = font(SANS_B, 15)
    f_also = font(SERIF, 15)
    y = ay + 28
    for tag, text, src in also:
        d.text((mx, y), tag + " — ", font=f_also_b, fill=INK)
        tw = d.textlength(tag + " — ", font=f_also_b)
        d.text((mx + tw, y), text, font=f_also, fill=INK)
        d.text((rx, y), src, font=f_cell_s, fill=GREY, anchor="ra")
        y += 27
    rule(d, mx, rx, 956, 1)
    d.text((W // 2, 966), "Sources: Reuters · AP · BBC · Al Jazeera · The New York Times · Sky News — "
           "every event reported on 19 November 2026",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG")
    data = out.read_bytes()
    print(f"wrote {out} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
