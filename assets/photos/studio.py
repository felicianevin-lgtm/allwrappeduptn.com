"""Studio v3 - clean seamless-studio product shots from phone photos.
Cutout: BiRefNet (rembg). Straighten top-down shots. Warm-white seamless backdrop,
soft shadow built from the subject's own silhouette, mild colour grade. No horizon line."""
import stub, sys, pathlib
from rembg import remove, new_session
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageDraw
import numpy as np

U = pathlib.Path(r'G:/My Drive/All Wrapped Up/Originals')  # phone originals, filed in Drive
OUT = pathlib.Path('out'); OUT.mkdir(exist_ok=True)
CUT = pathlib.Path('cut'); CUT.mkdir(exist_ok=True)
SQ, HERO, LAND = (1200, 1200), (1200, 1500), (1400, 933)
# name: (uid, canvas, kind)  kind: 'flat' = top-down flat-lay (straighten), 'stand' = upright/angled
SPECS = {
 'sq-llama-red-bow':          ('d804471c', SQ, 'flat'),
 'sq-birthday-black-white':   ('b453506e', SQ, 'flat', None, 'manual'),
 'sq-paisley':                ('a964ecf8', SQ, 'flat'),
 'land-camo-long':            ('dd10065f', LAND, 'stand', (0.02, 0.22, 0.99, 0.63)),
 'sq-camo-stack':             ('43ceaa6c', SQ, 'stand'),
 'sq-camo-birthday':          ('8fa4b488', SQ, 'stand'),
 'sq-flamingo':               ('c57b976a', SQ, 'stand'),
 'sq-hannah-check':           ('58dccf1a', SQ, 'flat', None, 'manual'),
 'about-hannah':              ('58dccf1a', HERO, 'flat', None, 'manual'),
 'hero-navy-chiffon':         ('1ca01fda', HERO, 'flat'),
 'sq-wedding-navy':           ('1ca01fda', SQ, 'flat'),
 'sq-plaid-green-bow':        ('69afd6a2', SQ, 'flat'),
 'sq-plaid-green-box':        ('878b2bd1', SQ, 'stand'),
 'sq-western-rose':           ('87fe1e52', SQ, 'flat'),
 'sq-camo-twine':             ('c0302a5a', SQ, 'flat'),
 'sq-christmas-gold-white':   ('f4c1d983', SQ, 'flat'),
 'sq-christmas-gold':         ('07cb3e95', SQ, 'flat'),
 'sq-vols':                   ('37879ab5', SQ, 'stand', (0.0, 0.05, 1.0, 0.98), 'isnet-general-use'),
 'sq-rainbow-dots':           ('7ca08313', SQ, 'flat'),
 'sq-rainbow-box':            ('c48b8f87', SQ, 'stand'),
 'sq-bee-bow':                ('f56cca68', SQ, 'flat'),
 'sq-bee-box':                ('da1763cf', SQ, 'stand'),
 'wide-holiday-display':      ('92c02b8d', LAND, 'stand'),
 'land-christmas-kraft':      ('970a07e7', LAND, 'stand', (0.0, 0.0, 0.89, 1.0)),
 'land-candy-cane-display':   ('a542f86b', LAND, 'stand'),
 'sq-pompom-stack':           ('3e538245', SQ, 'stand'),
 'sq-snowflake-bow':          ('4a690134', SQ, 'stand'),
 'sq-snowflake-just-for-you': ('05e247a1', SQ, 'stand'),
 'sq-snowflake-cube':         ('9de4b6e4', SQ, 'stand'),
 'land-christmas-stack':      ('f2f3b58f', LAND, 'stand'),
 'sq-special-delivery':       ('79d25bb7', SQ, 'stand'),
 'sq-nutcracker':             ('fab08a38', SQ, 'stand'),
 'land-colorful-trees':       ('9bceeace', LAND, 'stand'),
 'sq-dad-shirt':              ('5b6286ca', SQ, 'stand'),
 'sq-baby-shower':            ('95116a58', SQ, 'stand'),
}
ONLY = sys.argv[1:]
_sess = None
def sess():
    global _sess
    if _sess is None: _sess = new_session('birefnet-general')
    return _sess

def find(uid): return next(U.glob(uid + '*'))

_sessions = {}
def sess_for(model):
    if model not in _sessions: _sessions[model] = new_session(model)
    return _sessions[model]

