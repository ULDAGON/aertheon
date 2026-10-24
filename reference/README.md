# reference/

Source of the two finished AERTHEON videos, kept as the style reference for new ones. Read them; never build in them.

## Folders
- `hadwiger-nelson/`: the pilot and **gold standard** (v2, 11 scenes, 9:41). Predates the template: `PRON` lives in
  `tools/timeline.py`, topic helpers (`stick`, `BoundsBar`) live in `common.py`, `geom.py` replaces `topic.py`.
  `scenes/s04_triangle_geo.py` is a helper of `S04_Triangle`, not a scene.
- `riemann-hypothesis/`: the second video, made with this engine (11 scenes, 9:40). `topic.py` (numerics, shared layouts,
  `ErrorDial` motif), `brief.md`, `SCENE_GUIDE.md` with the 'This video' section, `thumbnail/`.
- Each `script/` holds the research, drafts, reviews, `CHANGELOG.md`, `script_synth.json` (synthesis before the critic
  fixes) and **`script.json` (the final, voiced script; the format example `SCRIPT_FORMAT.md` points to)**.
  `riemann-hypothesis/script/build_final.py` is the finalize pattern: it loads `script_synth.json`, applies every critic
  fix through asserting helpers and writes `script.json` (verified: reproduces it byte for byte).
- `*/thumbnail/`: `make_thumbnail.py` (final design) and its rendered `.png`/`.svg`. These are the only images kept.

## Not kept
- Rendered media: no `out/`, `media/`, `audio/`, `timeline/`, previews, QA images or final `.mp4`.
- `riemann-hypothesis/data/` (zeta zeros, wave caches): `topic.py` loads `data/zeros.json` and `data/*.npy`, so it does
  not import here. In a video, `python topic.py --precompute` fills `data/`.
- Venv links (`.venv`, `tts/.venv`). RH has no `build.sh`, `tools/` or `tts/` copy: it ran the template's versions.

## Known gaps
- Code is final-state except for **HN `s02_rule` and RH `s02_gauss`, `s03_coinflips`, `s08_onehalf`**, which may lack
  their last fix. Treat them as near-final, not as proof of a rule.
- `riemann-hypothesis/script/draft_C_visual.json` is truncated (ends inside `facts`) and does not parse as JSON.
- HN `script/script_synth.json` predates the bookmark rule (digits in `{#ring1}`, `{#y1970}`, ...): the validator reports
  ERRORs on it. Both `script.json` files pass `template/tools/validate_script.py`.

## Rules
- Never run `render.sh`, `timeline.py`, `build.sh`, `topic.py --precompute` or manim inside `reference/`. Copy a file into a
  video folder (`<videos>/<slug>/`, see `PIPELINE.md`) or into the scratchpad first.
- Do not edit these files to match later engine changes; new rules go into `template/` and the docs.
