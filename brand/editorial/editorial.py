"""Cedar Gate "editorial" post template (inspired by the 72 Open reference).

Full-bleed photo, dark forest-green fade from the top, centered logo,
two-line serif headline (tan line + white line), tracked caps details,
tracked light date/CTA line.

Usage: python3 editorial.py   (builds the samples at the bottom)
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

F = '/home/claude/tpl/fonts/'
SERIF = F + 'Gloock-Regular.ttf'
SANS_B = F + 'Lato-Bold.ttf'
SANS = F + 'Lato-Regular.ttf'
LOGO = '/mnt/user-data/uploads/Videos/CedarGate_Brand/logos/horiz_inverted.png'

TAN = (201, 162, 122)      # headline line 1 and details
TAN_LIGHT = (196, 176, 150)
WHITE = (246, 242, 234)
GREEN_DARK = (16, 22, 15)  # top fade colour


def grade(im):
    """Moody low-key look: lower exposure, softer greens, warm highlights."""
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    a = lum[..., None] + (a - lum[..., None]) * 0.72          # desaturate a little
    a = np.clip(a, 0, 1) ** 1.18 * 0.97                      # slightly darker mids (v2: brighter than v1)
    warm = np.array([1.06, 1.0, 0.86], dtype=np.float32)       # warm/olive cast
    a = a * (warm * lum[..., None] ** 0.5 + (1 - lum[..., None] ** 0.5))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def cover_crop(im, W, H, cx=0.5, cy=0.5):
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * cx); y = round((im.height - H) * cy)
    return im.crop((x, y, x + W, y + H))


def tracked(draw, xy_center, text, font, fill, tracking):
    """Draw text centered with letter spacing (tracking in px)."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy_center[0] - total / 2; y = xy_center[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def fit_font(draw, text, path, size, max_w):
    while size > 20:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, size)


