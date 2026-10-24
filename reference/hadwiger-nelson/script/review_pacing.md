# Review: TTS, pacing and animation for script_synth.json

**Reviewer role:** TTS, pacing and animation critic.

**Method.** I measured everything below; nothing is estimated from words per minute. I ran a scratch copy of `tools/timeline.py` on `script_synth.json` with Kokoro af_heart, the same per-sentence TTS, trim, gaps and clamps, and Whisper word alignment. That gave the real bookmark times. I also ran TTS-only passes at other speeds, checked the phonemes with misaki plus espeak, ran Whisper with no prompt to check the names, and ran the QA silence detector on the scene WAVs.

## What already passes

| Check | Result |
|---|---|
| Spoken words | 1,440, inside 1,350–1,450 |
| Scenes | 11 scenes, 94–200 words each |
| Sentence length | No sentence over 24 words. The longest are 21: S06 P4 s1 and S11 P4 s2. |
| Text hygiene | No digits, symbols, parentheses or dashes in the narration |
| Bookmarks | 1–5 per paragraph, all unique |
| `pause_after` | Every value is within 0.6–1.4 |
| Whisper | Matched every sentence, 0 similarity warnings |
| Hard-to-say lines | Short lines ("Just one.", "Why so stuck?", "cleverer") render cleanly |
| Names | Moser → mˈOzəɹ, "de" → də, Hadwiger heard as "Hadviger", Bruijn heard as "de Brown". All correct. |

---

## BLOCKER

### 1. At the planned speed the video is too short, and the pacing note is wrong

The script's `pronunciation_notes` claim that `--speed 0.9` gives about 9.8 min. It gives 9:03. Kokoro af_heart is much faster than the planned 160–174 wpm.

| `--speed` | Speech wpm | Total (engine pacing, current script) | Shortest scene |
|---|---|---|---|
| 1.0 (engine default, used by `build.sh`) | 203 | **8:35.8** | S03 34.5 s, below the 35 s floor |
| 0.9 | 191 | **9:02.9** | 36.3 s |
| 0.85 | 181 | 9:26.7 | 37.9 s |
| **0.83** | 177 | **9:37.6** | 38.5 s |
| 0.8 | 161 | 10:28.5 | 41.7 s (non-linear jump, no headroom) |

**Fix:**
- Render with `--speed 0.83`. Also raise `SENT_GAP` from 0.45 to 0.55 s: that adds 6.8 s over the 68 sentence gaps, and it answers the user's "breaks between sentences" complaint directly.
- With the text edits below (net +7 words, three extra paragraph and sentence breaks), I estimate about 9:45–9:50, and every scene stays in 38–80 s.
- Avoid 0.8. It jumps to 161 wpm and leaves no room.
- Replace the "Pacing" note with these measured numbers.
- Listen to 2–3 sentences at 0.83 before committing.

### 2. `build.sh` renders at speed 1.0

`build.sh` calls `tools/timeline.py` with no `--speed`, so it uses the default of 1.0. The TTS cache key includes the speed. A full build would therefore synthesize new audio at a different speed and rewrite every `timeline/*.json` after the animators have scheduled against them. Every mark would shift, and QA would fail with "late mark" and overrun errors.

**Fix:** Change the default in `timeline.py` to the chosen speed, or pass `--speed 0.83` in `build.sh`. Generate the timelines once, at that speed, before any scene is animated.

---

## HIGH: beats with too little narration time

These beats will spill into silence (the "animation without voice" failure) or look rushed. All times are measured at speed 0.9. At 0.83 they are about 8% longer, which is still not enough.

