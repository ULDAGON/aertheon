# Hadwiger–Nelson v2: pedagogy research

Written for the v2 script writer and the animators. Sources are listed at the end. Every factual claim here was checked against the cited source on 2026-09-27.

---

## 0. TL;DR for the script writer

1. **v1 had almost no breathing room.** In the voice-only track, the 34 clips sit back to back with gaps of 0.1 to 0.6 s. There is a single **9.1 s voiceless stretch** in S5 (the "web grows" montage between `grey_2` and `grey_3`, at 2:39 to 2:48 in the final cut). Kokoro `af_heart` at speed 1.0 measured **193 wpm overall** and 220 to 256 wpm on short sentences. Details are in §1.
2. **Pacing math.** At the measured rate, 1,400 words give about 7.2 min of pure speech. With the engine's 0.45 s sentence gaps and 0.6 to 1.4 s paragraph pauses, that comes to about **8.9 min**. That is short of 9:30. Either run TTS at **speed ≈ 0.9** (gives about 9.7 min) or write about 1,500 words. §2 has the numbers.
3. **The single biggest conceptual gap in v1:** it never said *why a 7-point shape says anything about the whole infinite plane*. Say it out loud: "Whatever you do to the whole plane, you also do to these seven points."
4. **Best lay metaphors found:**
   - James Grime's (Numberphile) **"one-unit step always lands on a new color"**
   - **"trap vs. pattern"** (lower bounds are finite traps, upper bounds are whole-plane patterns)
   - **"force and forbid"** (every lower-bound proof forces two points to match, then a stick forbids it)
   - **"the stick can turn"** (why the plane is harder than the line)