def cutout(uid, crop=None, model='birefnet-general'):
    tag = uid + ('' if crop is None else '_c' + '-'.join(f'{v:.2f}' for v in crop)) + ('' if model == 'birefnet-general' else '_' + model)
    f = CUT / (tag + '.png')
    if f.exists(): return Image.open(f).convert('RGBA')
    im = ImageOps.exif_transpose(Image.open(find(uid))).convert('RGB')
    if crop:
        l, t, r, b = crop; W, H = im.size
        im = im.crop((int(l*W), int(t*H), int(r*W), int(b*H)))
    im.thumbnail((2000, 2000), Image.LANCZOS)
    out = remove(im, session=sess_for(model))
    out.save(f); return out

def best_angle(alpha):
    """rotation (deg) that minimises the bounding box of the silhouette - squares a top-down box to the frame"""
    a = alpha.copy(); a.thumbnail((400, 400)); best = (0, 1e18)
    for i in range(-180, 181):
        ang = i*0.25; r = a.rotate(ang, expand=True, resample=Image.BILINEAR)
        bb = r.point(lambda v: 255 if v > 128 else 0).getbbox()
        if bb:
            area = (bb[2]-bb[0])*(bb[3]-bb[1])
            if area < best[1]: best = (ang, area)
    return best[0]

def square_up(rgba):
    """Perspective-correct a top-down shot so the box is a true rectangle.
    Finds the box body (mask opened to drop ribbon/mesh), fits a quadrilateral,
    and warps the whole cutout with that homography. Falls back to rotation."""
    import cv2
    a = np.asarray(rgba.split()[3]); m = (a > 128).astype(np.uint8)*255
    k = max(9, int(min(rgba.size)*0.05)) | 1
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    body = cv2.morphologyEx(m, cv2.MORPH_OPEN, ker)
    cnts, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts: return rgba, 'none'
    c = max(cnts, key=cv2.contourArea)
    if cv2.contourArea(c) < 0.15*m.size: return rgba, 'small'
    hull = cv2.convexHull(c); peri = cv2.arcLength(hull, True)
    quad = None
    for eps in (0.02, 0.03, 0.045, 0.06):
        ap = cv2.approxPolyDP(hull, eps*peri, True)
        if len(ap) == 4: quad = ap.reshape(4, 2).astype(np.float32); break
    if quad is None:
        quad = cv2.boxPoints(cv2.minAreaRect(c)).astype(np.float32)
    # order tl, tr, br, bl
    s = quad.sum(1); d = np.diff(quad, axis=1).ravel()
    tl, br = quad[np.argmin(s)], quad[np.argmax(s)]; tr, bl = quad[np.argmin(d)], quad[np.argmax(d)]
    src = np.array([tl, tr, br, bl], np.float32)
    w = (np.linalg.norm(tr-tl) + np.linalg.norm(br-bl))/2; h = (np.linalg.norm(bl-tl) + np.linalg.norm(br-tr))/2
    if w < 50 or h < 50: return rgba, 'degenerate'
    dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
    Hm = cv2.getPerspectiveTransform(src, dst)
    # keep everything (bows past the box edge): transform image corners, shift into view
    W0, H0 = rgba.size
    corners = np.array([[[0, 0]], [[W0, 0]], [[W0, H0]], [[0, H0]]], np.float32)
    tc = cv2.perspectiveTransform(corners, Hm).reshape(4, 2)
    minx, miny = np.floor(tc.min(0)); maxx, maxy = np.ceil(tc.max(0))
    T = np.array([[1, 0, -minx], [0, 1, -miny], [0, 0, 1]], np.float32)
    Hm = T @ Hm
    outw, outh = int(maxx-minx), int(maxy-miny)
    if outw*outh > 40_000_000 or outw < 100: return rgba, 'blowup'
    arr = np.asarray(rgba)
    warped = cv2.warpPerspective(arr, Hm, (outw, outh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return Image.fromarray(warped, 'RGBA'), f'quad w={w:.0f} h={h:.0f}'

def defringe(rgba):
    arr = np.asarray(rgba).astype(np.float32); rgb, al = arr[..., :3], arr[..., 3]/255.0
    pre = Image.fromarray((rgb*al[..., None]).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    ab = Image.fromarray((al*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    pre = np.asarray(pre).astype(np.float32); ab = np.asarray(ab).astype(np.float32)/255.0
    fill = pre/np.maximum(ab[..., None], 1e-3)
    w = np.clip((0.85 - al)/0.85, 0, 1)[..., None]
    rgb = rgb*(1-w) + fill*w
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al*255]).astype(np.uint8), 'RGBA')

def grade(rgba):
    rgba = defringe(rgba)
    arr = np.asarray(rgba).astype(np.float32); rgb, al = arr[..., :3], arr[..., 3]/255.0
    m = al > 0.97; px = rgb[m]
    if len(px) > 1000:
        lum = px.mean(1); top = px[lum >= np.percentile(lum, 98)]
        ref = top.mean(0); gain = ref.mean()/np.maximum(ref, 1); gain = 1 + (gain-1)*0.5
        rgb = np.clip(rgb*np.clip(gain, 0.9, 1.12), 0, 255)
        px = rgb[m]; lo, hi = np.percentile(px, 0.3), np.percentile(px, 99.7)
        rgb = np.clip((rgb - lo)*(255/max(hi-lo, 1)), 0, 255)
    x = rgb/255.0
    x = x + 0.05*np.sin(np.pi*x)*(1-x)
    x = 0.5 + 0.5*np.tanh(2.0*(x-0.5))/np.tanh(1.0)
    mx, mn = x.max(2, keepdims=True), x.min(2, keepdims=True); sat = mx-mn
    mean = x.mean(2, keepdims=True); x = mean + (x-mean)*(1 + 0.10*(1-sat))
    out = Image.fromarray(np.dstack([np.clip(x, 0, 1)*255, al*255]).astype(np.uint8), 'RGBA')
    r = out.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2)).convert('RGBA')
    r.putalpha(out.split()[3]); return r