| Where | Measured time available | What the storyboard puts there | Concrete fix |
|---|---|---|---|
| **S04 P5** | 2.8 s, from `{#these}` (32.0 s) to P6 (34.8 s) | Mosaic fades in, camera zooms out, 3 glides with color sampling and BAD flashes. The flashes are also never narrated. | Add a sentence: **"Wherever they land, {#match} two of them share a color."** First glide at the start of that sentence, first BAD flash at `{#match}`, second landing before the pause. Drop the third landing. Pause 0.8 → 1.0. |
| **S08 P6** | 1.8 s, from `{#find}` (44.5 s) to the end of the scene, including the fade-out | 4 candidate shapes, 4 "4 colors work" badges, the marker reaching 2017 | Add **"Every shape they tried {#tried} still worked with four colors."** Shapes appear at `{#find}`, badges at `{#tried}`, and the tail is only the fade. This also narrates the badges, which are currently silent. |
| **S06 P5** | 1.0 s, from `{#twice}` (43.6 s) to the next sentence (44.6 s) | Two diamond highlights and two dashed `=` arcs in turn | Replace s2–s3 with **"It's the diamond rule, {#twice} used twice. {#tip1} The first top tip must match the bottom, {#tip2} and so must the second. So {#same} they match each other."** Map: `{#tip1}` = first arc, D turns pink. `{#tip2}` = second arc, D2 turns pink. `{#same}` = the D–D2 `=`. Keep s4 `{#clash}` as it is. |
| **S06 P3** | "Seven dots," lasts 0.6 s. "eleven sticks" lasts 0.7 s. | Numeric labels 1–7 on the dots, sticks ticked 1–11, "not a dot" tags | Drop the per-item numbering. Flash the dots in a lagged sweep at the paragraph start and the sticks in a sweep at `{#count}`, and build the counter "7 dots · 11 sticks". Add **`{#crossings}`** before "crossings" for the "not a dot" tags. |
| **S04 P1** | 1.6 s after "something cleverer" (starts at 4.5 s), including the pause | Morph to blobs, stick lands, BAD flash, then the pattern fades | Split the sentence: **"Maybe {#checker} a checkerboard? {#clever} Or something cleverer?"** This buys one more sentence gap. Pause 0.8 → 1.0. The blob landing happens at `{#clever}`, and the fade overlaps "Here's why…". |
| **S07 P2** | 3.2 s, from `{#small}` to `{#block}` | Blob, 2 stick attempts, morph to a square, diagonal, readout 0.94 | Cut the blob. At `{#small}` show the 2/3 square directly: the stick tries one angle and pokes out, then the diagonal "0.94" and the stick "1" appear. The 3×3 block comes at `{#block}` as now. |
| **S09 P6** | 1.6 s after `{#trim}`, then only the 0.9 s tail | Countdown to 1,581, inset magnifier, then the fade | Drop the magnifier. Show the "illustration" tag at `{#big}`. Finish the countdown before the sentence ends. The tail is only the fade. |
| **S01 P2** | 2.1 s after `{#always}` (17.6 s), including the 0.8 s pause | Two further lift, glide and land moves, each with a check | Do one re-landing at `{#always}`. In the pause, only pulse the check. Pause 0.8 → 1.0. |
| **S06 P1** | The diamond appears in the 0.3 s lead-in and `{#copy}` fires at 0.8 s | Bar, badge and tilted diamond, then the copy lifts off almost at once | Split the sentence: **"Take the diamond and {#copy} copy it, hinged at the bottom tip {#scissors} like scissors. Then draw {#ring} the ring around its top tip."** The diamond gets about 1 s on its own, and there is a breath before the ring. |

## HIGH: the two reveals at the ends of scenes are clamped by the engine

In `timeline.py`, the last paragraph of each scene uses `TAIL_MAX = 0.9`, and that tail also has to hold the fade-out.

- **S07 P6.** It asks for 1.2 s after "Seven colors are always enough", but gets 0.9 s including the fade, so there is no hold on the ≤7 reveal. **Fix, no extra cost:**
  - Make it two paragraphs.
  - P6: **"So {#seven} seven colors are always enough."** with pause 1.2.
  - P7: **"{#isbell} John Isbell, Nelson's twenty-year-old friend, found this in nineteen fifty."** with pause 0.9, followed by the fade.
  - Also move `{#isbell}` before "John" so the caption appears with the name.
- **S11 P7.** The final line asks for 1.4 s and gets 0.9 s including the fade to black. This ending is too abrupt. **Fix (engine change for the orchestrator):** allow the last scene a tail of 2.0 s: a static 1.2 s hold, then a 0.8 s fade. QA ignores silence at the end of a file, and 0.8 s of motion is under the 1.6 s limit.

## HIGH: camera moves while the BoundsBar is on screen

`TimedScene` is a `MovingCameraScene`, but `BoundsBar` is a plain VGroup in scene coordinates. Any zoom therefore shrinks, grows or moves the scoreboard.

