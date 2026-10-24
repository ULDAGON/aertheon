# Adversarial fact-check: script_synth.json

Checked 2026-09-27. I checked every narrated claim against a primary or high-trust source. I read the source texts directly: de Grey arXiv:1804.02385 v3 in full, Soifer's Geombinatorics essay in full, de Grey & Parts arXiv:2303.14714 in full, and the openings of Parts arXiv:2010.12665, Parts arXiv:2010.12661 and Heule arXiv:1805.12181. I also used Quanta, Aaronson's blog, MathWorld (updated 2 Sep 2026), Wikipedia, and the Sokolov–Voronov and Voronov arXiv pages. I re-ran the geometry scripts (`checks/spindle_check.py`, `checks/hexagon_check.py`) and did the arithmetic again by hand.

**Verdict:** No narrated fact is wrong: every name, date and number checks out. The spindle argument is airtight. The hexagon construction and the "finite traps are enough" statement are correct. One sentence has a real logic error (S11, "To prove six"). A few sentences are loose or ambiguous enough that an informed viewer could object. All fixes below keep the bookmarks. Together they add at most 8 words (1,440 → 1,448, under the 1,450 cap).

---

## Issues, most severe first

### 1. MEDIUM: S11_Today [1.1]: logic error
- **Sentence:** "To prove six, you'd need {#six} a trap that five colors can't escape."
- **Problem:** A trap that five colors cannot escape proves only *at least six*. It does not prove the answer *is* six. To prove six you would also need a six-color pattern for the whole plane. This contradicts the video's own logic from S08 (traps raise the lower bound, patterns lower the upper one).
- **Fix (+1 word):** "To rule out five, you'd need {#six} a trap that five colors can't escape."
  (Alternative, +3 words: "To push it up to six, you'd need {#six} a trap that five colors can't escape.")

### 2. MEDIUM-LOW: S07_Hexagons [2.0]: misleading reason
- **Sentence:** "{#hex} Hexagons are rounder, so they pack tighter."
- **Problem:** Squares and hexagons both tile the plane with no gaps, so neither "packs tighter". The real point, which the visual already shows by overlaying a square of the same corner-to-corner width, is that a hexagon covers more area for the same width: about 0.65·d² versus 0.5·d². So fewer tiles crowd into the one-unit zone around each tile, and fewer colors are needed.
- **Fix (+4 words):** "{#hex} Hexagons are rounder, so they cover more area for their width."

### 3. MEDIUM-LOW: S07_Hexagons [3.1]: "every other" is ambiguous when spoken
- **Sentence:** "It lands only on {#other} other colors, because every other blue hexagon is {#gap} a bit more than one unit away."
- **Problem:** Heard aloud, "every other blue hexagon" can mean "every second blue hexagon". That meaning is false, because *all* other blue hexagons are more than one unit away. (The geometry is right: the same-color gap is √7·s, which is 1.19 at s = 0.45. It is always above 1 when 1/√7 < s < 1/2. Re-checked.)
- **Fix (±0 words):** "It lands only on {#other} other colors, because all other blue hexagons are {#gap} a bit more than one unit away."

### 4. LOW-MEDIUM: S08_Stall [1.0]: why the problem carries Hadwiger's name
- **Sentence:** "The Swiss mathematician Hugo Hadwiger {#hadwiger} helped spread it, so it's called {#name} the Hadwiger Nelson problem."
- **Problem:** The sentence says the name comes *only* from spreading the problem. De Grey (§1) gives the reason differently: the problem is named after Hadwiger "because the 7-colouring of the hexagonal tiling was first discussed (though in another context) by Hadwiger in 1945". Wikipedia's Hadwiger page credits his 1945 related result *and* his 1961 popularization. Soifer notes that in 1961 Hadwiger said he was not the problem's author. "Swiss" is correct: he was born in Karlsruhe and grew up in Bern.
- **Fix (+2 words):** "The Swiss mathematician Hugo Hadwiger {#hadwiger} worked on related questions and helped spread it, so it's {#name} the Hadwiger Nelson problem."

### 5. LOW: S11_Today [3.1]: the "thin band" result rests on a preprint
- **Sentence:** "Thicken every ring into {#band} a thin band, forbidding distances near one too, and mathematicians have shown {#seven} the answer is exactly seven."
- **Problem:** The mathematics is right. Voronov proves Exoo's 2004 conjecture that at least 7 colors are needed for every ε > 0, and the hexagons give exactly 7 when ε is small. But the proof is a single-author arXiv preprint (2304.10163, v3 April 2025) with no journal reference. The peer-reviewed Sokolov–Voronov paper (Discrete Mathematics 349, 2026) cites it as established. "Mathematicians have shown" is defensible but slightly overstates the certainty.
- **Fix (+1 word, optional):** "…forbidding distances near one too, and a recent proof shows {#seven} the answer is exactly seven."

