#!/usr/bin/env python3
"""Builds the static assets for the rescue landing page.

Brutalist pass: paper base, pure black for every line, two loud accents
(red + yellow). Zero radius, zero gradients, zero blur.

Sources are read-only: the portrait is copied from aseppp-web's public dir and
never modified. Everything here writes new files into public/.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path("/home/cosmic/vibe-code-rescue/public")
SRC_PHOTO = pathlib.Path("/home/cosmic/app/aseppp-web/public/profile_picture.png")

PAPER = (244, 241, 232)
WHITE = (255, 255, 255)
INK = (0, 0, 0)
RED = (255, 59, 48)
YELLOW = (255, 210, 63)

MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


# ── Portrait avatar ───────────────────────────────────────────────
# Shown at 176px, so 400px wide covers retina. Square crop, face-weighted.
def avatar():
    im = Image.open(SRC_PHOTO).convert("RGB")
    w, h = im.size
    side = min(w, h)
    top = int((h - side) * 0.10)  # faces sit in the top third of a portrait
    im = im.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side))
    im = im.resize((400, 400), Image.LANCZOS)
    im.save(OUT / "asep.jpg", quality=86, optimize=True, progressive=True)
    return (OUT / "asep.jpg").stat().st_size


# ── Favicon ───────────────────────────────────────────────────────
# Black tile, red V. Square joins — the rectangle is the only shape here.
def favicon_svg():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" fill="#000000"/>'
        '<path d="M7 7 L16 25 L25 7" fill="none" stroke="#FF3B30" '
        'stroke-width="5" stroke-linejoin="miter" stroke-linecap="butt"/>'
        '</svg>'
    )
    (OUT / "favicon.svg").write_text(svg)
    return (OUT / "favicon.svg").stat().st_size


def apple_touch():
    s = 180
    im = Image.new("RGB", (s, s), INK)
    d = ImageDraw.Draw(im)
    d.line([(44, 46), (90, 136), (136, 46)], fill=RED, width=17, joint="curve")
    im.save(OUT / "apple-touch-icon.png", optimize=True)
    return (OUT / "apple-touch-icon.png").stat().st_size


# ── Open Graph card (1200x630) ────────────────────────────────────
def og_card():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    d.rectangle([24, 24, W - 25, H - 25], outline=INK, width=8)

    kick = f(MONO_B, 19)
    d.rectangle([64, 62, 64 + int(kick.getlength("VIBE CODE RESCUE")) + 32, 110], fill=INK)
    d.text((80, 75), "VIBE CODE RESCUE", font=kick, fill=PAPER)

    head = f(MONO_B, 52)
    d.text((64, 156), "IT WORKED ON YOUR LAPTOP.", font=head, fill=INK)

    y = 226
    a, b, c = "THEN ", "REAL USERS", " SHOWED UP."
    d.text((64, y), a, font=head, fill=INK)
    xb = 64 + head.getlength(a)
    bx = d.textbbox((xb, y), b, font=head)
    d.rectangle([bx[0] - 8, bx[1] - 8, bx[2] + 8, bx[3] + 8], fill=YELLOW)
    d.text((xb, y), b, font=head, fill=INK)
    d.text((xb + head.getlength(b), y), c, font=head, fill=INK)

    d.rectangle([64, 330, W - 65, 338], fill=INK)

    sub = f(MONO_R, 25)
    d.text((64, 362), "48-HOUR AUDIT OF AN AI-BUILT APP.", font=sub, fill=INK)
    d.text((64, 400), "LEAKED KEYS \u00b7 DEAD AUTH \u00b7 BROKEN FORMS.", font=sub, fill=INK)

    price = f(MONO_B, 33)
    pw = int(price.getlength("$150 FLAT"))
    d.rectangle([64, 486, 64 + pw + 44, 566], fill=RED, outline=INK, width=6)
    d.text((64 + 22, 504), "$150 FLAT", font=price, fill=INK)

    note = f(MONO_B, 23)
    mail = f(MONO_R, 22)
    d.text((64 + pw + 84, 500), "MONEY BACK IF NOTHING SERIOUS.", font=note, fill=INK)
    d.text((64 + pw + 84, 538), "asepp.saepudiin@gmail.com", font=mail, fill=INK)

    im.save(OUT / "og.png", optimize=True)
    return (OUT / "og.png").stat().st_size


if __name__ == "__main__":
    for name, fn in (("avatar", avatar), ("favicon.svg", favicon_svg),
                     ("apple-touch-icon", apple_touch), ("og.png", og_card)):
        print(f"{name:20} {fn():>9,} bytes")