Affected beats:
- **S04 P5:** zoom out with the bar visible.
- **S07 P5:** zoom to the point where three hexagons meet (the bar leaves the frame).
- **S10 P2:** zoom into the web.
- **S11 P7:** pull back over the floor while "5 6 7" glows.
- **S01 P1 and S02 P6:** the camera is already zoomed (1.25× and 2.2×) when the bar fades in. The home position `to_edge(DOWN)` is then wrong.

**Fix:**
- Preferred: in any scene that shows the bar, do not move the camera. Scale or shift the content group about a point instead.
- Otherwise: add a shared helper that pins the bar to `self.camera.frame` with an updater that sets its width and bottom position relative to the frame.
- For S01 and S02, create the bar only after the camera has returned to 1.0, or place it relative to the frame.

---

## MEDIUM

### 3. Picture likely frozen for more than 5 s while speaking (QA WARN)

These are measured gaps with no scheduled visual trigger. Add one bookmark to each and give it a small, meaningful change.

| Where | Measured gap | New bookmark and what changes there |
|---|---|---|
| S01 P2 | 5.6 s, `{#stick}` → `{#differ}` | "anywhere, {#angle} at any angle": the stick rotates in place |
| S06 P7 | 6.4 s, `{#moser}` → `{#force}` | "by the brothers {#brothers} Leo and William Moser in {#y1961} nineteen sixty-one": caption, then "1961" |
| S07 P3 | 5.5 s, `{#hex}` → `{#corner}` | "so they {#tighter} pack tighter": the square overlay comparison |
| S08 P5 | 7.3 s, `{#dbe}` → `{#finite}` | "{#rules} Under the standard rules…": the "usual axioms" tag. "if the plane {#fifth} needs a fifth color": the 5 on the bar glows. |
| S09 P1 | 5.2 s, `{#degrey}` → `{#hobby}` | "He was {#bio} a biologist": the tag's first half |
| S09 P3 | 7.6 s, `{#wheel}` → `{#triple}` | "a dot with {#six} six others": the rim dots. "{#four} With four colors": the swatches. |
| S11 P4 | 5.5 s, `{#band}` → `{#seven}` | "forbidding distances {#near} near one too": the annulus label |

### 4. Mid-sentence "On '…'" triggers need real bookmarks

Animators can only schedule against marks. These triggers fall mid-sentence and have none:

| Where | Add |
|---|---|
| S02 P5 "spin a stick" | `{#spin}`. The sweep should start at `{#spin}` and be the same motion that traces the ring at `{#ring}`. The storyboard currently lists these as two separate events. |
| S04 P1 "something cleverer" | `{#clever}` (see the table above) |
| S06 P3 "crossings don't matter" | `{#crossings}` |
| S07 P5 "with room to spare" | `{#room}` |
| S08 P5 "standard rules" | `{#rules}` |
| S11 P1 "5, 6 and 7 pulse as spoken" | `{#six}` and `{#seven}`, next to the existing `{#board}` before "five" |

### 5. Bookmarks placed after the word they illustrate

| Where | Move to |
|---|---|
| S01 P3 `{#nelson}` | before "Edward" |
| S08 P2 `{#hadwiger}` | before "Hugo" |
| S11 P4 `{#exactly}` | before the final word "exactly" |
| S02 P6 `{#rings}` | before "Every point has its own ring", plus a new `{#overlap}` before "overlap" |
| S03 P2 | "{#one} One color {#fails} fails at once": the line turns blue on "One color" and the stick drops on "fails" |
| S09 P4 | "{#spindles} built from Moser spindles, {#forbids} forbids it…" |
| S09 P5 | `{#nowhere}` before "and four colors have nowhere to go", not before "everywhere" |
| S04 P3 | "neither {#nblue} blue nor {#nyellow} yellow", for the two rejections |
| S07 P5 | "{#both} Too small…, {#far} too far…", for the two labels |

### 6. Sentences that are hard to follow by ear

| Where | Current | Replace with |
|---|---|---|
| S06 P4 s1 | Gapped verbs ("the first middle pair the other two"), 21 words and 3 marks in one breath | **"Say {#bottom} the bottom is pink. {#pair} The first middle pair takes blue and yellow, so {#top1} its top tip gets the leftover, pink."** Concrete colors that match the picture, same word count. |
| S08 P6 s1 | "Erdős himself suspected it did." ("it did" points back two sentences) | **"Erdős himself {#erdos} suspected it needed five."** |
| S05 P5 s2 | "We never chose which three colors, so this always happens." (muddled) | **"Whichever colors you use, {#any} it always happens."** |
| S07 P1 s1 | "is some number of colors always enough?" | **"Now flip it around: how many colors are {#enough} always enough?"** |
| S02 P6 s2 | "what's the fewest colors that respect…" | **"So how few colors {#board} can respect every ring at once?"** |

