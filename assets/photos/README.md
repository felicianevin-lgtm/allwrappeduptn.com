# Photos

Every image here is a real order wrapped by Amiebeth. The phone originals live in
`G:\My Drive\All Wrapped Up\Originals`. `studio.py` (with `stub.py` beside it) turns an
original into the studio shot used on the site:

1. Cutout with BiRefNet (`rembg`, model `birefnet-general`); `stub.py` fakes the
   `pymatting` import that Windows app-control blocks. Per-photo crops and alternate
   models are set in `SPECS`; a hand-drawn outline can be dropped in as
   `cut/<uid>_manual.png` for boxes the model refuses (dark box on dark wood).
2. Top-down shots (`flat`) are perspective-corrected so the box is a true rectangle;
   standing shots (`stand`) are left as photographed.
3. Placed on a warm-white seamless backdrop with a soft shadow made from the gift's own
   silhouette, a light colour grade, and exported as 1200-square, 1200x1500 (hero) or
   1400x933 (landscape).

Run `python studio.py` (all) or `python studio.py sq-flamingo` (one) from this folder,
then export PNG to WebP at quality 84.

Tips for new originals: a plain surface that contrasts with the paper (a white sheet
under a dark gift, a dark table under a light one), shoot straight down or straight on,
and leave room around the bow. Wood-grain paper on a wood table and black paper on a dark
table are the two cases the cutout cannot separate.