5. **Make the spindle airtight with one named lemma**, "the diamond rule": with three colors, the two tips of a diamond must match. Say that the tips are √3 ≈ 1.73 apart, so matching is allowed there. Say that the argument never depended on *which* colors were used.
6. **Hexagons:** say "even its longest diagonal is shorter than one stick" (not "across" or "narrower"). The valid size window is a corner-to-corner width between 0.76 and 1. Borders: **any assignment of border points to a neighbor works**, because of the slack. One honest sentence settles it.
7. **Computer proof:** 4^1581 ≈ 10^952 colorings, so it is *not* brute force. The program reasons by forced colors, just like we do. It was independently re-checked with different software within days, and a bug in the very first version was caught that way. **Since 2020 there is also a proof humans can check by hand** (Parts). That is the best reassurance for lay viewers.
8. **A strong "why it's hard" nugget (verified):** if the rule were even slightly blurry, forbidding every distance in [1−ε, 1+ε], the answer is known: **exactly seven** (Voronov, arXiv 2023, proving Exoo's 2004 conjecture). The whole mystery lives in the razor-thin exact distance.
9. **A second one:** a coloring with fewer than six colors can't be a tidy "map" of regions with nice borders (at least 6 are needed then: Woodall 1973, Townsend 2005). For natural polygon maps, at least 7 are needed (Sokolov–Voronov 2025). So if the answer is 5 or 6, the coloring has to be strange.
10. **Tone:** v1's "nobody on Earth knows" and "a beautiful pattern comes to the rescue" drift toward hype and filler. Prefer calm specifics ("five, six, or seven, and we don't know which").

---

## 1. Critique of v1 (`archive_v1/narration.py`)

### 1a. What the audio actually did (measured)

| measurement | value |
|---|---|
| spoken words | 604 (34 clips, 6 scenes) |
| total speech (sum of clip durations) | 188.1 s |
| final video | 203.1 s |
| speaking rate, overall | **193 wpm** (median clip 195 wpm) |
| fastest clips | `tri_1` 256 wpm, `intro_5` 236, `tri_5` 226, `tri_2` 221 (all short, plain sentences) |
| slowest clips | `grey_6` 157, `out_3` 158 (numbers and long words) |
| gaps ≥ 0.5 s in voice-only track (`out/_joined.mp4`, −45 dB) | 8 gaps of 0.51 to 0.64 s, plus **one 9.07 s gap** ending at 167.98 s (S5, 14.2 to 23.3 s into the scene) |

Method: `ffmpeg silencedetect` on `archive_v1/out/_joined.mp4` (voice only, before the music bed). The per-clip rates come from `audio/durations.json`.

Consequences:
- **"No breaks":** within a scene, the next clip started 0.1 to 0.6 s after the previous one ended. A deduction ("so each tip is forced...") and the next setup ("Now build a second diamond...") ran together with no time to look at the payoff.
- **"Animation without voice":** the S5 dense-graph build ran about 9 s over the music bed alone. Any montage (graph growing, tiling spreading, timeline ticking) needs narration running through it. If it can't have narration, it must fit in a paragraph pause (≤ 1.4 s).
- **Kokoro rushes short sentences.** A 5 to 10 word punchline ("Two colors can never work.") comes out at more than 220 wpm. Give punchlines a `pause_after` of ≥ 0.9 s, or merge them into a slightly longer sentence.

### 1b. Content: what worked (keep or reuse)

- `intro_1`: "sounds like a coloring book exercise, but it has stumped mathematicians..." is a good, warm, honest hook.
- `intro_3`/`intro_4`: the rule, then "closer or farther may match; only exactly one is forbidden". This is the most important misconception-buster and v1 had it. Keep the visual (live distance readout 0.6 ✓, 1.4 ✓, 1.0 ✗).
- `tri_4`: "Every corner is one unit away from both of the others". This is clean.
- `spin_2` to `spin_6`: the correct and airtight lemma (diamond tips must match). Only the pacing and wording need fixing.
- `hex_3`: the two-property logic (too small to hold a stick; same colors far apart).
- `grey_2`/`grey_3`: the human angle (hobbyist) and "a much bigger cousin of the Moser spindle".
- The recurring scoreboard (`BoundsBar`) is a strong device. Keep it and extend it with the ≥3, ≥4, ≤7, ≥5 steps.

### 1c. What was too fast or unclear for a lay viewer

| v1 line | problem | fix |
|---|---|---|
| `intro_2` "color every single point" | Nobody says what that means: no gaps, no blending, exactly one color per point, borders included. | Add a zoom-in beat: "Every point, even the ones on a border, gets exactly one color." |
| `intro_3` "say, one centimeter" | Mixes units. Viewers may think the size matters. | Say once that the size doesn't matter (zoom), then always say "one unit" or "one stick". |
| (missing) | No reason given for "exactly one". | Give scale invariance, and say that forbidding *all* short distances would need endless colors (§5). |
| `tri_2` "circle of radius one ... off limits for blue" | Introduced, then dropped. It never connects to the triangle. | Either use it (circle → second point on the circle → the two circles cross → triangle), or cut it. |
| `tri_3` "Could two colors be enough? Draw a triangle..." | The question and the answer come in the same breath. | Ask, pause (`pause_after` ≈ 1.0), then build. |
| `spin_1` "the brothers ... found a clever little shape that says no" | Implies the Mosers were first to show ≥ 4. Nelson already knew ≥ 4 in 1950 (Soifer). | "The neatest proof uses a shape published by the brothers Leo and William Moser in nineteen sixty-one." |
| `spin_3`/`spin_4` "touch each other" | "Touch" suggests neighbouring regions (map thinking). It is ambiguous. | Use "joined by a stick" or "exactly one unit apart". |
| `spin_4` "The bottom tip and the top tip must match." | Lay viewers may think that is already the contradiction. | Show the tips are √3 ≈ 1.73 apart: "They're not one unit apart, so that's allowed. So far." |
| `spin_5` "rotate it until its top tip is exactly one unit away" | Doesn't show that such an angle must exist, or what the rotation is around. | "Swing it open around the bottom point, like scissors. The gap between the tips grows smoothly from zero, so at some moment it is exactly one." |
| (missing) | "No matter how you color": the argument never used *which* colors. | State it explicitly: "We never chose the colors. Any three colors fail the same way." |
| (missing) | Why 7 points prove something about the infinite plane. | "However you color the whole plane, these seven points get colors too, and that already fails." |
| `hex_2` "a little less than one unit across" / `hex_3` "narrower than one unit" | "Across" and "narrower" are ambiguous (flat-to-flat is shorter than corner-to-corner). | "Even its longest diagonal, corner to corner, is a bit shorter than one stick." |
| `hex_1` "a beautiful pattern comes to the rescue" | Filler, no content. | Motivate the switch: "To show some number is *enough*, you don't need a trap. You need a pattern for the whole plane." |
| `hex_5` | No honest word about border points. | One sentence (see §6.6). |
| `grey_3`/`grey_4` | "Computer magic". No idea of how the trap works or why to trust the check. | "Force and forbid" summary + "not brute force" + independent checks + human-checkable proof since 2020 (§6.8 and §6.9). |
| `out_2` "nobody on Earth knows" | Mild hype. | "and we still don't know which." |
| `out_3` "Sometimes, the simplest questions are the hardest ones." | Generic cliché. It doesn't return to the opening image. | End on the stick sliding across the painted plane, and the trap-or-pattern open question (§7). |
| Whole video | No "why is it hard" section. No on-ramp. No reframing as dots and sticks. | The v2 brief adds these. §6 has material for each. |

---

## 2. Pacing math for v2 (with the measured Kokoro rate)

Assumptions: 193 wpm raw at speed 1.0, 0.45 s between sentences (engine), about 12 words per sentence, and an average `pause_after` of 0.9 s over about 55 paragraphs.

| words | speech @ 1.0 | + sentence gaps | + paragraph pauses | total @ 1.0 | total @ speed 0.9 (≈174 wpm) |
|---|---|---|---|---|---|
| 1,350 | 420 s | +50 s | +50 s | **8.7 min** | 9.4 min |
| 1,400 | 435 s | +52 s | +50 s | **8.9 min** | **9.7 min** |
| 1,450 | 451 s | +54 s | +50 s | **9.3 min** | 10.0 min |

**Recommendation to the orchestrator:** the brief assumes about 160 wpm, but the measured rate is about 193 wpm. To land at 9:30 to 10:30 with 1,350 to 1,450 words, render with `--speed 0.9` (or about 0.92). Alternatively, raise the word count to about 1,550 at speed 1.0. The slower speed also fixes the rushed short sentences.

Rule of thumb for the writer: **one paragraph ≈ one visual beat of 6 to 14 s**. A scene of 150 words at speed 0.9 with pauses is about 60 s.

---

## 3. How the best explainers teach it

| source | audience | what they do well | what to borrow |
|---|---|---|---|
| **Numberphile, "A Colorful Unsolved Problem"** (James Grime, 27 Feb 2019, 9:39, about 700k views) | general YouTube | Opens with the **four color theorem** as a familiar anchor. Then the **walk metaphor**: "I'm going to take a step... one unit... every time I take a step, I want to step onto a different color... no matter what walk I choose." Shows the **7-hexagon answer first** ("seven colors work, and we can prove that really quickly"), then eliminates 2, 3, 4. Gives the hexagon size window: "less than one and greater than 0.76". Human angle on de Grey: "does maths for fun". The extra footage has Grime betting on 7. | The step metaphor. Upper-bound-first ordering (optional). The size window. |
| **Quanta, "Four Is Not Enough"** (Patrick Honner, 18 Jun 2018) | curious adults | Warm-up puzzle (dominoes on a chessboard) to show that **coloring is a proof tool**. **Nine squares** of side 2/3 (diagonal √(8/9) < 1, same colors 4/3 apart) before the hexagons. The circle argument for ≥ 3 ("all points 1 unit from P form a circle"). The spindle as two rhombuses hinged at a point, "pulled apart until" the tips are one apart. Ends with "Color me optimistic." | The **squares-then-hexagons** on-ramp (shows the *strategy* with easy geometry). "Hinged ... pulled apart". |
| **Quanta, "Decades-Old Graph Problem Yields to Amateur Mathematician"** (Evelyn Lamb, 17 Apr 2018) | curious adults | Graph framing ("points connected by lines ... all exactly the same length"). The four color theorem analogy. de Grey "fused copies of the Moser spindle and another small assembly of points into a 20,425-vertex monstrosity". Royle: "the final solution might be some incredibly deep mathematics ... Or it could just be somebody's ingenuity finding a graph." de Grey: "I got extraordinarily lucky." | The Royle quote idea (answer could come from deep theory or from one clever construction) for the "why it's hard" or ending. |
| **Scientific American, "A Few of My Favorite Spaces: The Moser Spindle"** (Evelyn Lamb, 19 Apr 2018) | general | Invites the reader to *try*: "Can you convince yourself that you need four colors...?" | A 1 s "try it yourself" pause before the spindle reveal (use `pause_after`). |
| **HLF blog, "Colouring in like a mathematician"** (Katie Steckles, 3 May 2018) | general | Hook: "A recent mathematical breakthrough has been made, in the area of… colouring in." Spindle as "two pairs of equilateral triangles stuck back-to-back". de Grey's graph as "layering multiple copies of triangulated hexagons". | The playful "breakthrough in colouring in" hook. |
| **ThatsMaths** (Peter Lynch, 2022) | general | Triangle first, then the spindle as a procedure: "rotate the rhombi about the top point until the lowest points are a unit distance apart." Closes on the axioms subtlety. | The procedural spindle build. |
| **de Grey's paper** (arXiv 1804.02385) | research | Unusually readable overview (§1). The wheel H (hexagon + centre), "monochromatic triple", graph L forces one, graph M forbids one, 52 copies glued, 20,425 vertices. Custom backtracking in Mathematica on a MacBook Air, running "only a few minutes", because "fixing ... only 20 or so colours ... lets almost all remaining colours be forced". | The **force-and-forbid** summary. The **forced-color cascade** as the visual for "what the computer does". |
| **Soifer, "Breakthrough in My Favorite Open Problem"** (Geombinatorics 2018 essay) | enthusiasts | History with personality. Nelson posed it "at a tender age of 18 in November 1950". Nelson found ≥ 4, and Isbell (20) found ≤ 7. Erdős thought ≥ 5. A 2009 workshop vote gave a "democratic value" of 4.5. Erdős on computer proofs: "Beggars cannot be choosers." Klee and Wagon predicted a solution "by the year 2084". | Human bookends (18-year-old student in 1950, hobbyist in 2018). Erdős's line on computer proofs. |

Other video explainers exist, but they are small or niche: XorUnison's tiling videos, including a SoME4 entry; a 2026 "Dimensional Algebra" video; Michael Penn's "Coloring the plane". I found no 3Blue1Brown video on this problem. So v2 has little direct competition in the 3b1b style.

General 3Blue1Brown/SoME exposition principles that apply here: **concrete before abstract** (a triangle before "unit-distance graph"), **let the viewer try first** (a question, then a pause, then the reveal), and give the feeling the viewer **"could have invented it"** (the diamond rule is exactly that).

---

## 4. The most effective intuitions and "aha" framings (ranked)

1. **"One step, new color."** (Grime) Rephrase "points at distance one" as a walker whose stride is exactly one unit. "Paint an endless floor so that one exact-length step, in any direction, always lands on a new color." It makes the rule physical. It also explains why regions smaller than a stride are fine (you can't land inside the region you're standing in).
2. **"The stick."** A single yellow unit stick is the recurring character. It slides and spins over any coloring and must always show two different colors at its ends. Spinning it around one end draws the **ring of forbidden partners** (the unit circle). Every proof is "find where the stick lands on two equal colors".
3. **"Whatever you do to the plane, you also do to these points."** This is why a finite shape (triangle, spindle, de Grey's graph) proves a lower bound for the infinite plane. It is the missing idea in v1.
4. **"Trap vs. pattern."** To prove you need *at least* k colors, build one finite trap of dots and sticks that k−1 colors can't escape. To prove k colors are *enough*, paint a pattern for the entire plane. These are completely different kinds of objects, which is why the gap between them is hard to close. (Optional deepening: de Bruijn and Erdős (1951) showed that, with the standard axioms, *any* true lower bound has a finite trap.)
5. **"Force and forbid."** Every lower-bound proof has the same shape. Some structure *forces* two points to share a color, and a stick *forbids* it.
   - Spindle: the diamond forces the tips to match, and the extra stick forbids it.
   - de Grey: one gadget forces a same-colored triple in some wheel, and another gadget forbids it in every wheel.
   This lets the video explain de Grey's idea without detail, as "the spindle's trick, scaled up".
6. **"The stick can turn."** On a line, alternating unit stripes work (exactly 2 colors). Extend the stripes into the plane and the stick simply stands up inside one stripe. The freedom to rotate is what makes the plane hard.
7. **"Too small to hold a stick; too far to reach a twin."** The whole 7-color proof in one line.
8. **"The mystery lives in the exact distance."** Blur the rule a hair and the answer is known: exactly 7. Forbid *all* short distances and you need endless colors. Exactly one is the one knife-edge setting where nobody knows.

---

## 5. Usual points of confusion, and how to defuse each

Example lines follow the script rules (spoken, numbers spelled out, no symbols).

| confusion | defuse with | example line |
|---|---|---|
| **"What does it mean to color every point?"** | Zoom in on a border. Every point has exactly one color: no gaps, no mixing, no "outline" points left blank. The coloring may be as strange as you like; it does not have to look like regions. | "Every point gets exactly one color, even the points right on a border." |
| **"Why only *exactly* one?"** (a) the size of the unit | Zoom. Any coloring for one centimeter becomes a coloring for one kilometer by scaling, so every distance gives the same puzzle. | "Zoom in or out and the puzzle doesn't change, so we just call the distance one unit." |
| (b) why not forbid all short distances? | Then all points in a small disk would have to differ pairwise: endless colors. That is boring. | "If every short distance were forbidden, every point in a tiny disk would need its own color." |
| (c) closer and farther are fine | v1's live readout demo. Necessary later for the hexagons (a whole region can be one color). | "Closer is fine. Farther is fine. Only exactly one unit is forbidden." |
| **"Why can't two colors work?"** | The triangle, or stripes failing because the stick turns. | "Any triangle with three sticks needs three different colors." |
| **"Is this the four color theorem?"** | No. Maps: neighbours that share a border must differ, and the regions are given. Here nothing is given, you choose everything, and the forbidden pairs are points exactly one unit apart. The four color theorem was settled in 1976; this one is open. | "It sounds like the famous map problem, but here there are no countries. We get to paint however we like." |
| **"The diamond tips match. Isn't that already a problem?"** | No: they are √3 ≈ 1.73 apart, not 1. Show the measurement. | "The two tips are farther apart than one unit, so matching is allowed. For now." |
| **"Did it depend on which colors I picked?"** | Never name the colors in the deduction. Say "the middle two take two colors; each tip gets the only color left". | "We never picked the colors. Any three colors run into the same wall." |
| **"Why can you rotate until exactly one?"** | The tip gap grows smoothly from zero as the diamond swings, so it passes through one. The angle is about 33.6°. | "As it swings open, the gap between the tips grows smoothly from zero, so at one moment it is exactly one." |
| **"How can seven points say anything about the whole plane?"** | Any plane coloring colors these points. | "However cleverly you paint the whole plane, these seven points get colors too." |
| **"Borders of hexagons?"** | Border points can join either neighbour. Every choice works because there is slack: a closed hexagon is less than one wide, and same-colored hexagons are more than one apart (verified numerically: side 0.45 gives width 0.90 and gap 1.19). Note: on the *line*, the stripe ends *do* matter, because the stripes are exactly one long. | "Points on a border can simply join either neighbor. There's enough room to spare that any choice works." |
| **"So is the answer seven, since hexagons are the best tiling?"** | No. A cleverer coloring need not be tiles at all. But it would have to be strange: tidy maps need at least 6 colors, and natural polygon maps need at least 7. | "Any coloring with fewer than seven colors, if one exists, can't be a tidy map. It would have to be strange." |
| **"Why does a computer proof count?"** | (1) The question is finite: 1,581 points, 4 colors. (2) It is not brute force: 4^1581 ≈ 10^952, far more than the ~10^80 atoms in the observable universe. The program reasons like we did, and forced colors cascade. (3) Other people re-checked it with completely different software (SAT solvers) within days, and a bug in the first version was caught exactly that way. (4) SAT solvers can print a proof that small independent checkers verify. (5) The four color theorem (1976) was also computer-assisted. (6) **Since 2020 there is a proof that people can check by hand** (Jaan Parts). | "The computer didn't try every coloring. There are far too many. It reasoned the way we did, one forced color at a time." |
| **"Why can't they just try harder?"** | Trap vs. pattern. Traps grow fast (7 dots for four colors, about 500 for five), and no trap for six is known. A 5- or 6-color pattern would have to be strange. | See §6.11. |

---

## 6. Step-by-step teaching notes and visual ideas

Shared visual language (from the brief): points are dots, a unit pair is a yellow "stick", a 7-color palette, and the scoreboard "1 2 3 4 5 6 7 8 …" with a narrowing window. Add the **free-roaming stick** as the recurring character.

### 6.1 Hook (opening image)
- Visual: an endless dark sheet. Paint splotches appear, then dense colored points. A single yellow stick drifts across and spins, and its ends flash two colors each time it lands.
- Options, ranked:
  1. The walk/floor metaphor plus the tease "five, six, or seven, and nobody knows which."
  2. The coloring-book framing (v1 `intro_1`, which is good).
  3. The four color theorem bridge: "Maps need four colors. That was settled in nineteen seventy-six. This is its wilder cousin, and it is still open."
  4. Human bookends: an eighteen-year-old student in nineteen fifty, and a hobbyist in twenty eighteen.
- Keep the hook ≤ 35 s. Pose the question in one plain sentence before any history.

### 6.2 The rule
- Visual: two dots, a stick, live distance readout. Closer 0.6 ✓, farther 1.4 ✓, exactly 1.0 ✗ (v1 demo, keep). Zoom into a border to show "every point, exactly one color". Zoom out and in with the stick label unchanged (scale doesn't matter).
- Introduce the scoreboard here: "What's the fewest colors that can do it?" The whole row 1 to 8… is lit, with a "?".
- Say the name once: "This is the Hadwiger Nelson problem." "Chromatic number of the plane" is optional; if used, say it once.

### 6.3 One-dimensional warm-up (strong optional on-ramp, about 100 to 120 words)
- A line, with a stick sliding along it. One color fails at once. Two colors: alternate stripes one unit long.
  - Show that each stripe *includes its left end and not its right end* (filled vs. hollow dot), so a point and the point one unit to its right always sit in neighbouring stripes.
  - Verified: color x by the parity of ⌊x⌋; x and x+1 always differ in parity.
- Payoff: "On a line, the answer is exactly two, and we just proved it."
- Then extrude the stripes into the plane. The stick rotates upright inside one stripe, both ends turn the same color, and it flashes red. "In the plane, the stick can turn. That's what makes everything hard."
- Callback possibility for the ending: "On a line the answer is two. Add one dimension, and after seventy-five years we still don't know."

### 6.4 Triangle (≥ 3)
- Optional circle build (Honner): color a dot blue, spin the stick to draw its ring ("no blue anywhere on this ring"), pick a point on the ring, draw its ring. The rings cross at two points, which gives the triangle. This connects the circle idea to the triangle instead of dropping it.
- Ask "Could two colors be enough?", pause about 1 s, then color the corners: two colors, then the third corner has nowhere to go.
- Say the general principle once: "whatever you do to the plane, you also do to these three points." It sets up the spindle.
- Scoreboard: 1 and 2 dim out, window "≥ 3".
- Introduce the vocabulary "a shape made only of sticks": dots joined by sticks that are all exactly one unit long. This is the "dots and sticks" reframing, and the triangle is the smallest example.

### 6.5 Moser spindle (≥ 4). The heart of the video.
Teach it in four beats, each with its own paragraph and pause.
1. **Diamond rule.** Two triangles glued along a stick make a diamond (a rhombus of two equilateral triangles). The two middle dots are joined, so they take two different colors. Each tip is joined to both middle dots, so it gets the *only color left*. Therefore **both tips get the same color**. Show the tips are √3 ≈ 1.73 apart: allowed. Give the rule a name, on screen "diamond rule: tips match".
2. **Second diamond, hinged.** Copy the diamond, sharing the bottom tip. Swing it open around that tip, with a live readout of the gap between the two top tips growing 0.00 → 1.00, and snap at exactly one (angle ≈ 33.56°, verified). Draw the new stick.
3. **Contradiction.** The diamond rule, twice: both top tips match the bottom tip, so they match each other. But they are one stick apart. Red flash.
4. **Generality.** "We never chose the colors." "However you paint the plane, these seven dots get painted too." 7 dots, 11 sticks (count them). Scoreboard "≥ 4".
- History, stated correctly: the shape was published by Leo and William Moser in 1961. Nelson already knew four were needed in 1950, so don't imply the Mosers were first. Optional: Golomb found a 10-dot shape at about the same time.
- Also name "force and forbid" here: the diamond *forces* the tips to match, and the extra stick *forbids* it. The de Grey scene will reuse this.
- Viewers pause frames here. Geometry must be exact: the rotation is about the shared tip, the rotated tip lands exactly one unit away, and the other nine sticks keep length 1.

### 6.6 Upper bound (≤ 7): patterns, not traps
- Motivate the switch: "To prove a number is enough, a trap is useless. We need one pattern that works everywhere."
- Optional on-ramp (Honner): **nine squares** of side two-thirds, in a 3×3 block of colors, repeated. Diagonal 0.94 < 1 (a square can't hold a stick), and same-colored squares are 4/3 ≈ 1.33 apart. "Nine colors is enough. Can we do better?" Costs about 40 words and makes the hexagon step feel earned.
- Hexagons: they are the roundest shape that tiles with no gaps, so you can pack them tighter.
  - One hexagon with a stick spinning inside it: the stick never fits, because even the longest diagonal is < 1.
  - The flower (one hexagon in the middle, six around it) gets colors 0 to 6. The pattern spreads.
  - Highlight one color and show the gap (≈ 1.19 with side 0.45) next to a stick.
- **Valid size window:** side s with 1/√7 < s < 1/2. That is, a corner-to-corner width between 0.756 and 1 (Grime: "less than one and greater than 0.76"). The same-color gap is exactly √7·s (verified numerically).
- **Honest border note** (one or two sentences): border points join either neighbour, and every choice works because of the slack. Proof sketch, not for narration: any two points of one closed hexagon are < 1 apart, and any two points of different same-colored closed hexagons are ≥ √7·s > 1 apart.
- Credit: John Isbell, 1950 (Soifer), a fellow student of Nelson. Hadwiger had discussed the 7-colored hexagon tiling in another context in 1945 (de Grey's paper, §1).
- Scoreboard: window "4 to 7".

### 6.7 The long stall (1950 to 2018)
- Timeline 1950 → 2018 with the scoreboard frozen at 4…7. It must be narrated throughout (in v1, this is where silence crept in).
- Content options:
  - The "trap vs. pattern" statement.
  - Experts disagreed: Erdős suspected at least five. In a 2009 workshop vote, the room split mostly between four and five. Soifer joked the "democratic value" was 4.5. Four has since been ruled out.
  - Optional de Bruijn–Erdős (1951): with the standard axioms, if the plane needs more colors, some *finite* dots-and-sticks trap already proves it. "You never need infinity to prove a lower bound. You just need the right finite trap."
- Avoid claiming "nobody tried". Many partial results exist; the *bounds* just didn't move. Wording: "The bounds didn't move for sixty-eight years."

### 6.8 de Grey's breakthrough (≥ 5)
- Who: Aubrey de Grey, English, best known for research on the biology of aging, with an earlier degree in computer science. He did this as a hobby. Keep it neutral and brief. Don't name his organization (he left SENS in 2021 amid controversy). No photo or likeness. Pronounced "de GRAY".
- When: posted to arXiv on 8 April 2018.
- Lay-accurate idea (from the paper's own overview):
  - Building block: the **wheel**, a hexagon of sticks with its centre (7 dots, 12 sticks). With four colors, a wheel either has **three alternate corners of the same color** (a big triangle of side √3) or it doesn't.
  - Gadget A (121 dots) **forces** at least one of its 52 wheels to have such a same-colored triple.
  - Gadget B (1,345 dots, packed with Moser spindles) **forbids** its central wheel from having one.
  - Glue a copy of B onto every wheel of A, and four colors have nowhere to go: over 20,000 dots (20,425), later trimmed to 1,581.
  - "It's the spindle's trick, force and forbid, scaled up."
- Visual: the wheel with its alternating triple highlighted. Two labeled blobs "forces a triple" and "forbids a triple" snap together, then red. Then an illustrative dense graph with a counter going over 20,000 and down to 1,581. Label it "illustration", not de Grey's actual graph, unless the real coordinates are used; they are listed in the paper, §5.1.
- Scoreboard: 4 is struck, window "5 to 7". This is a big reveal, so `pause_after` 1.2 to 1.4.

### 6.9 The computer check, and why to trust it
- **Not brute force.** 4^1581 ≈ 10^952 colorings (computed). "More ways to color it than there are atoms in the universe, by a mind-boggling margin". (Tone: prefer "far more than".)
- **What it did.** de Grey's own program colored a few dots and followed the forced colors. "Fixing only 20 or so colours ... lets almost all remaining colours be forced". When it hit a dead end, it backtracked. Visual: a domino cascade of forced colors, a red dead end, then a rewind. This mirrors the spindle reasoning, which is nice continuity.
- **Checks.** Within days, others (Dustin Mixon, Boris Alexeev, and others) confirmed it with completely different software (SAT solvers). The first posted version (1,567 dots) turned out to be four-colorable because of a bug, which McKay and Royle's independent checks exposed. The corrected graph (1,581) held up. The honest version is "checking by independent programs is exactly how errors get caught." This is optional and 1 to 2 sentences at most.
- **Precedent and reassurance.** The four color theorem (1976) also needed a computer. Erdős: "Beggars cannot be choosers." **In 2020 Jaan Parts published a proof that can be checked by hand**, so the result no longer rests on trusting a machine.

### 6.10 Shrinking the trap (Polymath16)
- An open online collaboration, Polymath16, was proposed on Terence Tao's Polymath blog in April 2018. Threads were hosted by Dustin Mixon. Anyone could join. Goals: smaller traps, and proofs a human can check.
- Counter visual: 1,581 → 874 (Heule, 14 Apr 2018) → 826 (16 Apr) → 803 → 633 → 610 → … → 529 (Heule, SAT-based, 2019) → **509** (Jaan Parts, 2020: 509 dots, 2,442 sticks). As of August 2026, **509 is still the smallest known** (Haugland 2026 cites it as the record).
- Keep it light: one paragraph plus the ticking counter, narrated throughout.

### 6.11 Status today and why it's hard
- **5, 6, or 7.** The scoreboard glows on those three.
- Why it is hard. Pick 2 or 3 of these:
  1. **Trap vs. pattern.** To prove six, find a finite trap that five colors can't escape. None is known, and such traps may be enormous (Grime's guess). To prove five or six is enough, paint a pattern, but such a pattern would have to be strange:
  2. **Tidy maps can't do it.** If the colors form regions with nice borders, at least six colors are needed (Woodall 1973, Townsend 2005). For natural polygon maps, at least seven (Sokolov and Voronov, 2025). A 5-coloring, if one exists, looks like nothing we can draw.
  3. **Exactness.** "Blur the rule even slightly, forbidding every distance within a hair of one, and the answer is known: exactly seven." (Voronov 2023, proving Exoo's 2004 conjecture.) "The whole mystery lives in the exact distance."
  4. **Search explodes.** 4^509 ≈ 10^306 colorings, even for the smallest trap.
  5. Deep, optional, and **not recommended** for this audience: the answer might even depend on the axioms of set theory (Shelah and Soifer 2003; Wikipedia: "may depend"). If mentioned, use one gentle sentence at most, and say "might".
- Royle's line (Quanta): the solution "might be some incredibly deep mathematics ... Or it could just be somebody's ingenuity finding a graph."

### 6.12 Three dimensions (optional extra)
- In space: **at least 6 and at most 15.**
  - Lower bound: Nechushtan, 2002.
  - Upper bound: Coulson, 2002, and Radoičić and Tóth, 2003, independently.
- Visual: a translucent cube lattice with a stick spinning in 3D; the scoreboard reads "6 … 15". One or two sentences.

### 6.13 Ending
- Return to the opening image: the endless sheet, the stick drifting and spinning.
- Candidate closing ideas:
  - "Somewhere out there is either a trap that five colors can't escape, or a pattern nobody has painted yet. We don't know which."
  - Line callback: "On a line, the answer is two. Add one dimension, and the answer is five, six, or seven."
  - Bookend: "It began with an eighteen-year-old's question in nineteen fifty. The last big step came from someone doing math for fun. The next step could come from anyone."
- Hold on the final frame, still narrated or within ≤ 1.5 s of silence (hard constraint).

---

## 7. Hooks and endings: recommendation

- **Hook:** the stick on the endless painted sheet, plus Grime's step framing, plus the explicit tease "five, six, or seven". Then the plain question. Put history later.
- **Ending:** return to the same sheet and stick, and the trap-or-pattern open question. Optionally add the line callback (only if the 1D warm-up is used, so the callback pays off).
- Avoid: "stumped the greatest minds", "nobody on Earth", "mind-blowing", "genius", cliché closers.

---

## 8. Vocabulary and tone guide

| avoid (jargon) | say instead |
|---|---|
| graph, unit-distance graph | a shape made of sticks / dots and sticks |
| vertex, vertices | dot(s), point(s) |
| edge | stick |
| adjacent, "touch" | joined by a stick / exactly one unit apart |
| monochromatic | the same color |
| lower bound / upper bound | "at least" / "enough" or "at most" |
| chromatic number | "the fewest colors" (the name at most once) |
| rhombus | diamond |
| diameter (of hexagon) | longest diagonal, corner to corner |
| SAT solver | "a different kind of program" |
| proof by contradiction | "that breaks the rule" |

- Refer to colors by role ("the middle two colors", "the only color left"), not by name, during deductions.
- Keep one idea per paragraph. Ask the question, pause, then answer.
- Short punchlines need a `pause_after` (Kokoro speeds through them).

---

## 9. Fact sheet with sources

| claim | source |
|---|---|
| Edward Nelson posed the problem in November 1950, aged 18; he found the lower bound 4; his friend John Isbell (20) found the upper bound 7 | Soifer essay: https://www.cs.umd.edu/~gasarch/BLOGPAPERS/soifer.pdf |
| First published by Martin Gardner in 1960; Hadwiger 1945 published a related result | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem |
| Hadwiger discussed the 7-coloring of the hexagonal tiling in 1945 (another context); bounds 4 to 7 known since 1950 | de Grey 2018, §1: https://arxiv.org/pdf/1804.02385 |
| Moser spindle: Leo and William Moser, 1961, 7 vertices, 11 edges, tips of each rhombus must match in a 3-coloring | https://en.wikipedia.org/wiki/Moser_spindle |
| Golomb graph: 10 vertices, 4-chromatic, around the same time | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem |
| Hexagons with diameter slightly less than one, seven colors | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; Numberphile (Grime: 0.76 to 1) https://www.youtube.com/watch?v=niaeV_NHh-o |
| Nine squares of side 2/3 give a 9-coloring | Honner, Quanta: https://www.quantamagazine.org/the-numbers-and-geometry-behind-a-math-coloring-puzzle-20180618/ |
| de Grey arXiv v1 8 Apr 2018 claimed 1,567 vertices; v2 11 Apr 2018 has 1,581 | https://arxiv.org/abs/1804.02385v1 , https://arxiv.org/abs/1804.02385 |
| First graph N had 20,425 vertices; wheel H (7 vertices, 12 edges); L (121 vertices, 52 wheels) forces a monochromatic triple; M (1,345 vertices) forbids it; Mathematica on a MacBook Air, a few minutes | https://arxiv.org/pdf/1804.02385 |
| 1,567 graph was 4-colorable (bug), found by McKay and Royle; Mixon and Alexeev confirmed the corrected graph with a SAT solver | Kalai: https://gilkalai.wordpress.com/2018/04/10/aubrey-de-grey-the-chromatic-number-of-the-plane-is-at-least-5/ |
| Independent verification with different SAT solvers | Aaronson, 11 Apr 2018: https://scottaaronson.blog/?p=3697 |
| "Fused copies of the Moser spindle ... 20,425-vertex monstrosity"; Heule 874 then 826; Royle quote | Quanta, 17 Apr 2018: https://www.quantamagazine.org/decades-old-graph-problem-yields-to-amateur-mathematician-20180417/ |
| Polymath16 proposal and goals | https://polymathprojects.org/2018/04/10/polymath-proposal-finding-simpler-unit-distance-graphs-of-chromatic-number-5/ |
| Heule record sequence 874 (14 Apr), 826 (16 Apr), 803, 633, 610, 533 (18 May 2018) | Soifer essay (above) |
| Heule 529 vertices, 2,670 edges (SAT proof minimization) | https://arxiv.org/abs/1907.00929 |
| Parts: 509 vertices, 2,442 edges (Oct 2020) | https://arxiv.org/abs/2010.12665 |
| Parts: human-verifiable proof that χ ≥ 5 (Oct 2020) | https://arxiv.org/abs/2010.12661 |
| 509 is still the smallest known in Aug 2026; bounds 5 to 7 | Haugland 2026: https://arxiv.org/abs/2608.04542 |
| de Bruijn–Erdős (1951): finite subgraphs determine the chromatic number (needs the axiom of choice) | https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Erd%C5%91s_theorem_(graph_theory) |
| Answer "may depend on the choice of axioms" (Shelah and Soifer 2003) | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem |
| Map-type colorings (regions bounded by Jordan curves) need ≥ 6 (Woodall 1973; Townsend 2005) | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; https://arxiv.org/abs/2502.01958 |
| Polygon maps (three boundaries at each vertex, boundaries not unit-circle arcs) need ≥ 7 (Sokolov and Voronov, 2025) | https://arxiv.org/abs/2502.01958 |
| Forbidding the interval [1−ε, 1+ε] gives exactly 7 for small ε (Voronov 2023, Exoo's 2004 conjecture) | https://arxiv.org/abs/2304.10163 |
| 3D: 6 ≤ χ ≤ 15 (Nechushtan 2002; Coulson 2002; Radoičić and Tóth 2003) | https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem ; https://www.cs.bme.hu/~geza/chromatic.pdf |
| Erdős guessed ≥ 5; 2009 DIMACS vote "4.5"; Erdős "Beggars cannot be choosers"; Klee and Wagon "by the year 2084" | Soifer essay (above) |
| Four color theorem proved in 1976 with computer assistance | https://en.wikipedia.org/wiki/Four_color_theorem |
| de Grey: English biomedical gerontologist, earlier computer science degree (Cambridge 1985) | https://en.wikipedia.org/wiki/Aubrey_de_Grey |
| Computed in this session: spindle hinge angle 2·asin(1/(2√3)) = 33.557°; hexagon same-color gap = √7·s (s = 0.45 → 1.19); valid s ∈ (0.378, 0.5); 4^1581 ≈ 10^951.9; 4^509 ≈ 10^306.4 | numeric check |

**Pronunciation notes for the writer and TTS:**
- Hadwiger: the engine handles it
- de Grey: "de GRAY"
- Moser: "MOH-zer"
- Isbell: "IZ-bel"
- Erdős: "AIR-dish" (Kokoro may need a phoneme override)
- de Bruijn: "de BROWN"
- Heule: "HUR-luh"
- Jaan Parts: "YAHN"
- Polymath: plain English

---

## 10. Factual traps (things v2 must not say)

- ✗ "The Moser brothers first proved four colors are needed." Nelson knew it in 1950; the Mosers published the neat seven-point shape in 1961.
- ✗ "For seventy years nothing happened." Say "the bounds didn't move for sixty-eight years", or "almost seventy years".
- ✗ "de Grey's computer tried every coloring." It is not brute force (10^952).
- ✗ "de Grey used a SAT solver." His own program did the search (Mathematica). *Others* confirmed it with SAT solvers.
- ✗ "The graph has exactly twenty thousand points." It had 20,425; "over twenty thousand" is safe.
- ✗ "Hexagons one unit across." The longest diagonal must be *less* than one (and more than about 0.76).
- ✗ "The answer depends on the axioms." That is only possible ("may"), not proven for the plane.
- ✗ Any claim that a six-color trap or a six-color pattern is known. Neither is known as of Aug 2026.
- ✗ "Nobody on Earth knows" (hype). Prefer "we still don't know".
- Years: 1950 → 2026 is "more than seventy-five years".

---

## 11. Sources consulted

- Numberphile, "A Colorful Unsolved Problem" (James Grime, 2019) and the extra footage: https://www.youtube.com/watch?v=niaeV_NHh-o , https://www.youtube.com/watch?v=7nBtRKvUox4 (auto-captions read via yt-dlp)
- Quanta, Evelyn Lamb (2018): https://www.quantamagazine.org/decades-old-graph-problem-yields-to-amateur-mathematician-20180417/
- Quanta, Patrick Honner, "Four Is Not Enough" (2018): https://www.quantamagazine.org/the-numbers-and-geometry-behind-a-math-coloring-puzzle-20180618/
- Scientific American, Evelyn Lamb (2018): https://www.scientificamerican.com/blog/roots-of-unity/a-few-of-my-favorite-spaces-the-moser-spindle/
- HLF SciLogs, Katie Steckles (2018): https://scilogs.spektrum.de/hlf/colouring-like-mathematician/
- ThatsMaths, Peter Lynch (2022): https://thatsmaths.com/2022/03/24/the-chromatic-number-of-the-plane/
- The Aperiodical (2018): https://aperiodical.com/2018/04/the-chromatic-number-of-the-plane-is-at-least-5/
- de Grey, arXiv 1804.02385: https://arxiv.org/abs/1804.02385
- Soifer, Geombinatorics essay (2018): https://www.cs.umd.edu/~gasarch/BLOGPAPERS/soifer.pdf
- Gil Kalai (2018): https://gilkalai.wordpress.com/2018/04/10/aubrey-de-grey-the-chromatic-number-of-the-plane-is-at-least-5/
- Scott Aaronson (2018): https://scottaaronson.blog/?p=3697
- Polymath proposal (2018): https://polymathprojects.org/2018/04/10/polymath-proposal-finding-simpler-unit-distance-graphs-of-chromatic-number-5/
- Heule, arXiv 1907.00929; Parts, arXiv 2010.12665 and 2010.12661; Haugland, arXiv 2608.04542; Voronov, arXiv 2304.10163; Sokolov and Voronov, arXiv 2502.01958
- Wikipedia: Hadwiger–Nelson problem; Moser spindle; de Bruijn–Erdős theorem; Aubrey de Grey; Four color theorem
- 3Blue1Brown, SoME blog (exposition principles): https://www.3blue1brown.com/blog/some1/