### 6. LOW: S09_Breakthrough [3.1]: "built from" versus "packed with"
- **Sentence:** "Another, {#forbids} built from Moser spindles, forbids it in its central wheel."
- **Problem:** M is not literally assembled from whole spindles. De Grey builds it from the edge directions of tightly linked spindles (graph V, then W, then M), aiming for a "high density of Moser spindles" (§4). Soifer describes it as a construction he "floods … with lots of Mosers' Spindles".
- **Fix (±0 words):** "Another, {#forbids} packed with Moser spindles, forbids it in its central wheel."

### 7. LOW (optional): S04_Triangle [5.0]: stated too broadly
- **Sentence:** "So we can forget the plane and draw {#dots} only dots and sticks."
- **Problem:** Dots and sticks are enough only for showing that *more* colors are needed. The upper bound (S07) still needs the whole plane, and S08 says so. The next sentence limits the claim well enough, so this is only a nitpick.
- **Fix (+2 words, only if the budget allows):** "So for now, we can forget the plane and draw {#dots} only dots and sticks."

### 8. NOTE, no change required: S09_Breakthrough [0.1]
- "He was a biologist known for his work on aging, doing math as a hobby." The facts are fine (Quanta: "a biologist"; paper title: "amateur mathematician"). The past tense can sound as if he has died. The fact sheet chose past tense for sensitivity reasons. Because it is anchored in 2018, it is acceptable. Keep it, or use "He's a biologist…".

---

## Visual and animator notes (mathematical faithfulness)

1. **S08 [0]:** A mini Moser spindle tagged "at least 4" sits above the 1950 tick. The spindle was published in 1961, and S06 says so, so this is anachronistic. Nelson's 1950 argument is not documented. Use a plain "at least 4" tag at 1950 and, if wanted, a small spindle icon at the 1961 tick.
2. **S09 [3]:** "A flower-like cluster of about 13 small wheels, label 'forces a triple somewhere'". The 13-wheel graph (J, 31 points) does *not* force a triple. The forcing graph is L, with 121 points and 52 wheels. The scene carries an "illustration" tag, but drop the "13" (say "a cluster of wheels") so no one reads it as J.
3. **S06 [0]:** The coordinates in the note are slightly off. With UNIT 1.8 and A = (0, −2.0), the top tips sit at y ≈ 0.985 (not 1.1), and the ring's top at y ≈ 2.79 (not 2.9). Both are still in frame. Use `geom` values, not the prose numbers.
4. **S01 [0] and S11 [4], [6]:** The random seven-color Voronoi mosaic with cells about 0.3 units wide is *not* a valid coloring: many of its unit pairs are same-colored. The stick only lands on hand-picked spots, which is fine as an illustration. The finale, however, shows GOOD checks on "this endless floor" as if the floor were valid. Consider morphing the finale floor into Isbell's hexagon pattern, which really is valid, or avoid implying the floor is a solution.
5. **S07 [2]:** The note asks for "flat-top" hexagons, but `hexagon_check.py` uses pointy-top. This is harmless: the axial color rule (q + 3r) mod 7 is independent of orientation, because both orientations have the same six neighbor offsets. Check only that `geom.hex_color` and `hex_cells` use the same axial convention.
6. Checked and correct: triangle crossings at (0, −0.2 ± 1.732) in S04 and S05. The diamond colorings in S05 [1] and [4] are all valid. In S06 [3], B2 and C2 are adjacent only to A, to each other and to D2, so the dead end is genuine. The wheel coloring in S09 [2] is valid. A unit stick inside a unit checkerboard square is possible (diagonal √2 > 1). The squares have side 2/3 (diagonal 0.943, same-color gap 1.333). The text "4¹⁵⁸¹ ≈ 10⁹⁵², 952 digits" is right. The 11 spindle sticks with no accidental unit pairs, the absence of a 3-coloring, and the crossing sticks (for example B1–C1 crosses A–C2) all check out.

## Pronunciation (minor)
- `Hadwiger /hˈædvɪɡəɹ/` gives "HAD-vig-er" (/æ/ as in "cat"), not the "HAHD-vig-er" the note promises. If "HAHD" is wanted, use /hˈɑːdvɪɡəɹ/. Either is acceptable in English.

---

## Claims verified as correct (no change)

