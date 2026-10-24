# Pedagogy research: the Riemann Hypothesis

For the script writers (drafts A/B/C) and the synthesis step. What works when you teach RH to non-experts,
what confuses people, which pictures make each step obvious, and which gap most explainers leave open.
All hard numbers still go through `research_facts.md`. Values flagged **[verify]** here are leads, not script facts.

---

## TL;DR for the script writer (numbered, in priority order)

1. **Close the gap that almost every explainer leaves: *why the location of a zero matters*.** 3Blue1Brown's zeta
   video says outright that it leaves the link to primes "unexplained". Quanta and most YouTube explainers state
   "zeros on a line" and "it's about primes" but never join the two. Our scene 8 must say, and show, three things:
   (a) each zero adds one wave to the smooth curve; (b) the zero's **height** sets how fast the wave wiggles, and its
   **real part** is the **exponent** of how fast the wave grows (size about x^(real part)); (c) **the "one half" in
   "real part one half" is the same one half as in "x to the one half" = square root.** Say (c) out loud. It is the
   single most satisfying "aha" of the topic, and almost nobody says it.
2. **Answer "why exactly one half?" with the mirror.** Zeros come in mirror pairs across the line at one half (the
   functional equation symmetry, s <-> 1 - s, plus the up/down mirror). A zero at 0.5 + d has a twin at 0.5 - d, and
   the *bigger* of the two sets the error. So the middle line is the **only** place where no twin is louder than
   √x. RH = "every zero sits on the mirror", which is the best the primes could possibly behave. This turns RH from
   an arbitrary-looking guess into a natural one. (Mathematically true, and easy to animate: a pair of zeros moving
   symmetrically off the line while their two wave envelopes split into x^0.5+d and x^0.5-d.)
3. **Make "square-root error" feel like a gold standard before zeta appears.** Mazur & Stein's framing is the best
   lay one: "estimate a number with D digits and miss by a number with about half as many digits". Estimating
   10,000 and missing by 100; estimating a million and missing by 1,000. Pair it with the coin-flip walk: after N fair
   flips, heads minus tails typically sits within about √N of zero. RH = "the primes wander from Gauss's curve no
   more than coin flips would." Keep it clearly a *comparison of error sizes*, not a claim that primes are random.
