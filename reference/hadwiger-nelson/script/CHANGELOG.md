# Script changelog: script_synth.json → script.json

**Result:** 11 scenes, 65 paragraphs, 140 sentences, **1,449 spoken words** (cap 1,450). The estimate is **about 9:54** at `--speed 0.83` with `SENT_GAP = 0.55`. The same timing model gives 9:38 for the old draft, and the pacing review measured 9:37.6, so the model is calibrated. Every scene is estimated at 38–87 s. The validator reports no errors and no warnings. It checks the spec rules plus these extra rules: 1–4 sentences per paragraph, 1–5 bookmarks per paragraph, no bookmark at the end of a sentence, every bookmark used in its paragraph's `visual`, no `visual` that references a bookmark from another paragraph, and a URL for every fact.

| Scene | Words | Estimate (s) |
|---|---|---|
| S01_Hook | 93 | 38.5 |
| S02_Rule | 125 | 51.4 |
| S03_Line | 101 | 42.0 |
| S04_Triangle | 144 | 59.7 |
| S05_Diamond | 121 | 49.8 |
| S06_Spindle | 210 | 86.8 |
| S07_Hexagons | 152 | 62.4 |
| S08_Stall | 119 | 48.5 |
| S09_Breakthrough | 144 | 57.1 |
| S10_Check | 121 | 48.8 |
| S11_Today | 119 | 48.7 |

S06 is close to the 90 s limit. Do not add words to it.

---

## Changes that must be made outside the script (engine and build)

The script cannot fix these. Do them before generating any timeline.

1. **Speed (pacing BLOCKER 1).** Render with `--speed 0.83`. At 1.0 the video is too short: 8:36 for the old draft. Avoid 0.8: it drops to 161 wpm and leaves no headroom.
2. **Sentence gap.** Raise `SENT_GAP` in `tools/timeline.py` from 0.45 to 0.55 s. The 9:54 estimate assumes this.
3. **build.sh (pacing BLOCKER 2).** It runs `timeline.py` at the default speed of 1.0. Pass `--speed 0.83`, or change the default. Generate the timelines once, at that speed, before anyone animates.
4. **Jaan.** Add `"Jaan": "/jˈɑn/"` to `PRON` in `tools/timeline.py`. Without it, Whisper hears "John Parts".
5. **Final tail.** Allow a 2.0 s tail for the last scene (S11): a 1.2 s hold, then a 0.8 s fade. The S11 P6 storyboard also gives a fallback in case the engine stays at 0.9 s.

---

## Fact review (review_facts.md)

| Item | Action |
|---|---|
| 1. S11 "To prove six" logic error (mandatory) | **Fixed.** Now reads "To push the five up to six, you'd need a trap five colors can't escape." This is the reviewer's alternative wording. It mirrors S08's "To push the four up" and fixes clarity M7's ambiguity too. |
| 2. S07 "pack tighter" misleading (mandatory) | **Fixed.** Now reads "Hexagons are rounder, so they {#cover} cover more area for their width." The storyboard now shows a square and a hexagon inscribed in the same 0.90 circle (0.65·d² vs 0.50·d², checked). |
| 3. S07 "every other blue hexagon" ambiguous (mandatory) | **Fixed.** Now reads "all other blue hexagons are". |
| 4. S08 Hadwiger naming reason (mandatory) | **Fixed differently.** Instead of adding a longer reason, I removed the causal claim: "It's called the Hadwiger Nelson problem, after Nelson and the Swiss mathematician Hugo Hadwiger." It is accurate, 4 words shorter, and says the name first. The 1945 and 1961 details are in `facts`. |
| 5. S11 thin band rests on a preprint | **Moot.** S11 P4 is cut (see clarity M10). Its fact entry is removed. |
| 6. S09 "built from" → "packed with Moser spindles" | **Applied.** It is part of the H8 rewrite. |
| 7. S04 "So for now…" (optional) | **Applied** as "For now, forget the plane…". This fixes the overclaim that dots and sticks are all you need. |
| 8. "He was a biologist" tense | **Kept.** Both reviewers agree it is acceptable. |
| Visual 1. Anachronistic spindle icon at 1950 | **Fixed.** A plain "at least 4" tag at 1950. An optional spindle icon appears at the 1961 tick. |
| Visual 2. "about 13 wheels" reads as graph J | **Fixed.** "Do NOT label or show a specific count." |
| Visual 3. S06 coordinates | **Fixed.** y ≈ 0.99 and 2.79, with the instruction to use `geom` values. |
| Visual 4. Random mosaic floor is not a valid coloring | **Fixed.** S01 marks the mosaic as an illustration with hand-picked landings. The S11 finale floor morphs into Isbell's hexagon pattern, so the final GOOD checks are honest. |
| Visual 5. Flat-top vs pointy-top | **Fixed.** S07 now says to use `hex_cells`' pointy-top orientation. |
| Pronunciation. Hadwiger vowel | **Note corrected.** The engine says HAD-vig-er. The note now gives `/hˈɑːdvɪɡəɹ/` if HAHD is wanted. |