| Narrated claim | Status | Source |
|---|---|---|
| Nelson asked it in 1950, aged 18, as a student | ✔ (Soifer: "at a tender age of 18 in November 1950"; Quanta: "a student at the University of Chicago"; born 4 May 1932) | soifer.pdf; Quanta 2018-04-17; Wikipedia Edward Nelson |
| Only exactly one unit is forbidden; banning all shorter distances needs endless colors | ✔ elementary | Wikipedia HN |
| A line needs exactly two colors (half-open unit stripes) | ✔ elementary | Polymath16 wiki (ℝ¹: 2/2) |
| Two crossing unit rings give an equilateral unit triangle, so at least 3 | ✔ | Wikipedia HN; de Grey & Parts 2023 (v₃ = 3) |
| A diamond has five sticks, its tips are √3 ≈ 1.73 apart, and they must match with 3 colors | ✔ | Wikipedia Moser spindle; spindle_check.py |
| The rotating copy's tip gap goes from 0 upward and hits 1 at 33.557° | ✔ (2√3·sin(φ/2) = 1) | recomputed |
| Spindle: 7 dots, 11 sticks, sticks cross, not 3-colorable, so at least 4 | ✔ | Wikipedia; spindle_check.py |
| Published by the brothers Leo and William Moser, 1961 | ✔ | Wikipedia (Moser & Moser 1961, Canad. Math. Bull. 4) |
| Squares with 9 colors work; hexagons just under one unit corner to corner work with 7; borders are fine | ✔ | de Grey §1; hexagon_check.py; recomputed |
| Isbell, Nelson's 20-year-old friend, found the 7-coloring in 1950 | ✔ (Soifer: "his 20-year old friend John Isbell"; born 27 Oct 1930) | soifer.pdf; de Grey §1; Wikipedia Isbell |
| Nelson already knew 4 in 1950; bounds 4–7 from 1950 on | ✔ (de Grey: "The lower bound was also noted by Nelson") | de Grey §1; Soifer |
| No change in 1970, 1990 or 2010; 68 years | ✔ (de Grey: "Since 1950, no improvement has been made to either bound") | de Grey §1; Soifer; Aaronson |
| De Bruijn–Erdős 1951; under the standard axioms, a fifth color needed implies a finite trap | ✔ (needs a weak form of the axiom of choice, so "standard rules" is right) | Wikipedia dBE theorem; Aaronson |
| Erdős suspected at least five | ✔ (Soifer: "Paul Erdős thought χ ≥ 5") | soifer.pdf |
| De Grey posted his paper in April 2018; biologist known for work on aging; amateur | ✔ (arXiv v1 8 Apr 2018) | arXiv 1804.02385; Quanta |
| Wheel = center plus 6 on its ring; key question: three alternate corners the same color | ✔ (H: 7 points, 12 edges; 2 of its 4 essentially different colorings have a monochromatic triple) | de Grey §1 |
| One structure forces a triple somewhere, another forbids it; attach one to every wheel | ✔ (L: 52 copies of H; M forbids a triple in its central H; N = 52 copies of M) | de Grey §1, §4.2 |
| Over twenty thousand dots, trimmed to 1,581 | ✔ (20,425 → 1,581, "a factor of nearly 13") | de Grey §4.2, §5.1 |
| More colorings than atoms | ✔ (4¹⁵⁸¹ ≈ 10⁹⁵² ≫ 10⁸⁰) | recomputed |
| Program: fix a few colors, follow forced ones, backtrack | ✔ (depth-first search; "fixing of only 20 or so colours … lets almost all remaining colours be forced") | de Grey §4.3 |
| Others checked it within days with different programs | ✔ (Aaronson, 11 Apr 2018: "independently verified, using different SAT-solvers") | scottaaronson.blog/?p=3697 |
| Professionals and amateurs teamed up online | ✔ (Polymath16, proposed 10 Apr 2018) | polymathprojects.org; Mixon blog |
| Down to 874 within a week | ✔ (Heule, 874 vertices, created 14 Apr 2018; paper 8 Apr) | Soifer essay; Aaronson |
| Parts found 509 by 2020, still the smallest known | ✔ (509 v / 2,442 e; Parts posted it 7 Mar 2020; MathWorld, 2 Sep 2026: still the record; spindle-free graphs of 2026 are larger) | arXiv 2010.12665; MathWorld; arXiv 2608.04542 |
| Parts wrote a proof checkable by hand | ✔ ("can be verified manually without the help of the computer") | arXiv 2010.12661 |
| Today: 5, 6 or 7 | ✔ | MathWorld (2 Sep 2026) |
| A six-color trap would need at least 42 dots, and none is known | ✔ ("v₆ ≥ 42") | de Grey & Parts, arXiv 2303.14714 |
| Polygon patches need all seven | ✔ (Corollary 1, χ_poly = 7, locally finite polygonal maps) | Sokolov & Voronov, arXiv 2502.01958; Discrete Math 349 (2026) |
| Thin band gives exactly seven | ✔ mathematically; preprint status (see issue 5) | Voronov, arXiv 2304.10163 |
| Either a trap five colors can't escape, or an unpainted five-color pattern | ✔ (follows from the 5–7 bounds plus de Bruijn–Erdős) | logic |
| The last big step came from a hobbyist | ✔ (2018 was the last change to either bound) | MathWorld; Quanta |

## Word budget
The mandatory fixes (1, 2, 3, 4, 6) add +7 words, and fix 5 adds +1, for a total of 1,448. Fix 7 adds +2 more and reaches exactly 1,450. Apply it only if nothing else grows.