4. **Use the divergence at s = 1 twice.** In scene 5 the harmonic series (s = 1) blows up. In scene 8, that same blow-up
   point is what produces the smooth main curve in the explicit formula ("the one point where zeta explodes gives
   the smooth trend; each point where zeta vanishes adds one wave"). A true, elegant structural callback.
5. **Prime number theorem = "no zero on the strip's edge".** The 1896 proofs worked by showing no zero has real part
   exactly 1. That gives a clean ladder on the strip map: edge free (1896, ratio is right) -> middle line (RH, error
   is as small as possible). The further from the edge you can push zeros, the better the error. This also sets up
   Guth-Maynard as "a limit on how many zeros could sit out near three-quarters".
6. **Build the explicit formula the Zagier way:** first show the first 3-4 individual waves (T1, T2, T3...) *each on its
   own*, then the running sum with 1, 3, 10, 30, 100+ zeros snapping onto the staircase (Zagier's 1977 paper shows
   exactly T1..T4, then the 10th and 29th approximations). Seeing single waves before the sum is what makes
   "one wave per zero" concrete.
7. **Be honest about the smooth curve in scene 8.** With x up to ~100, Li(x) and the prime staircase differ by a
   *systematic* amount (about half of Li(√x), roughly 2-3 at x = 100, from prime squares), so "Li + waves" will not
   land on π(x). Use either Riemann's refined curve R(x) ("Riemann's own sharper version of Gauss's curve") with
   π(x), or Chebyshev's weighted staircase ψ(x) against the straight line y = x. Say which, in one sentence.
8. **Waves wiggle in log x, not x.** x^(i t) = a rotation by angle t·ln x. On a linear x-axis the oscillations spread out
   as x grows; on a log axis they are regular. Either plot on a log axis or accept the spreading and don't call them
   "evenly spaced".
9. **Analytic continuation: say "rigid", not "no kink".** "Only one way to continue a curve without a kink" is
   *false* for ordinary real curves (many smooth extensions exist). It is true only for complex-smooth
   (angle-preserving) functions. Honest lay line: "In the complex plane, 'smooth' is so strict that a function is
   rigid: know it on any small patch and you know it everywhere it can go. So there is exactly one way to extend
   zeta." 3Blue1Brown's image: an infinite jigsaw with only one solution.
10. **Pre-empt the four big misconceptions on screen, briefly:** (a) the zeros are **not** where 1 + 1/2^s + 1/3^s + ...
    equals zero (the sum doesn't even work in the strip); (b) no "1 + 2 + 3 + ... = -1/12" detour; (c) RH does not
    give a formula for the next prime (it bounds the *overall* error); (d) proving RH would not break internet
    encryption.
11. **"Checked trillions of times" needs one sentence on why that isn't proof**, and there is a perfect true story:
    Gauss believed the count of primes always stays *below* Li(x), and every computation ever done agrees, yet
    Littlewood proved in 1914 that it eventually crosses, somewhere astronomically far out (Skewes). Evidence that
    goes on forever can still be wrong.
12. **How computers check a zero is *exactly* on the line** (a question viewers will have, since computers round):
    along the line, zeta can be turned into a real-valued wave (Hardy's Z function). A sign change proves a zero
    exactly on the line; comparing with a formula for how many zeros *should* exist up to that height (Turing's
    method) proves none were missed off the line. Nice for scene 9, optional.
13. **Hook with the paradox, end with the hum.** Zagier's two facts: primes "grow like weeds among the natural
    numbers, seeming to obey no other law than that of chance", yet "obey these laws with almost military precision".
    Open on the jagged staircase close-up, zoom out to the smooth curve. Close on the same staircase, now rebuilt
    from waves, each wave tied to a dot on one line.
14. **Recurring device (recommendation):** a small **critical-strip map** with a fixed home (right third or a corner
    inset): the strip appears when the plane is introduced, the edge line at 1 lights up at the PNT beat, the first
    zero lands at 14.13 in scene 7, more zeros fill in as the explicit formula adds waves, a hypothetical off-line
    zero is shown in BAD and removed, and the verified height climbs in scene 9. Alternative: an "error meter"
    showing (count - curve)/√x staying inside a fixed band. The strip map tracks the story better; the meter is a
    good one-scene visual.

---

## 1. How the best explainers teach it

| Source | Arc / what it does well | What it leaves out |
|---|---|---|
| **3Blue1Brown, "Visualizing the Riemann zeta function and analytic continuation" (2016)** | Grid-deformation of the plane; complex powers as rotations, the sum as a spiral that converges; continuation via angle-preservation, "incredibly restrictive", "only one possible extension, if one exists at all"; jigsaw metaphor. | Says it will not explain why zeta "carries so much information about primes". No explicit formula, no error term. |
| **Mazur & Stein, *Prime Numbers and the Riemann Hypothesis* (2016; draft notes 2007)** | States RH **without zeta first**: "the staircase of primes is approximated with essentially square-root error". Defines "good approximation" as missing by a number with half as many digits. Devil's committee fable (miscounting by random errors gives √N-size error). "Tinkers with the carpentry" of the staircase to get ψ (steps of height log p at prime powers), which hugs the 45-degree line y = x. Then Fourier/spectrum: the zero heights 14.13, 21.02, ... are the "spectrum" of the primes. | Part II (spectra, distributions) is too heavy for lay viewers. |
| **Zagier, "The first 50 million prime numbers" (1977)** | The weeds / military precision paradox; table comparing π(x), Li(x), R(x); Riemann's formula π(x) = R(x) - Σ R(x^ρ); shows single waves T1..T4 and then the 10th and 29th approximations. | Says little about why RH matters beyond "far-reaching consequences". |
| **Quanta, Guth-Maynard article (Cepelewicz, July 2024)** | Zeta via 1 + 1/4 + 1/9 + ... = π²/6 (1.64) vs the diverging harmonic series; complex plane as a coordinate plane; RH as "exceptions"; "Mathematicians have no idea how to prove the Riemann hypothesis. But they can still get useful results just by showing that the number of possible exceptions to it is limited." Maynard's gambit analogy. | Doesn't explain *why* zeros control primes. |
| **Scientific American (Kontorovich, Maynard quotes)** | Orchestra metaphor: RH ensures "all these different instruments in the orchestra of the primes play at exactly the same volume"; without it, a "conductorless symphony". Maynard: "I just don't really have any good idea of how to get started." | Metaphor only, no mechanism. |
| **riemann.adilmoujahid.com (interactive, 5 levels)** | Order: atoms of arithmetic -> infinite series -> zeta ("golden key") -> critical line -> where we stand. Slider that adds 0..100 zeros to rebuild the staircase; the real part as a "volume knob"; square-root error as fair coin flips; a box of what RH does **not** say (no prime formula, no even spacing). Line: "The zeros are not bookkeeping; they are the frequencies of the primes." | Secondary source; use the ideas, not the claims. |
| **Tao (blog)** | Cleanest one-line mechanism: "each zero induces an oscillation ... the zero controlling the frequency of the oscillation and the rate to which the oscillation dies out [or grows]"; calls it "the music of the primes". | Written for mathematicians. |
| **Watkins (Exeter) encoding pages** | Animations of R_n(x) converging to π(x) as zero pairs are added; the derivative shows spikes at primes appearing "as bands of light". | Web 1.0; idea only. |

**The shared pattern of the best ones:** primes -> staircase -> smooth guess -> *how good is the guess?* -> zeta as the
tool -> zeros -> zeros are the wiggles. The explainers that feel most satisfying (Mazur-Stein, Zagier) make the
**error term** the main character. The ones that feel hollow (most YouTube RH videos) make the **zeros** the main
character and never pay off why their location matters. Our brief already follows the good pattern; keep it.

---

## 2. Intuitions and "aha" framings, scene by scene

**Scene 1 (hook).**
- Zagier's paradox (weeds vs military precision) is the best one-sentence hook. It sets up the whole video: *both*
  are true, and RH is the exact statement of how they fit together.
- Concrete image: a strip of 1..100 with primes lit; ask "where is the next one?" (1.2 s pause); then zoom out.
- Honest status up front (on brand): Riemann 1859, "very likely" (his words: "sehr wahrscheinlich"), Clay prize,
  checked for trillions of zeros, never proved.
- Avoid the Hilbert "slept for a thousand years" quote as a fact. No primary source is known; if used at all, say
  "Hilbert is said to have said".

**Scene 2 (staircase).**
- Name it the "prime staircase" (du Sautoy's phrase, adopted by Mazur-Stein). One step up at every prime. Show it
  jagged close up (up to 30), then zoom out (up to 1000, then 10^5): it looks smooth. The zoom-out *is* the
  argument that there's a law to find.

**Scene 3 (Gauss).**
- Mazur-Stein's lay version of 1/ln x: "the chance that a number is prime is inversely proportional to its number
  of digits". Every extra digit adds about 2.3 to ln x: near 1,000 about 1 in 7, near a million about 1 in 14, near
  a billion about 1 in 21 (ln 10^3 = 6.9, ln 10^6 = 13.8, ln 10^9 = 20.7).
- Li(x) as "add up the chances": shade the area under 1/ln t (Mazur-Stein's figure: "the expected tally of primes
  < X is the area under the graph").
- Gauss's 1849 letter to Encke with his count below 3 million is a lovely detail, but the numbers vary between
  sources (Mazur-Stein: Gauss said 216,745; true count 216,816; Gauss's curve 216,971; they call the true miss
  "161", but 216,971 - 216,816 = 155). **[verify: compute with mpmath and use our own number]**
- **Confusion to bust:** the prime number theorem is a *ratio* statement. Show two readouts side by side as x grows:
  ratio -> 1.00, while the *difference* keeps growing. That makes "the real question is the size of the error"
  (scene 4) feel necessary rather than pedantic.

**Scene 4 (error size, coin flips).**
- Coin-flip walk: heads +1, tails -1; plot several walks with the ±√N envelope. Then: RH ⇔ the prime staircase
  stays within about √x (times a log) of Li (Koch 1901; explicit form by Schoenfeld 1976:
  |π(x) - Li(x)| < √x·ln x / (8π) for x ≥ 2657, iff RH). **[verify via facts file]**
- "Half the digits" framing (Mazur-Stein): "estimate a ten-digit number and miss by a five-digit number".
- The coin analogy has a precise mathematical cousin (Denjoy's heuristic): if the Möbius function's ±1 values were
  independent coin flips, RH would hold with probability one. It is a heuristic, not a proof: the real values are
  deterministic. So say "as if", never "the primes are random".
- Caution for visuals: over the whole computed range, π(x) stays **below** Li(x). Don't draw the staircase
  crossing above Li, and don't say "above and below" for π vs Li.

**Scene 5 (zeta, Euler product).**
- s = 2: 1 + 1/4 + 1/9 + ... = π²/6 ≈ 1.645 (Quanta uses this too). s = 1: harmonic series diverges (classic
  pairing proof: 1/3 + 1/4 > 1/2, 1/5..1/8 > 1/2, ...).
- **Euler product as a sieve** (the standard lay derivation; a perfect Manim beat, no algebra needed): write the row
  1, 1/2^s, 1/3^s, 1/4^s, ...; multiply by (1 - 1/2^s) and every even term greys out; multiply by (1 - 1/3^s) and
  the multiples of 3 grey out; ... only "1" survives. So the sum times one factor per prime = 1, i.e. sum = product
  over primes. It is literally the sieve of Eratosthenes running inside the sum. Line: "the sum knows every whole
  number; the product knows only primes; they're the same thing."

**Scene 6 (complex plane, continuation).**
- Treat complex numbers as points on a plane (Quanta does this); avoid "imaginary means fake". The only thing
  viewers must feel is: a power with an "upward" exponent **spins** (n^(-it) is a rotation by t·ln n), so the terms
  of the sum become a **spiral** (3Blue1Brown's picture). Spiral converges when real part > 1.
- Gentle on-ramp for continuation (common in teaching): 1 + x + x² + x³ + ... equals 1/(1 - x) only for |x| < 1, but
  the formula 1/(1 - x) keeps working beyond. The sum was just one window onto a bigger function. **Do not** then
  say "so 1 + 2 + 4 + ... = -1"; say "the sum stops working, the function doesn't".
- Rigidity wording (see TL;DR 9). 3Blue1Brown: "incredibly restrictive"; "forces you into only one possible
  extension".
- Map visual: a moving input dot and its output dot (clearer for lay viewers than domain colouring). Domain
  colouring looks great but needs a legend and costs time.

**Scene 7 (zeros).**
- "Trivial" means easy and fully understood, not unimportant. One sentence is enough: they come from the extension
  itself.
- Why the strip: to the right of 1, the prime product can't be zero (a product of non-zero factors); by the mirror
  symmetry, left of 0 only the easy zeros remain. That leaves the strip.
- Iconic visual: the path of ζ(1/2 + it) as t climbs is a looping curve that **passes through the origin** at each
  zero (first at t ≈ 14.1347). Alternative: Hardy's Z(t), a real wave whose crossings are the zeros; lay viewers read
  it instantly and it sets up how computers check (TL;DR 12).
- State RH with the mirror (TL;DR 2) so it doesn't feel arbitrary.

**Scene 8 (central argument).** See TL;DR 1, 2, 4, 6, 7, 8. Mechanism for the storyboard:
- ψ version (cleanest): ψ(x) = x - Σ_ρ x^ρ/ρ - ln(2π) - ½ln(1 - x^(-2)). Each conjugate pair contributes
  -2·Re(x^ρ/ρ) = -(2√x/|ρ|)·cos(t·ln x - arg ρ) when ρ = ½ + it. Envelope ±2√x/|ρ|; for the first zero about
  ±0.14√x. Higher zeros: faster wiggles, smaller amplitude (1/|ρ|), which is why the first few carry the shape.
- π version: π(x) = R(x) - Σ_ρ R(x^ρ) (sum over zeros in order of height, plus tiny trivial-zero terms); Zagier's
  T_n(x) = -R(x^ρn) - R(x^ρ̄n). Envelope roughly √x/(|ρ| ln x) per pair.
- Honest notes: the sum must be taken in order of height and needs *all* zeros to be exact; a finite number gives a
  smooth curve with ringing near each step (like Fourier series near a jump). Say "with more and more zeros, the
  curve sharpens into the staircase".
- The "rogue zero" demo: slide one zero (and its mirror twin) off the line to real part 0.8 and show its wave's
  envelope growing like x^0.8 and swamping the others: "primes lumpier". Colour it BAD, then put it back.
- "Music" is fine as a metaphor if it stays concrete: each zero is a pure tone; height = pitch, real part = how
  quickly that tone gets louder; RH = all tones swell at the same rate (Kontorovich's "same volume" framing). No
  mysticism, no "the universe hums".

**Scene 9 (story/evidence).**
- Siegel (1932) found in Riemann's unpublished notes that he had computed zeros by hand: "very likely" was not a
  wild guess. Hilbert 1900 (8th problem). Hardy 1914: infinitely many zeros on the line. Proportions: Conrey 1989
  (> 40%); current best lead is Pratt-Robles-Zaharescu-Zeindler (2020): more than five-twelfths (≈ 41.7%)
  **[verify]**. Largest rigorous verification lead: Platt & Trudgian (2021), all zeros up to height 3·10^12 on the
  line, 12,363,153,437,138 of them **[verify; check for anything newer]**. A 2025/26 arXiv paper by Goldston &
  Suriajaya on "2/3 of zeros on the line" is about Montgomery's method *assuming* RH or aiming to remove it; do not
  cite it as a new unconditional record without the facts researcher confirming.
- Montgomery-Dyson (April 1972, tea at the Institute for Advanced Study): Montgomery mentions his formula for how
  zeros are spaced; Dyson recognises it as the formula for energy levels in random-matrix models of heavy nuclei.
  Lay line: zeros repel each other, like energy levels. Optional, 2-3 sentences max, and don't imply it proves
  anything.

**Scene 10 (today, why hard).**
- Why checking isn't proof: Littlewood/Skewes (TL;DR 11). Second true example: the Mertens conjecture, consistent
  with all computations, disproved in 1985 (Odlyzko & te Riele) without an explicit counterexample **[verify]**.
- Guth-Maynard (arXiv May 2024; Annals of Mathematics 2026 **[verify volume/date]**): lay statement that is still
  accurate: "They proved there can't be too many zeros far off the line, especially near three-quarters, beating a
  bound that had stood for about 80 years (Ingham, 1940 **[verify]**). It's not a proof of RH; it's a better limit on
  how many rebels there could be, and it already sharpens what we know about primes in short stretches."
  Quanta: "Mathematicians have no idea how to prove the Riemann hypothesis. But they can still get useful results
  just by showing that the number of possible exceptions to it is limited." Iwaniec: "It's a sensational result."
  Maynard's own view: the method probably can't reach the full hypothesis.
- "Thousands of theorems start with 'if RH is true'" (Kontorovich: "There are hundreds of papers that prove 'x is
  true if RH holds'"). Use "hundreds, maybe thousands" or quote carefully.

**Scene 11 (callback).** Return to the opening staircase at the same framing; overlay the rebuilt curve; each wave
lights up a matching dot on the strip map's line. Final line should restate the audience promise almost word for
word (brief's promise paragraph), then end on honest status ("Nobody has proved it. Yet.").

---

## 3. Usual points of confusion (and a one-line fix each)

1. **"The zeros are where the sum is zero."** No: in the strip the sum doesn't converge. Fix: show the sum's region
   (right of 1) shaded, the strip outside it, and say "the zeros live where only the extended function reaches".
2. **-1/12 and "divergent sums equal numbers".** Don't raise it; if continuation is shown, say the sum *stops
   working*, the function continues.
3. **"RH lets us predict primes / gives a prime formula."** It controls the *size of the overall error*, not where
   the next prime is.
4. **"RH breaks encryption."** No: factoring stays exactly as hard. (Worth one clause at most, or skip.)
5. **"Verified for trillions, so it's basically proven."** Skewes/Littlewood story.
6. **PNT vs RH.** PNT = right on average (percentages); RH = how far off, in absolute numbers. The ratio/difference
   readout (scene 3) fixes it.
7. **"Why one half, of all numbers?"** Mirror symmetry + "one half = square root" (TL;DR 1, 2).
8. **"Imaginary numbers are made up."** Points on a plane; upward exponents spin.
9. **"Critical line" vs "critical strip"**, "trivial zeros" sounding unimportant. Keep vocabulary to: *the strip*,
   *the line at one half*, *easy zeros*, *interesting zeros*. Introduce the official words once, as labels.
10. **Waves "evenly spaced" in x.** They are regular in log x.
11. **"Error ~ √x" sounds small but still grows.** Say it as a bound, not a typical value: below a trillion there are
    about 37.6 billion primes, Li misses by only about 38 thousand, comfortably inside √x = one million
    **[verify with mpmath / known tables: π(10^12) = 37,607,912,018; Li - π ≈ 38,263]**. The real error is usually
    well below the RH bound; don't imply it sits right at √x.
12. **"RH says zeros are evenly spaced."** No; it says nothing about spacing. Spacing statistics are Montgomery-Dyson,
    a separate (conjectural) story.
13. **"Real part" as a word.** Say "how far right it sits" or "its left-right position" at first, then "real part".

---

## 4. Visual ideas that make each step obvious (all doable in Manim without LaTeX)

- **Staircase zoom** (jagged at 30 -> smooth at 10^5) with a Li curve fading in; the zoom is the hook's payoff.
- **Probability strip:** numbers as tiles; a translucent band whose density drops as 1/ln x; the "digits" counter.
- **Area under 1/ln t** filling as x slides: Li as accumulated chance.
- **Ratio vs difference readouts** (two Palatino numbers) as x grows by powers of 10.
- **Coin-flip walks** (5-7 walks in PALETTE colours) inside a ±√N envelope; then the prime error curve drawn in the
  same envelope shape (rescaled honestly, e.g. by √x·ln x, or plotted (π - Li)/√x).
- **Euler sieve row:** terms grey out in waves, primes' factors appear on the left; ends with sum = product.
- **Spiral of partial sums** for a complex input (3Blue1Brown); for real part > 1 it settles, for less it doesn't.
- **Input dot / output dot** map; a path along the line at one half and its looping output hitting 0.
- **Strip map** (recurring device): shaded strip 0..1, gold line at ½, zeros as dots with rims, labelled heights
  14.13, 21.02, 25.01, 30.42, 32.94 (first five zero heights, per Zagier's table **[verify]**).
- **One wave per zero:** a zero dot on the strip map sends a coloured wave to the graph panel; envelope ±c√x drawn
  faintly; then the running sum over 1, 3, 10, 30, 100 zeros converges on the staircase.
- **Rogue zero slider:** drag a zero pair to 0.5 ± 0.3; its envelope opens to x^0.8; the rebuilt staircase grows
  lumpy (BAD colour); shake once; snap back.
- **Mirror:** fold the strip about the gold line; off-line zeros show their twin; the louder twin sets the error.
- **Hardy Z wave** for "how computers check": crossings tick a counter; a "should be" counter from the zero-counting
  formula; they match.

---

## 5. Hooks and endings

**Hooks (pick one, 1-3 sentences):**
- Zagier paradox: "Primes grow like weeds ... and yet obey laws with almost military precision." (quote or
  paraphrase; attribute to Don Zagier).
- The zoom: "Up close, the primes look like noise. Step back, and they draw a smooth curve. The Riemann Hypothesis
  is about the tiny gap between the two."
- Viewer question: "Where's the next prime after 113?" (pause) -> "Nobody can say without checking. But how many
  primes are below a trillion? That, we can predict, astonishingly well, and one guess from 1859 says exactly how
  well."

**Endings (callback):**
- Same staircase, same framing as the opening, now drawn by the waves; the strip map's zeros glow in time with the
  waves. "Every wobble in this staircase is a zero on that one line, as far as anyone has ever checked. Whether all
  of them are there is the Riemann Hypothesis. Nobody knows yet."
- Echo the audience promise from the brief nearly verbatim; it's a good closing paragraph.

---

## 6. The single biggest conceptual gap

**Explainers say the zeros "control" the primes but never show *how the position of a zero turns into the size of
the error*.** The missing chain is short and fully visual:

pole at 1 -> smooth curve; each zero -> one wave; wave size ≈ x^(real part of the zero);
real part ½ -> size √x = x^½ (the same one half!); mirror symmetry -> ½ is the only place no twin is louder;
so RH <=> the error is as small as it could possibly be (≈ √x, the coin-flip size).

Everything else (zeta, continuation, the strip) is scaffolding for this chain. If scene 8 lands this, the video
beats the famous explainers on exactly the point they skip.

---

## Sources

- 3Blue1Brown, "Visualizing the Riemann zeta function and analytic continuation" (2016): https://www.3blue1brown.com/lessons/zeta/
- B. Mazur & W. Stein, *What is Riemann's Hypothesis?* (draft, 2007): https://wstein.org/edu/2007/simuw07/notes/rh.pdf ; book *Prime Numbers and the Riemann Hypothesis* (CUP 2016), chapters "The staircase of primes", "The spectrum and the staircase of primes": https://www.cambridge.org/core/books/abs/prime-numbers-and-the-riemann-hypothesis/staircase-of-primes/7E173341C6C690C2E5D4D0F82C34AD8C
- D. Zagier, "The first 50 million prime numbers", Math. Intelligencer (1977): https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF03039306/fulltext.pdf
- Quanta, "'Sensational' Proof Delivers New Insights Into Prime Numbers" (July 2024): https://www.quantamagazine.org/sensational-proof-delivers-new-insights-into-prime-numbers-20240715/
- Quanta video, "The Riemann Hypothesis, Explained" (Kontorovich): https://www.quantamagazine.org/videos/the-riemann-hypothesis-explained/ ; essay: https://www.quantamagazine.org/how-i-learned-to-love-and-fear-the-riemann-hypothesis-20210104/
- Scientific American, "The Riemann hypothesis is a million-dollar math problem hardly anyone is trying to solve": https://www.scientificamerican.com/article/the-riemann-hypothesis-is-a-million-dollar-math-problem-hardly-anyone-is-trying-to-solve/
- Guth & Maynard, "New large value estimates for Dirichlet polynomials", arXiv:2405.20552: https://arxiv.org/abs/2405.20552 ; Annals of Math. 203(2): https://projecteuclid.org/journals/annals-of-mathematics/volume-203/issue-2/New-large-value-estimates-for-Dirichlet-polynomials/10.4007/annals.2026.203.2.6.short
- T. Tao, "explicit formula" posts: https://terrytao.wordpress.com/tag/explicit-formula/
- M. Watkins, encoding of primes by zeta zeros: https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/encoding1.htm
- Interactive explainer (secondary): https://riemann.adilmoujahid.com/hypothesis
- Wikipedia, Riemann hypothesis (Koch/Schoenfeld, Riemann's "sehr wahrscheinlich"): https://en.wikipedia.org/wiki/Riemann_hypothesis ; Skewes's number: https://en.wikipedia.org/wiki/Skewes's_number
- Hilbert quote provenance (apocryphal): https://en.wikiquote.org/wiki/David_Hilbert
- Montgomery-Dyson tea story: https://www.ias.edu/ideas/2013/primes-random-matrices ; https://cims.nyu.edu/~bourgade/papers/TeaTime.pdf
- Platt & Trudgian, "The Riemann hypothesis is true up to 3·10^12", Bull. LMS (2021): https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.12460
- Goldston & Suriajaya, "Zeta Zeros on the Critical Line", arXiv:2511.20059: https://arxiv.org/abs/2511.20059
- Denjoy heuristic / Möbius random walk: https://arxiv.org/pdf/2607.25002
- Hardy Z and Turing's method: https://arxiv.org/pdf/1601.06512 ; https://arxiv.org/pdf/1710.00603