def backdrop(w, h):
    yy, xx = np.mgrid[0:h, 0:w]; u, v = xx/w, yy/h
    base = np.array([247, 244, 239], np.float32)[None, None, :] * np.ones((h, w, 1), np.float32)
    light = np.exp(-(((u-0.5)/0.75)**2 + ((v-0.42)/0.75)**2))
    base = base*(0.955 + 0.055*light)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

def shadow_layer(W, H, a, x, y, sw, kind):
    if kind == 'flat':
        s = Image.new('L', (W, H), 0); s.paste(a, (x + int(sw*0.012), y + int(sw*0.02)))
        s = s.filter(ImageFilter.GaussianBlur(sw*0.028)).point(lambda v: int(v*0.30))
        t = Image.new('L', (W, H), 0); t.paste(a, (x + int(sw*0.004), y + int(sw*0.006)))
        t = t.filter(ImageFilter.GaussianBlur(sw*0.008)).point(lambda v: int(v*0.22))
        return ImageChops.lighter(s, t)
    sh = a.resize((a.width, max(1, int(a.height*0.18))), Image.BILINEAR)
    cast = Image.new('L', (W, H), 0); cast.paste(sh, (x, y + a.height - sh.height + int(sw*0.015)))
    cast = cast.filter(ImageFilter.GaussianBlur(sw*0.035)).point(lambda v: int(v*0.30))
    ew, eh = int(a.width*0.98), int(sw*0.06)
    ell = Image.new('L', (ew, eh), 0); ImageDraw.Draw(ell).ellipse((0, 0, ew-1, eh-1), fill=255)
    con = Image.new('L', (W, H), 0); con.paste(ell, (x + (a.width-ew)//2, y + a.height - eh//2 - int(sw*0.004)))
    con = con.filter(ImageFilter.GaussianBlur(sw*0.014)).point(lambda v: int(v*0.45))
    return ImageChops.lighter(cast, con)

def compose(name, uid, canvas, kind, crop=None, model='birefnet-general'):
    sub = cutout(uid, crop, model)
    if kind == 'flat':
        sub, how = square_up(sub)
        if not how.startswith('quad'):
            ang = best_angle(sub.split()[3]); ang = ((ang + 45) % 90) - 45
            if abs(ang) > 0.3: sub = sub.rotate(ang, expand=True, resample=Image.BICUBIC)
        print('  square_up:', how, flush=True)
    bb = sub.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox(); sub = sub.crop(bb)
    sub = grade(sub)
    W, H = canvas; pad = 0.09
    maxw, maxh = W*(1-2*pad), H*(1-2*pad)
    sc = min(maxw/sub.width, maxh/sub.height)
    sub = sub.resize((max(1, int(sub.width*sc)), max(1, int(sub.height*sc))), Image.LANCZOS)
    x = (W - sub.width)//2
    y = (H - sub.height)//2 if kind == 'flat' else int(H*(1-pad)) - sub.height - int(H*0.03)
    bg = backdrop(W, H)
    a = sub.split()[3]
    shade = shadow_layer(W, H, a, x, y, sub.width, kind)
    dark = Image.new('RGB', (W, H), (92, 78, 66))
    bg = Image.composite(dark, bg, shade)
    bg.paste(sub, (x, y), sub)
    bg.save(OUT / f'{name}.png', optimize=True)
    print('wrote', name, canvas, kind, flush=True)

for name, spec in SPECS.items():
    if ONLY and name not in ONLY: continue
    compose(name, *spec)