def editorial(photo, out, line1, line2, details, footer, W=1080, H=1350,
              cx=0.5, cy=0.5, fade_end=0.42, photo_h=0.72, logo=True, top_y=150, hsize=76, dsize=23):
    src = ImageOps.exif_transpose(Image.open(photo)).convert('RGB')
    # photo occupies the lower part of the canvas; text sits on dark space above
    PH = round(H * photo_h)
    ph = grade(cover_crop(src, W, PH, cx, cy))
    im = Image.new('RGB', (W, H), GREEN_DARK)
    im.paste(ph, (0, H - PH))

    # fade from the dark top into the photo
    fade = Image.new('L', (1, H))
    top = H - PH; band = PH * fade_end
    for y in range(H):
        if y <= top: v = 255
        else:
            t = (y - top) / band
            v = int(255 * max(0, 1 - t) ** 1.4) if t < 1 else 0
        fade.putpixel((0, y), v)
    fade = fade.resize((W, H))
    im = Image.composite(Image.new('RGB', (W, H), GREEN_DARK), im, fade)

    # soft vignette
    vg = Image.new('L', (W, H), 0); d = ImageDraw.Draw(vg)
    d.ellipse((-W * 0.25, -H * 0.15, W * 1.25, H * 1.15), fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(160))
    im = Image.blend(Image.composite(im, Image.new('RGB', (W, H), (8, 10, 7)), vg), im, 0.4)

    # darken the bottom edge so bright foregrounds sit back
    bot = Image.new('L', (1, H))
    for yy in range(H):
        t = (yy - H * 0.72) / (H * 0.28)
        bot.putpixel((0, yy), int(95 * min(1, max(0, t)) ** 1.2))
    im = Image.composite(Image.new('RGB', (W, H), (10, 13, 9)), im, bot.resize((W, H)))

    d = ImageDraw.Draw(im)
    y = top_y
    if logo:
        lg = Image.open(LOGO).convert('RGBA')
        lw = 380; lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
        im.paste(lg, ((W - lw) // 2, y), lg); y += lg.height + 92

    margin = 70
    f1 = fit_font(d, line1, SERIF, hsize, W - 2 * margin)
    f2 = fit_font(d, line2, SERIF, hsize, W - 2 * margin)
    f = min(f1, f2, key=lambda x: x.size)  # same size for both lines
    for text, col in ((line1, TAN), (line2, WHITE)):
        d.text((W / 2, y), text, font=f, fill=col, anchor='mt'); y += int(f.size * 1.12)

    y += 42
    fd = fit_font(d, details, SANS_B, dsize, W - 2 * margin - 6 * len(details))
    tracked(d, (W / 2, y), details, fd, TAN, 5.2); y += int(dsize * 2)
    ff = fit_font(d, footer, SANS, dsize - 1, W - 2 * margin - 6 * len(footer))
    tracked(d, (W / 2, y), footer, ff, TAN_LIGHT, 5.6)

    im.save(out, quality=95)
    return out


if __name__ == '__main__':
    S = '/mnt/user-data/uploads/Videos/CedarGate_Nov/stills/'
    O = '/home/claude/tpl/'
    editorial(S + 's19.jpg', O + 'sample_holiday.jpg',
              'December at The Cedar Gate.', 'One night, just for your team.',
              'PRIVATE DINNER · SPORTING CLAYS · THE LODGE',
              'NOW BOOKING DECEMBER · DM US "EVENT"', cx=0.45, cy=0.5)
    editorial(S + 's2.jpg', O + 'sample_retreat.jpg',
              'Kingfisher, Oklahoma.', 'Your team, off the grid.',
              'MEETINGS · DINNERS · CABINS · CLAYS',
              'PLANNING 2027 · DM US "RETREAT"', cx=0.55, cy=0.5)
    print('ok')


def reel_overlay(out, line1, line2, details='', footer='', W=1080, H=1920, top_y=300,
                 hsize=92, dsize=28, band=0.52):
    """Transparent PNG for Reels: dark-green band fading down from the top, same
    type system as the posts (tan + white serif, tracked caps)."""
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    a = Image.new('L', (1, H))
    for y in range(H):
        t = y / (H * band)
        a.putpixel((0, y), int(250 * min(1, max(0, 1 - t) * 1.6) ** 1.1) if t < 1 else 0)
    ov.putalpha(a.resize((W, H)))
    base = Image.new('RGBA', (W, H), GREEN_DARK + (255,)); base.putalpha(ov.getchannel('A'))
    ov = base
    d = ImageDraw.Draw(ov)
    margin = 70; y = top_y
    f1 = fit_font(d, line1, SERIF, hsize, W - 2 * margin)
    f2 = fit_font(d, line2, SERIF, hsize, W - 2 * margin) if line2 else f1
    f = min(f1, f2, key=lambda x: x.size)
    for text, col in ((line1, TAN), (line2, WHITE)):
        if text:
            d.text((W / 2, y), text, font=f, fill=col + (255,), anchor='mt'); y += int(f.size * 1.12)
    y += 36
    if details:
        fd = fit_font(d, details, SANS_B, dsize, W - 2 * margin - 6 * len(details))
        tracked(d, (W / 2, y), details, fd, TAN + (255,), 5.2); y += int(dsize * 2)
    if footer:
        ff = fit_font(d, footer, SANS, dsize - 1, W - 2 * margin - 6 * len(footer))
        tracked(d, (W / 2, y), footer, ff, TAN_LIGHT + (255,), 5.6)
    ov.save(out)
    return out


# ---------------------------------------------------------------------------
# Layout family (same grade, palette and type; different layouts)
# ---------------------------------------------------------------------------
CREAM = (232, 224, 210)


def tracked_left(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def tracked_w(draw, text, font, tracking):
    return sum(draw.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def _logo(im, width, xy=None, center_y=None):
    lg = Image.open(LOGO).convert('RGBA')
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    W, H = im.size
    if xy is None: xy = ((W - width) // 2, center_y - lg.height // 2)
    im.paste(lg, xy, lg)


def _grain(im, amt=5):
    a = np.asarray(im).astype(np.int16)
    n = np.random.default_rng(7).normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))


def text_block(d, W, y, kicker, line1, line2, body, align='center', x0=80, hsize=72,
               ksize=22, bsize=28, maxw=None):
    """Kicker (tracked caps, tan) / serif line1 (tan) / serif line2 (white) / body (cream)."""
    maxw = maxw or W - 2 * x0
    cx = W / 2
    if kicker:
        fk = fit_font(d, kicker, SANS_B, ksize, maxw - 6 * len(kicker))
        if align == 'center': tracked(d, (cx, y), kicker, fk, TAN, 5.5)
        else: tracked_left(d, (x0, y), kicker, fk, TAN, 5.5)
        y += int(ksize * 2.1)
    lines = [(l, c) for l, c in ((line1, TAN), (line2, WHITE)) if l]
    if lines:
        f = min((fit_font(d, l, SERIF, hsize, maxw) for l, _ in lines), key=lambda x: x.size)
        for l, c in lines:
            if align == 'center': d.text((cx, y), l, font=f, fill=c, anchor='mt')
            else: d.text((x0, y), l, font=f, fill=c)
            y += int(f.size * 1.12)
    if body:
        y += int(bsize * 0.9)
        fb = ImageFont.truetype(SANS, bsize)
        for l in wrap(d, body, fb, maxw - 40):
            if align == 'center': d.text((cx, y), l, font=fb, fill=CREAM, anchor='mt')
            else: d.text((x0, y), l, font=fb, fill=CREAM)
            y += int(bsize * 1.45)
    return y


def measure_block(W, *a, **k):
    tmp = Image.new('RGB', (W, 4000)); d = ImageDraw.Draw(tmp)
    return text_block(d, W, 0, *a, **k)


def fullbleed(photo, out, kicker, line1, line2='', body='', W=1080, H=1350, cx=0.5, cy=0.5,
              align='left', hsize=72, logo=False, bsize=28, ksize=22, pregraded=False, pad=None):
    """Photo fills the frame; text sits at the bottom on a soft dark-green fade."""
    src = ImageOps.exif_transpose(Image.open(photo)).convert('RGB')
    im = cover_crop(src, W, H, cx, cy)
    if not pregraded: im = grade(im)
    x0 = 80
    bh = measure_block(W, kicker, line1, line2, body, align=align, x0=x0, hsize=hsize, bsize=bsize, ksize=ksize)
    bottom_pad = 150 if logo else 100
    if H > 1500: bottom_pad += 180          # stories: keep clear of the reply bar
    if pad is not None: bottom_pad = pad
    ytxt = H - bottom_pad - bh
    a = Image.new('L', (1, H))
    start = max(0, ytxt - H * 0.22)
    for y in range(H):
        t = (y - start) / max(1, (H - start))
        a.putpixel((0, y), int(225 * min(1, max(0, t) * 1.7) ** 1.3))
    im = Image.composite(Image.new('RGB', (W, H), GREEN_DARK), im, a.resize((W, H)))
    d = ImageDraw.Draw(im)
    text_block(d, W, ytxt, kicker, line1, line2, body, align=align, x0=x0, hsize=hsize, bsize=bsize, ksize=ksize)
    if logo: _logo(im, 300, center_y=H - (85 if H < 1500 else 260))
    _grain(im).save(out, quality=95)
    return out


def framed(photo, out, kicker, line1, line2='', body='', W=1080, H=1350, cx=0.5, cy=0.5,
           hsize=64, photo_frac=0.56, bsize=27, ksize=22):
    """Dark-green page, photo set inside with a thin tan rule, centered text below."""
    m = 70
    im = Image.new('RGB', (W, H), GREEN_DARK)
    ph_h = round(H * photo_frac); ph_w = W - 2 * m
    src = ImageOps.exif_transpose(Image.open(photo)).convert('RGB')
    ph = grade(cover_crop(src, ph_w, ph_h, cx, cy))
    top = m + (40 if H < 1500 else 200)
    im.paste(ph, (m, top))
    d = ImageDraw.Draw(im)
    d.rectangle((m - 14, top - 14, m + ph_w + 13, top + ph_h + 13), outline=TAN + (0,), width=1)
    y = top + ph_h + 70
    text_block(d, W, y, kicker, line1, line2, body, hsize=hsize, bsize=bsize, ksize=ksize, x0=m + 20)
    _logo(im, 240, center_y=H - (60 if H < 1500 else 240))
    _grain(im).save(out, quality=95)
    return out


def typecard(out, kicker, line1, line2='', body='', footer='', W=1080, H=1350, hsize=86, bsize=30, ksize=22):
    """No photo: dark green, big serif statement, thin tan rules."""
    im = Image.new('RGB', (W, H), GREEN_DARK)
    # very soft centre glow so the card isn't flat
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((W * 0.1, H * 0.2, W * 0.9, H * 0.8), fill=255); g = g.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new('RGB', (W, H), (30, 38, 28)), im, g)
    d = ImageDraw.Draw(im)
    bh = measure_block(W, kicker, line1, line2, body, hsize=hsize, bsize=bsize, ksize=ksize)
    y = (H - bh) // 2 - 30
    d.line((W / 2 - 40, y - 60, W / 2 + 40, y - 60), fill=TAN, width=2)
    y = text_block(d, W, y, kicker, line1, line2, body, hsize=hsize, bsize=bsize, ksize=ksize)
    if footer:
        ff = fit_font(d, footer, SANS, ksize, W - 160 - 6 * len(footer))
        tracked(d, (W / 2, y + 40), footer, ff, TAN_LIGHT, 5.6)
    _logo(im, 280, center_y=H - (90 if H < 1500 else 300))
    _grain(im).save(out, quality=95)
    return out


def reel_text(out, kicker, line1, line2='', footer='', W=1080, H=1920, top_y=300, hsize=92, band=0.52):
    """Reel overlay v2: top dark-green band + kicker / tan / white / footer, same type as posts."""
    a = Image.new('L', (1, H))
    for y in range(H):
        t = y / (H * band)
        a.putpixel((0, y), int(250 * min(1, max(0, 1 - t) * 1.6) ** 1.1) if t < 1 else 0)
    ov = Image.new('RGBA', (W, H), GREEN_DARK + (255,)); ov.putalpha(a.resize((W, H)))
    d = ImageDraw.Draw(ov)
    y = text_block(d, W, top_y, kicker, line1, line2, '', hsize=hsize, ksize=28)
    if footer:
        ff = fit_font(d, footer, SANS_B, 26, W - 160 - 6 * len(footer))
        tracked(d, (W / 2, y + 30), footer, ff, TAN_LIGHT, 5.6)
    ov.save(out)
    return out


def endcard(out, W=1080, H=1920):
    im = Image.new('RGB', (W, H), GREEN_DARK)
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((W * 0.05, H * 0.3, W * 0.95, H * 0.7), fill=255); g = g.filter(ImageFilter.GaussianBlur(240))
    im = Image.composite(Image.new('RGB', (W, H), (30, 38, 28)), im, g)
    _logo(im, 620, center_y=int(H * 0.47))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(SANS_B, 26)
    tracked(d, (W / 2, int(H * 0.47) + 70), 'KINGFISHER, OKLAHOMA', f, TAN, 7)
    _grain(im).save(out)
    return out
