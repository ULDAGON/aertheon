# Thumbnails

Every video gets **three** 1280×720 thumbnails in the AERTHEON **pastel** channel style (the light, soft twin of the dark
video), in `$P/thumbnails/` (the video folder's top level, next to the mp4), so the user can pick one or A/B test them
on YouTube. Each pairs with one of the three titles in `$P/youtube.md` (`YOUTUBE.md`).
References (single-thumbnail scripts from before the three-thumbnail layout, still the style reference): `$E/reference/hadwiger-nelson/thumbnail/` and `reference/riemann-hypothesis/thumbnail/` (scripts plus their rendered `*_thumbnail.png`: Read the PNGs; never run the reference scripts, they write into the engine). Channel banner and profile picture:
`$E/branding/` (`python3 make_branding.py` rebuilds them). All tokens and SVG helpers live in `$E/branding/brand.py`.

## Layout (from the reference)
- **Background:** diagonal gradient `CREAM #FCF8F3` → `LAVENDER #EFEAF8` (`background()`).
- **Left ~55 %: the key visual** of the video, drawn in `PASTEL` (pastel twins of the video palette, same order:
  `#A9D3F7 #F9E1A0 #F6B6D4 #B6E2BB #D3C0F8 #F8CBA1 #A6E8DF`). Shapes have small gaps between them (4–6 px inset) and fade out
  toward the edges through opacity with a little random jitter. One **focal element** is outlined in `INK #3A3D5C` (stroke ~8–12,
  with a wide `CREAM` halo underneath) so it pops: in the reference, the unit stick whose two ends sit on different colours,
  with an italic Palatino "1".
- **Right: the hook text**, centred at x ≈ 975. Headline in two short lines of uppercase Avenir Next, weight 800, size ~82,
  `INK` (`headline()`), e.g. "HOW MANY / COLORS?". Below it one bold tension element (the reference: three pastel hexagons with
  "5 6 7" at size 112, weight 800). At the bottom a lowercase subline, weight 600, size 36, letter-spacing 3, `INK_SOFT #8E8AA8`
  (`subline()`), e.g. "nobody knows which".
- Only these fonts: Avenir Next, Palatino. At most ~6 words of text in total.
- The second video (RH) shows the variant: a pastel prime staircase as polyline riser + tread (stroke 17, round caps),
  `INK` R(x) curve width 9 on a `CREAM` halo width 20; "HOW RANDOM / ARE PRIMES?" at size 70, x = 985; hexagons "0 ½ 1" with
  only ½ lit; subline "the riemann hypothesis".

## Three thumbnails
- Three **different concepts**, not recolours or crops of one picture. Each one is a different way into the same video,
  and each is paired with one title suggestion (deliver the three titles with them). Good spread:
  1. **The hook question**: the opening image and the plain question (e.g. "WHAT IS / A HASH?").
  2. **The surprise**: the mechanism or number that makes the video worth watching (e.g. "CHANGE ONE / LETTER", "263 / 512").
  3. **The stakes or open question**: what is unknown, impossible or at risk (e.g. "FIND A / TWIN?", "2²⁵⁶ tries").
- All three follow every rule below: same palette, fonts, layout grid (headline x ≈ 975), ≤ ~6 words, one INK focal element,
  honest. Reuse the video's motif across them so they read as one family.
- One script, `$V/thumbnails/make_thumbnails.py` (in `src/`), with shared helpers and one function per variant; it writes
  the PNGs to `$P/thumbnails/<name>_thumbnail_1.png` … `_3.png` and keeps the `.svg` sources next to itself in `src/`.
  The first is the default if the user picks none.

## Lessons
- The focal art fills the whole left ~55 %, corners included (RH left its upper-left corner empty: a known weakness).
- Bold strokes (~17 px) and shapes, not thin lines or faint fills; they must survive 320×180.
- Long headline words may drop to size ~70; the headline must clear the right edge by ≥ 40 px (HN went 88 → 82, x 987 → 975).
- Keep the bottom-right corner clear: YouTube's duration badge covers it.

## Rules
- Honest: the picture must be true to the video's content. Assert it in code (the reference asserts that the stick's ends land
  on different colours).
- Readable small: after rendering, Read each PNG and a 320×180 strip of all three, inside `$V` (never `/tmp` or the engine):
  `ffmpeg -y -i ../thumbnails/<name>_thumbnail_1.png -i ../thumbnails/<name>_thumbnail_2.png -i ../thumbnails/<name>_thumbnail_3.png
  -filter_complex "[0]scale=320:180[a];[1]scale=320:180[b];[2]scale=320:180[c];[a][b][c]hstack=3" out/thumbs_small.png`;
  every headline and focal element must still read.
- Build: fill in `$V/thumbnails/make_thumbnails.py` (scaffolded with every video), then
  `cd $V && python3 thumbnails/make_thumbnails.py`; if it imports numpy, mpmath or `topic`, use the video's venv:
  `.venv/bin/python thumbnails/make_thumbnails.py`. Outputs `$P/thumbnails/<name>_thumbnail_{1,2,3}.png` (the `.svg`
  sources stay in `$V/thumbnails/`).
- When: during the scenes workflow (PIPELINE step 6), when the motif and key visual are settled.