### 7. Visual beats with no narration

- **S02 P2 pause.** One dot recolors to "fix" the pair. That is a new idea shown in silence. Drop it and hold the BAD pair.
- **S10 P5 pause.** The counter passes "553", a number the narration never says. Let the counter only tick, and settle it at 874.
- S04 P5 and S08 P6 are fixed above.

### 8. Pauses for questions to the viewer are too short

| Where | Change |
|---|---|
| S02 P1 "Which pairs break the rule?" | 0.9 → 1.2 |
| S05 P2 "What do you notice?" | 1.0 → 1.3 |
| S06 P3 "Pause and try, if you like." | 0.9 → 1.2 |

**Ceiling:** measured inner silence is about the pause plus 0.1 s (pause 1.3 measured as 1.40 s), and QA raises an ERROR at 1.6 s. Keep every non-final pause at 1.4 or less, even though the engine accepts 1.5.

### 9. One pronunciation is wrong: Jaan

"Jaan" becomes ʤˈɑn, and Whisper with no prompt heard **"John Parts"**. Add `"Jaan": "/jˈɑn/"` to `PRON` in `timeline.py`. Moser does not need an entry (mˈOzəɹ is correct).

---

## LOW: storyboard faithfulness and animatability

- **S03 P1, geometry.** "The ring squashes vertically onto the line" does not show two points: a squashed circle covers a whole segment. Instead, draw the ring, fade everything that is off the line, and keep only the two crossing points at −0.7 and 1.3.
- **S07 P2, colors.** The extra tints "light gray and rose" clash with `UNIT_COLOR` and with the pink paint. Use olive and brown instead.
- **Colors, all scenes.** `GOOD` green is the same hex as the palette green (`#6BCB77`). In S09 P3, make the wheel center pink or purple so it is not read as a check mark.
- **S05 P5, glyph.** Avenir Next has no "→" glyph, so Pango falls back to another font. Use an `Arrow` mobject or the text "3 colors: tips match". Palatino does have the superscripts, so "10⁹⁵²" in `N()` is fine.
- **S05 P5 tail.** "Card shrinks to a badge, then everything fades" in 0.9 s is wasted motion. Just fade; the S06 lead-in brings the badge back.
- **S08 P5, web size.** "A few thousand points" needs `geom.unit_web(n_points=3000, lattice_r=5)`. The default call caps at 1,849 points.
- **S10 P3, panel captions.** "custom search" is invented. The fact sheet (§7.3) says "different SAT solvers" plus Phillips's edge-length check. Use "SAT solver 1", "SAT solver 2" and "edge lengths checked".
- **S06 P1, coordinates.** With A = (0, −2.0) and UNIT = 1.8, the top tips are at y ≈ 0.99 and the ring top at about 2.79, not 1.1 and 2.9. They are still in the safe area; this is only a note for the animator.
- **S02 P3, content (optional).** It never says why a tiny disk needs endless colors. If there are words to spare, add "every point would need its own color".
- **For the fact critic.** S11 P4 "mathematicians have shown… exactly seven" rests on a preprint (fact sheet §1.2, Voronov). Consider "a recent proof shows".

---

## Word budget for the edits above

| Edit | Words |
|---|---|
| Cut S01 P5 ("Along the way… best ideas", abstract, generic visual). S01 then ends on "We just don't know which." At 0.83 speed S01 is still about 38 s. | −17 |
| S04 P5 new sentence | +9 |
| S08 P6 new sentence | +9 |
| S06 P5 rewrite | +7 |
| S06 P1 split | +2 |
| S07 P6 "So" | +1 |
| S08 P6 s1 | +1 |
| S06 P4 | 0 |
| S05 P5 | −3 |
| S07 P1 | −1 |
| S02 P6 | −1 |
| **Net** | **+7 → 1,447 words**, inside the cap |

To re-measure after the edits, run `tts/.venv/bin/python tools/timeline.py --speed 0.83` (with `SENT_GAP = 0.55`). Only the changed sentences are synthesized again.

