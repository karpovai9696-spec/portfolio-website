# -*- coding: utf-8 -*-
"""Финальный рендер визитки 1080x1920 (PNG + PDF) в дизайне vizitka.kanva.pptd."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
BG = (10, 12, 20)          # #0A0C14
CARD = (18, 21, 31)        # #12151F
BORDER = (38, 44, 64)      # #262C40
PRIMARY = (59, 130, 246)   # #3B82F6
ACCENT = (139, 92, 246)    # #8B5CF6
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)
SOFT = (203, 213, 225)
ICON_BLUE = (96, 165, 250)
VIOLET_LIGHT = (167, 139, 250)
BLUE_LIGHT = (96, 165, 250)

FD = "vizitka/fonts"

def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght is not None:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    return f

def lin_gradient(w, h, c1, c2, horizontal=True):
    if horizontal:
        t = np.linspace(0, 1, w)[None, :, None]
    else:
        t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(c1)[None, None, :] * (1 - t) + np.array(c2)[None, None, :] * t).astype(np.uint8)
    arr = np.broadcast_to(arr, (h, w, 3)).copy()
    return Image.fromarray(arr, "RGB")

def draw_tracked(draw, xy, text, f, fill, tracking=0, anchor_center_x=None):
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (anchor_center_x - total / 2) if anchor_center_x is not None else xy[0]
    y = xy[1]
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += wch + tracking
    return total

def gradient_text(img, center, text, f, c1, c2, tracking=0):
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    widths = [md.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = center[0] - total / 2
    bbox = md.textbbox((0, 0), text, font=f)
    y = center[1] - (bbox[3] - bbox[1]) / 2 - bbox[1]
    for ch, wch in zip(text, widths):
        md.text((x, y), ch, font=f, fill=255)
        x += wch + tracking
    grad = lin_gradient(img.size[0], img.size[1], c1, c2, horizontal=True)
    img.paste(grad, (0, 0), mask)

img = Image.new("RGB", (W, H), BG)

# ---- фоновые пятна (blur) ----
blobs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blobs)
bd.ellipse([-240, -240, 540, 540], fill=PRIMARY + (56,))
bd.ellipse([495, 1320, 1335, 2160], fill=ACCENT + (56,))
bd.ellipse([645, 450, 1215, 1020], fill=ACCENT + (32,))
blobs = blobs.filter(ImageFilter.GaussianBlur(120))
img.paste(Image.alpha_composite(img.convert("RGBA"), blobs).convert("RGB"), (0, 0))

d = ImageDraw.Draw(img)

# ---- верхняя плашка ----
mono = font(f"{FD}/JetBrainsMono-Var.ttf", 21, 500)
draw_tracked(d, (0, 78), "// ФРИЛАНС · ВЕБ-РАЗРАБОТКА", mono, PRIMARY, tracking=6, anchor_center_x=W / 2)

# ---- фото в градиентном кольце ----
cx, cy, r_ring, r_photo = 540, 420, 246, 228
ring_mask = Image.new("L", (W, H), 0)
rd = ImageDraw.Draw(ring_mask)
rd.ellipse([cx - r_ring, cy - r_ring, cx + r_ring, cy + r_ring], fill=255)
rd.ellipse([cx - r_photo, cy - r_photo, cx + r_photo, cy + r_photo], fill=0)
ring_grad = lin_gradient(W, H, PRIMARY, ACCENT, horizontal=False)
img.paste(ring_grad, (0, 0), ring_mask)

photo = Image.open("vizitka/media/photo.jpg").convert("RGB").resize((r_photo * 2, r_photo * 2), Image.LANCZOS)
pmask = Image.new("L", (r_photo * 2, r_photo * 2), 0)
ImageDraw.Draw(pmask).ellipse([0, 0, r_photo * 2, r_photo * 2], fill=255)
img.paste(photo, (cx - r_photo, cy - r_photo), pmask)

# ---- имя ----
russo = font(f"{FD}/RussoOne.ttf", 69)
draw_tracked(d, (0, 729), "МИХАИЛ КАРПОВ", russo, TEXT, tracking=3, anchor_center_x=W / 2)

# ---- роль (градиентный текст) ----
manrope_bold = font(f"{FD}/Manrope-Var.ttf", 35, 800)
gradient_text(img, (W / 2, 852), "Full Stack Developer", manrope_bold, BLUE_LIGHT, VIOLET_LIGHT)
d = ImageDraw.Draw(img)

# ---- разделитель ----
div_w, div_h = 180, 5
div_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(div_mask).rounded_rectangle([W / 2 - div_w / 2, 924, W / 2 + div_w / 2, 924 + div_h], radius=3, fill=255)
img.paste(lin_gradient(W, H, PRIMARY, ACCENT, horizontal=True), (0, 0), div_mask)
d = ImageDraw.Draw(img)

# ---- услуги ----
mono_small = font(f"{FD}/JetBrainsMono-Var.ttf", 20, 500)
draw_tracked(d, (0, 981), "ЧТО Я ДЕЛАЮ", mono_small, PRIMARY, tracking=6, anchor_center_x=W / 2)
manrope = font(f"{FD}/Manrope-Var.ttf", 28, 500)
services = ["Лендинги и сайты-визитки", "Веб-приложения на Vue / React", "Интернет-магазины", "Доработка и поддержка проектов"]
y = 1035
for s in services:
    w_line = d.textlength(s, font=manrope)
    d.text((W / 2 - w_line / 2, y), s, font=manrope, fill=SOFT)
    y += 53

# ---- карточка контактов ----
card_x0, card_y0, card_x1, card_y1 = 105, 1317, 975, 1665
d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=31, fill=CARD, outline=BORDER, width=2)

fa_solid = f"{FD}/fa-solid-900.ttf"
fa_brands = f"{FD}/fa-brands-400.ttf"
manrope_c = font(f"{FD}/Manrope-Var.ttf", 26, 500)
manrope_cb = font(f"{FD}/Manrope-Var.ttf", 26, 700)

rows = [
    (fa_brands, "\uf2c6", [("Telegram — ", SOFT, manrope_c), ("@Phoenix9696", TEXT, manrope_cb)]),
    (fa_solid, "\uf095", [("8 909 308-77-67", SOFT, manrope_c)]),
    (fa_solid, "\uf0e0", [("mikhail.karpov.03@internet.ru", SOFT, manrope_c)]),
    (fa_solid, "\uf0ac", [("yq2no6cpbdyom.kimi.page", SOFT, manrope_c)]),
]
row_ys = [1365, 1443, 1521, 1599]
for (ff, glyph, parts), ry in zip(rows, row_ys):
    fi = ImageFont.truetype(ff, 33)
    d.text((156, ry - 16), glyph, font=fi, fill=ICON_BLUE)
    x = 216
    for txt, color, fnt in parts:
        d.text((x, ry - 19), txt, font=fnt, fill=color)
        x += d.textlength(txt, font=fnt)

# ---- QR ----
qr_x, qr_y, qr_s = 129, 1710, 174
d.rounded_rectangle([qr_x, qr_y, qr_x + qr_s, qr_y + qr_s], radius=17, fill=(255, 255, 255))
qr = Image.open("vizitka/media/qr.png").convert("RGB").resize((150, 150), Image.LANCZOS)
img.paste(qr, (qr_x + 12, qr_y + 12))

cap_b = font(f"{FD}/Manrope-Var.ttf", 27, 700)
d.text((339, 1755), "Наведите камеру —", font=cap_b, fill=TEXT)
d.text((339, 1796), "откроется моё", font=cap_b, fill=TEXT)
site_t = "сайт-портфолио"
x2 = 339 + d.textlength("откроется моё ", font=cap_b)
d.text((x2, 1796), site_t, font=cap_b, fill=VIOLET_LIGHT)

img.save("vizitka-story.png")
img.save("vizitka.pdf", "PDF", resolution=144.0)
print("OK: vizitka-story.png", img.size, "+ vizitka.pdf")
