# Adversarial fact-check: script_synth.json

Reviewed on 2026-09-28. I checked every narrated sentence and every storyboard that says something is exact or valid.
New computations are in `script/checks/review_facts_check.py`. It runs in about 1 s with `engine/.venv/bin/python`.
Web sources are listed at the end.

**Verdict:** the script is in good shape. I found no false dates, names or numbers. There is 1 wrong historical claim, 2 overclaims that an expert viewer would catch, and a few clarity and faithfulness points.
The spoken word count is now **1,445**, against a limit of 1,450. The fixes below are word-neutral or change the count by at most ±2 words.

---

## Issues, most severe first

### 1. MEDIUM-HIGH: S09 P0 says Riemann's paper gives no reason (wrong)
- **Sentence:** "What made Riemann so sure? His paper doesn't say, and he died at thirty-nine."
- **Problem:** the paper does give a reason, in the sentence just before "very probable": *"Man findet nun in der That etwa so viel reelle Wurzeln innerhalb dieser Grenzen, und es ist sehr wahrscheinlich, dass alle Wurzeln reell sind."* In English: "Indeed, one finds between those limits about that many real zeros, and it is very probable that all zeros are real." (Riemann 1859; quoted in Bombieri's official Clay problem description.) Riemann said he had found about as many zeros on the line as his count predicted. The research sheet (§1.1) leaves out this clause, and the synth "purpose" line repeats the error ("Riemann's paper gives no reason").
- **Fix (+1 word):** "What made Riemann so sure? His paper offers only a hint, and he died at thirty-nine."
  - Alternative (+6 words, if the budget allows): "His paper gives one line: he'd found about as many zeros on the line as he expected."
- The next beat ("Siegel dug through Riemann's unpublished notes … no wild guess") still works, and now reads as "the notes showed the work behind that hint".

### 2. MEDIUM: S05 P2 says smoothness on a plane is stricter (false without "complex")
- **Sentence:** "But on a plane, being smooth is a far stricter demand than on a line."
- **Problem:** this is false for ordinary smoothness. A smooth function of two real variables can be extended in many ways, just as on a line. Uniqueness holds only for *complex*-differentiable (analytic) functions, because of the identity theorem. The research sheet lists this as misconception #6. The next two sentences ("locked in everywhere else", "exactly one smooth way") depend on this qualifier.
- **Fix (word-neutral, 15 → 15):** "But for complex inputs, being smooth is a far stricter demand than on a line."
- **Visual support:** in S05 P0, at {#up}, change the DIM note 'i marks the up-part' to 'points like 2 + 3i: complex numbers' (i marks the up-part), so that "complex" is on screen before it is spoken.

### 3. MEDIUM: S10 P3 overstates Guth and Maynard
- **Sentence:** "It was the first real progress there since nineteen forty."
- **Problem:** "there" means "zeros far from the line" (the sentence before). But Ingham's 1940 bound was improved for zeros with real part above ¾ in the 1960s and 1970s (for example Huxley, 1972). Quanta says this too: "Around the same time, mathematicians also introduced new techniques that improved Ingham's bounds for zeros with a real part greater than 3/4." What Guth and Maynard did was beat Ingham's bound in the critical range around real part ¾, which is "a record that had been set more than 80 years earlier" (Quanta).
- **Fix (10 → 9 words):** "It beat a record that had stood since nineteen forty."
- **Visual:** change the tag 'best since Ingham, 1940' to 'beats Ingham's 1940 bound (near real part ¾)'.

### 4. LOW-MEDIUM: S01 P2 says no formula finds the next prime
- **Sentence:** "No formula tells you; you check."
- **Problem:** exact prime formulas do exist, for example Willans (1964) and Mills' constant. They are useless in practice, but pedants will point this out in the comments.
- **Fix (+1 word):** "No simple formula tells you; you check."

### 5. LOW-MEDIUM (clarity, can mislead): S01 P0 reads two ways
- **Sentence:** "Primes can't be split into smaller factors, like seven or thirteen."
- **Problem:** heard aloud, "like seven or thirteen" can attach to "smaller factors", as if seven and thirteen were examples of factors.
- **Fix (word-neutral):** "Primes, like seven or thirteen, can't be split into smaller factors."

### 6. LOW: S02 P0 compresses Gauss's counting into his teenage years
- **Sentences:** "…a teenager, Carl Friedrich Gauss, around seventeen ninety-two. In idle quarter hours, he counted primes in blocks of a thousand."
- **Problem:** the letter to Encke (24 Dec 1849) says he began in 1792 or 1793 by counting "several chiliads". The "idle quarter of an hour … another chiliad here and there" counting went on for decades. By 1849 the counts reached **3,000,000** ("the first three millions have been counted"). The narration is not false, but it suggests a teenager did all the counting.
- **Fix (+2 words, optional):** "Over the years, in idle quarter hours, he counted primes in blocks of a thousand."
- **Visual (needed):** the bars for 10M and 100M are blocks that Gauss never counted. Give those two bars a DIM tag 'counted today', or put a thin DIM divider after the 1M bar with the label 'Gauss's tables reached 3 million'.

### 7. LOW: S10 P1 "below Gauss's curve" is false for x = 2 to 7 if the curve is Li
- **Sentence:** "For every number anyone has checked, the staircase stays below Gauss's curve."
- **Problem:** this is true for li(x), which is proved for all x from 2 up to 10¹⁹ (Büthe 2015). It fails for Gauss's own offset integral Li(x) = li(x) − 1.045 at x = 2, 3, 4, 5 and 7 (computed). The video labels li as "Gauss's curve" everywhere, so it is consistent, but only if `topic.li_curve` really is li and not Li.
- **Fix:** no narration change. **Animator:** `topic.li_curve` must be li(x) (mpmath `li`), not `li(x) − li(2)`. The S10 gap graph starts at x = 10, where li − π = 2.17 > 0, which is correct.

### 8. LOW: S10 P1 hedge on Skewes
- **Sentence:** "…John Littlewood proved it must cross above, probably first near a number three hundred and seventeen digits long."
- **Status:** Littlewood 1914 (infinitely many sign changes) is correct. A crossing region near e^727.95 ≈ 1.397 × 10³¹⁶ is correct, and that number has 317 digits (computed). But Wikipedia (Skewes's number) says: "It is not known whether this is the smallest crossing." "Probably" is a defensible hedge. A safer version (word-neutral): "…proved it must cross above, possibly first near a number three hundred and seventeen digits long." Keep the on-screen '≈ 10³¹⁶ ?'.

### 9. LOW: S09 P2 "the first few zeros"
- **Sentence:** "Riemann had worked out the first few zeros by hand."
- **Status:** Moree, Petrykiewicz and Sedunova (arXiv 1810.05244, §7) write: "Riemann seems to have computed only a few non-trivial zeros. He certainly found zeros at approximately 1/2 + i14.1386 and at 1/2 + i25.31, and very likely computed more." These are the first and third zeros. The sentence is acceptable. A tighter version (word-neutral): "Riemann had worked out a few zeros by hand." The visual (two dots, at 14.13 and 25.01) already shows this faithfully.
- **Visual:** label the second dot 'Riemann: 25.31', not '≈ 25.3', to match the source.

### 10. LOW: S09 P4, the 2026 result is still a preprint
- **Sentences:** "For decades, the proven share on the line stayed around forty percent. Then a new proof in twenty twenty-six pushed it past two thirds."
- **Verified:** Alpöge and Furman, arXiv 2608.13637 (v1 13 Aug 2026, v2 19 Aug 2026): "at least two thirds of the nontrivial zeros … are simple and lie on the critical line"; "the previous unconditional records are 5/12"; 0.6725 with the Montgomery–Taylor window; Lean 4 formalization; the proof was "discovered autonomously by Claude (Anthropic)". Lamzouri, arXiv 2609.02882 (2 Sep 2026), gives an independent, simpler proof of more than 67.25%. Anthropic's page (10 Aug 2026) reports 41.6% → 67.2%, with review by Conrey and Goldston. The constant 3/2 − cot(1/√2)/√2 = 0.672501 (computed).
- **Status:** true as narrated. It is not yet refereed, but it has two independent proofs and a formalization. Keep the on-screen 'preprint' tag. Do not remove it. Also keep "a share, not all".
- "For decades … around forty percent" is correct: Conrey (1989) proved more than 40%, and Pratt et al. (2020) proved more than 5/12 ≈ 41.7%.

### 11. LOW: S03 P1 "typically about a thousand"
- **Sentence:** "After a million flips, you typically end up about a thousand steps from the start."
- **Status:** the RMS distance is exactly 1,000. The mean |S| is about 798 (computed), and the median is about 674. Calling "typical" the standard deviation is standard in popular writing. It is acceptable and needs no change.

---

## Visual and animator notes on faithfulness

1. **S03 P3, Schoenfeld band.** The band √x·ln x/(8π) is valid only *if RH is true*. Unlabelled, it looks like a proven fence. Add a DIM tag on the band: 'if the Riemann Hypothesis is true'. The numbers are right: 549.7 at a million, against an actual gap of 129.5.
2. **S02 P0, block bars.** See issue 6. Gauss's own counts stopped at 3 million. The bar values 168, 135, 106, 81, 75, 61, 54 are verified.
3. **S04, Euler product.** The identity sum = product (and the sieve reading "only the one survives") holds only for s > 1. At s = 1 both sides are infinite. Add a small DIM tag 's > 1' beside the final equation in P3.
4. **S05 P1, spiral at 0.6 + 3i.** The divergence is honest but slow. The partial sums behave like ζ(s) + N^(1−s)/(1−s): a spiral of growing radius (about N^0.4/3) *centered on the extended value* ζ(0.6 + 3i) ≈ 0.552 − 0.086i. The computed distance from ζ(s) is 0.85 at 10 terms, 2.09 at 100, 5.24 at 1,000 and 6.91 at 2,000, with only about 3.6 turns in total. Never let the path look like it settles. Frame the output panel so that the growth is visible. ζ(2 + 3i) = 0.7980 − 0.1137i is verified.
5. **S05 P2–P3, domain colouring "spreading like ink".** This is fine as a metaphor for the identity theorem. It must not look as if colours outside the region right of 1 are made up. Use the real mpmath ζ values everywhere the colour spreads.
6. **S06 P5 / S08, dial and strip alignment.** This is faithful. The error exponent Θ equals the supremum of the real parts of the zeros (Ingham, Thm 30). Error = O(x^Θ log x), and it is larger than x^(Θ−ε) infinitely often. "The dial reads the rightmost zero" is correct, with a small caveat: the supremum is not necessarily attained, which is fine at this level. The dial range below ½ can never be reached (zeros on the line exist, and of each mirror pair, one zero has real part ≥ ½). No change is needed, but no beat should ever show the dial reading below ½.
7. **S06 P3, fold.** Folding about real part ½ maps β + iγ to (1 − β) + iγ = 1 − ρ̄. This is correct (functional equation plus conjugate symmetry).
8. **S07, explicit-formula rebuild (the visual heart).**
   - `topic.rebuild` must include the trivial-zero term −1/ln x + arctan(π/ln x)/π. It is −0.68 at x = 2.5, −0.14 at 10 and −0.03 at 100 (computed). Without it the "exactly" claim fails visibly near x = 2 to 10. The check script `staircase_rebuild_check.py` does include it, so mirror that in topic.py. (It is honestly "one wave per zero", because the trivial zeros are zeros too.)
   - Sum the zeros in order of height, with each conjugate pair as one real wave. The series converges only conditionally.
   - At each jump the rebuilt curve passes through the midpoint (the Gibbs-type overshoot is correct behaviour). Do not "fix" it.
   - The 100th zero is at height 236.524, so an inset range of 0 to 240 is right.
   - Optional: add a small DIM caption to 'Riemann 1859: staircase = smooth curve + one wave per zero': 'proved by von Mangoldt, 1895'. Riemann stated the formula but did not fully prove it.
   - "Waves enlarged … about a third of one step": the first-wave amplitude is 0.19 at x = 10 and 0.31 at x = 100 (computed). This is correct.
   - "Wave 5 wiggles more than twice as often": 32.935/14.135 = 2.33. This is correct.
9. **S08 P0–P1, rogue zero.** "About sixty times" is correct: x^0.3 = 63.1 at 10⁶, and the |ρ| difference changes it by less than 0.1% (63.03). Keep the 'imaginary' and 'illustration' tags on every rogue element. Note that sliding *one* zero off the line necessarily creates its twin. The storyboard already shows the twin appearing at the same moment. Keep that exact.
10. **S09 P3 counter.** Settling on '≈ 12.36 trillion' is correct. N(3.0001753328·10¹²) = 1.23632·10¹³ (computed), and it matches the Wikipedia table. Platt and Trudgian is still the rigorous record: arXiv April 2020, Bull. LMS 53(3), 2021. The web's "twenty trillion zeros" claim (mathlumen "2026 status report") has no paper behind it. Do not use it.
11. **S10 P1, Skewes graph.** Keep the far-out dip dashed with the tag 'illustration'. No explicit crossing point is known for certain.
12. **S10 P3, 'room for rebels' region.** It is good that this is a *shading-thins* metaphor rather than dots. Put it around real part ¾, as in the storyboard. Add nothing that suggests Guth and Maynard found or excluded specific zeros.
13. **S01 P4 card '1859 · about 8 pages'.** The page count is medium confidence (sources give 8, 8½ or 9). "About 8" is safe.

---

## Verified as correct (no change needed)

- **S01:** 25 primes up to 100. Next prime 101. 98 = 2 × 49, 99 = 9 × 11, 100 = 2 × 50. 12 = 2·2·3, 45 = 3·3·5, 91 = 7·13. li(10⁵) − π(10⁵) = 37.8 ("about 38"). Clay prize US$1M, open. More than twelve trillion zeros checked.
- **S02:** Gauss was 15 or 16 in 1792/93 (letter to Encke, 1849). The 19 listed primes in 1,000–1,119 and the 7 in 1,000,000–1,000,119 are exact. Average gaps: 6.94 (144 primes in 500–1,500) and 13.84 (7,227 primes in 950k–1.05M). ln values 6.91, 9.21, 11.51, 13.82. ln 10 = 2.3026. Ratios and gaps 0.946 / 9.6, 0.998 / 129.5 and 0.99987 / 754.4 are exact. PNT 1896, Hadamard and de la Vallée Poussin, independently.
- **S03:** √10⁶ = 1,000. Koch 1901: RH ⇔ π(x) = li(x) + O(√x log x). The Schoenfeld value 549.7 at 10⁶ is right. The proven window [½, 1] is correct: the lower end comes from Littlewood's Ω result, and no zero-free strip Re s > 1 − δ is known.
- **S04:** ζ(2) = π²/6 (Euler, 1734/1735). The harmonic partial sums are right. Euler product E72, presented 25 Apr 1737. Survivors after 2 and 3: 1, 5, 7, 11, 13, 17, 19, 23, 25, 29. Riemann introduced the notation ζ(s).
- **S05:** n^(−s) has length n^(−σ) and is turned by −t·ln n. Converges only for real part > 1. The unique analytic continuation has a single pole at 1, and Riemann found it.
- **S06:** trivial zeros at −2, −4, …. The nontrivial zeros are strictly inside 0 < Re < 1. The zeros 14.1347, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774 are correct. ζ(½) = −1.46. Mirror pairs are correct. The RH statement is correct.
- **S07:** Riemann set the proof aside ("vorläufig bei Seite gelassen"). The R(x) form of the explicit formula is correct. Height sets frequency (in ln x). Real part β sets growth x^β (divided by |ρ| ln x).
- **S08:** the 1896 proof works by ruling out zeros on Re s = 1, which is enough for the ratio only. "½ is the best possible" is correct.
- **S09:** Riemann 1826–1866, died at 39. Hilbert's 1900 Paris lecture, problem 8. Hardy 1914, infinitely many zeros on the line. Siegel 1932. Platt and Trudgian, 12.36 trillion zeros, rigorous. Conrey 1989 more than 40%. Alpöge and Furman 2026 more than ⅔ (see issue 10).
- **S10:** Littlewood 1914. The first crossing is not below 10¹⁹ (Büthe). A crossing region near 1.397·10³¹⁶ (317 digits). A 100% proportion would not rule out a rogue zero. Nobody can prove Θ < 0.99 (the quasi-Riemann hypothesis is open). Guth and Maynard, arXiv 31 May 2024.
- **S11:** 2026 − 1859 = 167.

## Sources
- Alpöge and Furman, arXiv 2608.13637: https://arxiv.org/abs/2608.13637
- Lamzouri, arXiv 2609.02882: https://arxiv.org/abs/2609.02882
- Anthropic, "riemann-zeta" research post: https://www.anthropic.com/research/riemann-zeta
- Platt and Trudgian, arXiv 2004.09765: https://arxiv.org/abs/2004.09765
- Quanta on Guth and Maynard (15 Jul 2024): https://www.quantamagazine.org/sensational-proof-delivers-new-insights-into-prime-numbers-20240715/
- Moree, Petrykiewicz and Sedunova, "A computational history of prime numbers and Riemann zeros", §7: https://arxiv.org/abs/1810.05244
- Bombieri, Clay problem description (quotes Riemann's "etwa so viel reelle Wurzeln…"): https://www.math.ucdavis.edu/~tracy/courses/math205A/riemann.pdf
- Riemann hypothesis (Wikipedia): https://en.wikipedia.org/wiki/Riemann_hypothesis
- Skewes's number (Wikipedia): https://en.wikipedia.org/wiki/Skewes%27s_number
- Prime number theorem (Wikipedia; Gauss 1792/93, aged 15 or 16): https://en.wikipedia.org/wiki/Prime_number_theorem
- Gauss–Encke letter context (chiliads, 3 million): https://arxiv.org/pdf/1311.1093