## Clarity review (review_clarity.md)

| Item | Action |
|---|---|
| H1. S06 P4 abstract | **Applied with changes.** The colors are named: "Say the bottom tip is pink. The first diamond's middle dots take blue and yellow, so its top tip gets the leftover: pink. The second diamond goes the same way, but the new stick rules out pink." The last sentence now gives the missing reason (pink is the only option left, and the stick forbids it). It is 13 words shorter than the reviewer's version, which S06's length requires. |
| H2. New stick not justified, "Its" unclear | **Applied.** "The copy's top tip drifts away from the ring's center, until it lands on the ring. Stop there: the tips are exactly one unit apart, so join them." |
| H3. No goal before the construction | **Applied.** P1 now opens with "The plan: force two dots to match, then join them with a stick." P7 is shortened to the callback "Force a match, then forbid it." Plan labels appear on screen. |
| H4. The stick rule is never stated | **Applied with changes.** "…study dots and sticks, with a stick wherever two dots are one unit apart. If a drawing can't be colored with two colors, it's a trap: the plane can't be either." I used "two colors" instead of "say, three" so the sentence matches the triangle on screen. "The plane can't be either" replaces "neither can the plane" because it is easier to follow by ear. |
| H5. Unit size never explained | **Applied.** New S02 P4: "The unit can be an inch or a mile: zooming doesn't change the puzzle." |
| H6. "The plane" undefined; S01 P5 generic | **Applied.** S01 P5 is cut, and its fade-out moves to the P4 tail. S03 P4 now says "…across the whole floor, which mathematicians call {#plane} the plane." |
| H7. "Squares… nine colors" is a leap | **Applied.** The storyboard is reordered: square, then {#apart} with the 1.33 gap, then {#block} for the tiling. |
| H8. S09 referent chain | **Applied.** Uses the names "forcer" and "blocker", "every other dot around the rim", and "that's allowed: no sticks join them". |
| M1. S08 "rule a number out" | **Applied with changes.** I kept "**one finite** trap" against "the **endless** plane", because that contrast is the point of the scene. |
| M2. Nelson vs Mosers: who was first | **Applied.** "…already knew in nineteen fifty that four were needed…" ("from the start" dropped for budget). |
| M3–M6, M8, M9 | **Applied.** M5 is phrased as a hypothetical ("If shorter distances were banned too… would clash"), so it cannot be heard as the real rule. M6 drops the spoken axiom hedge; the "with the usual axioms" tag stays on screen. M8 uses the pacing reviewer's version of the same line. |
| M7. S11 "prove six", forty-two dots | **Applied.** See fact item 1. "Forty-two dots" is no longer spoken, because right after 509 it sounds small. |
| M10. Cut S11 P4 | **Applied.** It saves 27 words, removes the preprint claim and the double meaning of "exactly", and lets the ending reach its callback sooner. |
| M11. Visuals outrunning the voice | **Applied.** Two landings only in S04 P5 and S06 P6, and the S09 fly-in finishes before {#blocked}. |
| L1–L4 | **Applied.** L1 uses the reviewer's shorter merge. L3 is inside the rewritten S06 P5. |
| L5 "Let's keep score" | **Rejected (budget).** The question at {#board} already narrates the bar's arrival. |
| L6 "making it easier to check" | **Rejected (budget).** |
| L7 "any patchwork of polygons" | **Rejected (accuracy).** "Ordinary" is the honest hedge for Sokolov–Voronov's locally finite polygonal maps, and "any" would overstate the result. |
| Budget line: drop "Swiss mathematician" | **Rejected.** Fact item 4 already restructured the sentence, and it stays short. |

## Pacing review (review_pacing.md)

| Item | Action |
|---|---|
| Blockers 1 and 2 | Outside the script (see the list above). The pacing note in `pronunciation_notes` is replaced with the measured numbers. |
| S04 P5 thin beat | **Applied.** New sentence: "With two colors, wherever they land, {#match} two of them match." I added "With two colors" for accuracy, because pigeonhole only works for two. Two landings. Pause 1.0. |
| S08 P6 thin beat | **Applied.** "Every shape they tried {#tried} still worked with four colors." |
| S06 P5 thin beat | **Applied in a tighter form.** "It's the diamond rule, {#twice} twice. {#both_tips} Both top tips must match {#bottom_tip} the bottom tip, so {#same} they match each other." The two arcs now get about 2 s, instead of the separate tip1/tip2 sentences. That saves 8 words. |
| S06 P3, S04 P1, S07 P2, S09 P6, S01 P2, S06 P1 | **Applied as specified.** S06 P3: no numbering, sweeps, {#crossings}. S04 P1: split into two questions, pause 1.0. S07 P2: no blob. S09 P6: no magnifier. S01 P2: one re-landing, pause 1.0. S06 P1: split, with the H3 plan line added. |
| S07 P6 reveal clamped | **Applied.** "So {#seven} seven colors are always enough." is its own paragraph (1.2), and Isbell is P7, with {#isbell} before "John". |
| S11 final tail | Outside the script (item 5). The storyboard gives both variants. |
| Camera moves under the BoundsBar | **Applied everywhere.** The global camera rule is in the S01 P4 storyboard. S01, S02, S04, S06, S07, S10 and S11 now scale the content group instead of moving the camera. S03 has no bar and may keep its camera zoom. |
| MED 3. Frozen picture | **Applied.** New bookmarks: {#angle}, {#brothers}, {#year}, {#cover}, {#hunt} and {#fifth} (instead of {#rules}, because the spoken hedge is gone), {#bio}, {#six}, {#four}. S11 {#near} is moot. |
| MED 4. Mid-sentence triggers | **Applied.** {#spin}, which starts the one sweep that draws the ring; {#clever}; {#crossings}; {#slack}, which replaces {#room}; S11 {#five}, {#six}, {#seven}. |
| MED 5. Late bookmarks | **All moved:** {#nelson}, {#hadwiger}, {#rings} and {#overlap}, {#one} and {#fails}, {#forbids} (plus a new {#blocker}), {#nowhere}, {#nblue} and {#nyellow}, {#both} and {#far}. |
| MED 6. Hard-to-hear sentences | **Applied.** S05 P5 uses clarity L1's shorter merge instead of the pacing version. |
| MED 7. Silent pause visuals | **Applied.** S02 P2 has no recolor. The S10 P5 counter holds at 874, and 553 is not shown. |
| MED 8. Question pauses | **Applied:** 1.2, 1.3 and 1.2. No non-final pause is above 1.4. |
| LOW items | **All applied:** S03 ring geometry (fade off the line; no squash), olive and brown square tints, purple wheel center (coloring re-checked as valid), no "→" glyph (also removed from S04's caption), S05 plain fade, `unit_web(n_points=3000, lattice_r=5)`, S10 captions "SAT solver 1 / SAT solver 2 / edge lengths checked" (backed by Aaronson and Phillips; the fact was added), S06 coordinates. |

## Other changes

- **Bookmark names contain no digits**, so a "no digits" check passes on the raw text too. Renames: ring1/ring2 → first_ring/second_ring, top1 → first_top, y1970/y1990/y2010 → seventy/ninety/twenty_ten, n874 → shrunk, n509 → record, S11 P2 six → trap_six.
- **S10 P6** is now "**In** twenty twenty, Jaan Parts found…", because "By… found" is ungrammatical. Parts posted the graph in March 2020.
- **S11 P1** drops "and we still don't know which" (budget). P5's either/or line carries that idea.
- **Last-paragraph pauses** are written as 0.9, the engine's real tail clamp, except S11's final 1.4.
- **Facts:**
  - Updated: Hadwiger naming, hexagon area, border slack, dots and sticks as unit-distance graphs, the S06 walk-through, the wheel, forcer and blocker, "every shape tried was four-colorable", Parts 2020, and six colors not known.
  - Added: unit size (scaling), pigeonhole for the two-color triangle, the Phillips edge check.
  - Removed: the thin-band claim.
  - Every fact now has a URL.
- **Purposes** updated for S03, S04, S06, S07, S08, S09, S10 and S11 to match the new narration.
