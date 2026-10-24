# CHANGELOG: script_synth.json to script.json

**Result:** 11 scenes, **1,449 spoken words**. The validator estimates **~9:25** (`validate_script.py --minutes 10`: 0 ERRORs, 0 WARNs).
The pacing review measured the synth with real Kokoro audio at 9:33.3. That is 11.8 s more than the validator's 9:21.5 for the same file.
With the same offset, the final script should run about **9:36**, inside the 9:30 to 10:30 band. Run `timeline.py` to confirm.

| scene | words | est. s |
|---|---|---|
| S01_Hook | 150 | 59.9 |
| S02_Gauss | 121 | 46.7 |
| S03_CoinFlips | 179 | 69.8 |
| S04_Zeta | 130 | 50.8 |
| S05_Plane | 115 | 43.8 |
| S06_Zeros | 140 | 55.7 |
| S07_Waves | 125 | 48.9 |
| S08_OneHalf | 150 | 57.4 |
| S09_Evidence | 117 | 45.7 |
| S10_WhyHard | 127 | 48.2 |
| S11_Callback | 95 | 37.7 |
| **total** | **1,449** | **~9:25** |

**Word budget:** the synth had 1,445 words. The clarity HIGH package added about 45 and the cap is 1,450. When reviews conflicted, the order was accuracy, then clarity, then budget.
- Every fact fix is in.
- Every clarity HIGH is in, some in a slightly compressed form.
- Most MEDIUMs are in, some shortened.
- The package is funded by the clarity cut list plus a few low-value words.
- The net change is +4 words, so the pacing review's "no net word cuts" (runtime floor) also holds.

Paragraph numbers below are 1-based, as in the validator and timeline (`P1` = first paragraph). The fact review used 0-based numbers in places, and they are converted here.

---

## review_facts.md

| # | item | decision | what changed |
|---|---|---|---|
| 1 | S09 "His paper doesn't say" is wrong | **Applied** | Now "What made Riemann so sure? His paper offers only a hint." Clarity C7 also drops "and he died at thirty-nine"; the dates stay on the card. At {#hint}, the screen shows the one line: 'about as many zeros on the line as expected'. The S09 purpose, the pron note and the fact entry are corrected, with the Bombieri source added. |
| 2 | S05 "on a plane, smooth is stricter" (false without "complex") | **Applied**, merged with clarity M4 | Now "On a line, a curve can be continued smoothly in many ways. / But with complex inputs, smoothness is so rigid that one small patch fixes the whole function." S05 P1 shows 'points like 2 + 3i: complex numbers', and 'complex numbers' stays in the corner through P3. |
| 3 | S10 "first real progress there since 1940" overstates | **Applied** | Now "It beat a record that had stood since nineteen forty." New tag: 'beats Ingham's 1940 bound (near real part ¾)'. The fact entry notes the earlier improvements (Huxley 1972) above ¾. |
| 4 | "No formula tells you" | **Applied** | Now "No simple formula tells you". A fact entry is added (Willans 1964, Mills' constant). |
| 5 | S01 "like seven or thirteen" can attach to "factors" | **Applied** | Now "Primes, like seven or thirteen, can't be split into smaller factors." |
| 6 | Gauss's counting squeezed into his teens | **Applied**, merged with clarity C4 | Now "Over the years, he counted primes in blocks of a thousand." The bars get a DIM divider after 1M, 'Gauss's tables reached 3 million', and the 10M and 100M bars are tagged 'counted today'. The fact entry is updated. |
| 7 | "below Gauss's curve" needs li, not Li | **Applied** (storyboard) | S02 P4 and S10 P2: `topic.li_curve` must be mpmath `li`, not li − li(2) or li − 1.045. |
| 8 | "probably first near…" | **Applied** | Now "possibly first near…". The fact entry says the first crossing is not known. |
| 9 | "the first few zeros" | **Applied** | Now "a few zeros". The label is now 'Riemann: 25.31', and the dots are called the first and third zeros. |
| 10 | 2026 result is a preprint | **Applied, strengthened** | The 'preprint' tag stays, and the narration now says "still under review" (clarity M8). The fact entry says not refereed, Lean-formalized, Lamzouri reproof. |
| 11 | "typically about a thousand" | No change | The reviewer judged it acceptable (RMS = 1,000). |
| V1 | Schoenfeld band looks like a proven fence | **Applied** | Two DIM tags: 'if the Riemann Hypothesis is true' and 'Schoenfeld's exact version (÷ 8π)' (with clarity L9). |
| V2 | Block bars beyond Gauss's tables | **Applied** | See 6. |
| V3 | Euler product holds only for s > 1 | **Applied** | A DIM 's > 1' tag sits by the final equation. |
| V4 | 0.6 + 3i spiral must never look settled | **Applied** | The storyboard gives the centre (ζ(0.6+3i) ≈ 0.55 − 0.09i, recomputed), the radius growth, the distances and the framing rule. |
| V5 | Domain colouring must use real ζ values | **Applied** | Stated in S05 P3. |
| V6 | Dial never below ½ | **Applied** | Stated in S08 P4. |
| V7 | Fold correctness | No change needed | |
| V8 | Explicit-formula rebuild details | **Applied** | S07 P1: `topic.rebuild` must include the trivial-zero term. Zeros are summed in height order, with conjugate pairs as one wave. The midpoint overshoot at each jump stays. The caption 'fully proved by von Mangoldt, 1895' is added, with a fact entry. |
| V9 | Rogue-zero tags and twin | **Applied** | All rings are tagged 'hypothetical' (pacing M4). The twin appears at the same moment. S10's rogue ring now also gets its twin. |
| V10–V13 | Counter, Skewes graph, 'room for rebels', 'about 8 pages' | No change / kept | Explicit note added in S10: nothing suggests Guth and Maynard found or excluded specific zeros. |

## review_clarity.md

| # | item | decision | what changed / why |
|---|---|---|---|
| H1 | Dial never defined | **Applied**, merged with pacing H8 | Now "Let's rate the error on a dial by its share of x's digits. / Zero would mean the error never grows. / One would mean an error with as many digits as x. / One half, half the digits, is coin-flip size." Dropped for budget: the tail ": x to the power one half". S07 P5 makes that link itself ("x to the one half is the square root of x"). A DIM caption 'share of x's digits in the error' is added. |
| H2 | "primes sit in this window" | **Applied** (shorter) | Now "So far, we can only prove the dial reads between one half and one." S08 P4 now explains the lower end (the twins). |
| H3 | "confirmed it for … zeros" too early | **Applied** | Now "Computers have checked it more than twelve trillion times, and it has never failed." The counter label is 'checks, all passed'. |
| H4 | Sum becomes product: jumpy, "only the one" ambiguous | **Applied** (compressed) | Now "…in the end, only the first term survives. / Undo those multiplications, and the sum over all whole numbers becomes a formula built from primes alone." On screen, each factor flips across '='. |
| H5 | "ratio of the two goes to one" | **Applied** | Now "the percentage error shrinks toward nothing, while the actual gap keeps growing." The table column is 'off by' (as % of the curve): 5.4%, 0.16%, 0.013% (recomputed with mpmath). S08 now says "percentages", not "ratio". |
| H6 | "Zeros on the line do exist, so ½ is best" does not follow | **Applied** (slightly compressed) | Now "So the dial reads the rightmost zero, which, thanks to the twins, is never left of the middle. / One half is the best the primes can do, and exactly what Riemann guessed." A mirror pair re-shows at {#reads}. The old pulse is gone and the fact entry is rewritten. |
| H7 | "kept zeros off the strip's edge: enough for the ratio" | **Applied** (shorter) | Now "The eighteen ninety-six proof only showed no zero sits on the right edge: enough for percentages, not for the gap." The new {#enough} beat is a small echo of the S02 table. |
| M1 | No reason to care about zeros | **Rejected** (budget) | A draft version was tried and cut to fit 1,450. The motivation lands within the same scene ("Is that a coincidence? It isn't, and the reason is Riemann's real goal"), and S04 now opens "To see why one half, we need Riemann's tool." |
| M2 | "natural logarithm" of what? | **Applied** (without "has a name") | Now "That typical gap is the natural logarithm of the number. / It grows by about two point three with every extra digit." |
| M3 | Coin flips: why, and what does chance "miss"? | **Partly applied** | Now "Pure chance strays by about half the digits." The P2 "yardstick" rewrite (+7) is rejected for budget. The dial scene now defines "half the digits" out loud, and "stray" returns in S08 and S11. |
| M4 | Rigidity abstract, colours unexplained | **Applied**, merged with fact 2 | The colours are explained by an on-screen legend, 'colour = direction of ζ's output'. Speaking it would push the sentence past 24 words. |
| M5 | Four names for the critical line | **Applied** | "this middle line" (S06 P5) and "On the middle line" (S07 P5). "Fold" is only the action. |
| M6 | "zero … zero point eight" | **Applied** | Now "Slide one zero off the line, eight tenths of the way across." |
| M7 | Link "shares" to the dial | **Applied** (shorter) | Now "…wouldn't rule out a single rogue, and one would move the dial." A new {#moves} beat shows a BAD dial marker jump (illustration). |
| M8 | "proven share" of what; preprint presented as settled | **Applied** (shorter) | Now "For decades, the proven share of zeros on the line stayed around forty percent. / Then a new proof in twenty twenty-six, still under review, pushed it past two thirds." |
| M9 | Why the evens drop out | **Applied**, option A | The identity flashes on screen for about 1.5 s at {#evens}. |
| M10 | What to make of "about a hundred and thirty" | **Rejected** (budget) | At {#miss}, the storyboard already puts 129.5 beside a much taller '√x = 1,000' bar, and the dial beat names coin-flip size a few seconds later. |
| M11 | "To see why": why what? | **Applied** (shorter) | Now "To see why one half, we need Riemann's tool." |
| M12 | "grows" ambiguous | **Applied** | Now "…sets how big the wave's swings grow: roughly x to the power of that position." |
| L1 | "step back" | **Applied** | Now "zoom out". |
| L2 | "factors" is jargon | **Rejected** (budget) | Fact fix 5 removes the ambiguity, and '6 = 2 × 3' on screen shows what a factor is. |
| L3 | Seed "hum" early | **Rejected** (budget) | "The hum of those zeros" reads fine on first hearing, over S11's visual of waves rising from their zeros. |
| L4 | "proved it must cross" | **Applied** | Now "proved the staircase must cross above". |
| L5 | "it lands exactly on zero" | **Applied** | Now "the output lands exactly on zero". |
| L6 | "to the power s" | **Rejected** (budget) | The superscript ˢ is on screen, and pacing M9 splits the definition so it has air. |
| L7 | "a rule we'll take on trust" | **Rejected** | The storyboard shows the exact turning arrows. |
| L8 | Silent dial move in S06 P2 | **Applied** | The dial fades in at S06 P1 start (pacing M2). The alignment is one quick 1 s move, and its payoff is at the strip's floor in P6. |
| L9 | Band label vs spoken "times a logarithm" | **Applied** | See facts V1. |
| L10 | "Half the digits" vs digit counts | Kept | Zeros are underlined (not digits), with an explicit note. |
| L11 | Hilbert compression | **Applied** (adapted) | Now "David Hilbert put Riemann's guess on his list of problems." The suggested "put it" would point back to "What made Riemann so sure?". |
| L12 | Log axis | **Applied** | The 'log scale' tag is size 24 and stays on screen through S07 and S08. |
| C1 | Drop the pole clause | **Applied** | |
| C2 | Drop "Riemann set the proof aside" | **Applied** | S07 now opens "Riemann's real goal was an exact recipe for the prime staircase." This picks up S06's last line. S07 P1 and P2 are merged into one paragraph, and the 'sehr wahrscheinlich' card is dropped from S07. |
| C3 | Drop the 1940 sentence | **Rejected** in favour of fact fix 3 | The fact fix removes the vague "there" and keeps the year spoken. |
| C4 | Drop "In idle quarter hours" | **Applied**, merged with fact 6 | |
| C5 | Drop "just very slowly" | **Applied** | |
| C6 | "Back where we started" | **Softened** | Now "Let's go back to the start:" (−1). This keeps the warmth, and S11 is the shortest scene. |
| C7 | Drop "and he died at thirty-nine" | **Applied** | The 1826 to 1866 card stays. |

## review_pacing.md

| # | item | decision | what changed |
|---|---|---|---|
| H1 | S04 8.45 s freeze | **Applied** | New bookmarks {#bridge} and {#factor}. The tiles lay out at {#bridge} and the factor appears at {#factor}. |
| H2 | S02 {#add} to {#curve} only 0.3 s | **Applied** | {#add} moves to the sentence start. The lit tile hops every 0.6 s. |
| H3 | S02 7.45 s freeze | **Applied** | New {#right} (GOOD check) and {#fine} (table headers). |
| H4 | S02 opening freeze | **Applied** | New {#year}. An echo of the S01 curve holds at P_START. |
| H5 | S07 {#height} at 0.0 s | **Applied** | {#height} moves to "its wave wiggles", and the graph change runs at P_START. New {#power} for the label. |
| H6 | S06 end overloaded | **Applied** | The inset move and staircase preview are deleted. The verticals glow, then the scene fades. |
| H7 | Scene-end pauses above 0.9 are clamped | **Applied** | S02 P5, S03 P6 and S07 P5 are set to 0.9. The holds move into speech ({#pin}, {#digits}). |
| H8 | S03 dial build 0.8 s | **Applied**, merged with clarity H1 | About 3 s now pass before {#zero}. |
| M1 | Stacked fade-ins at scene starts | **Applied** | "All fade in together over 0.8 s" in S06, S07, S08 and S09. |
| M2 | S06 {#strip} overload | **Applied** | The dial fades in at S06 P1 start. |
| M3 | S06 rings with no bookmark | **Applied** | New {#pairs}. The zero flashes are timed to the spoken numbers. |
| M4 | 'imaginary' will be misread | **Applied** | The tag is now 'hypothetical' everywhere. |
| M5 | S01 count to back 1.5 s | **Applied** | {#count} moves earlier. The zoom takes 1.7 s. |
| M6 | S03 walks | **Applied** | {#walks} moves to the sentence start, and the walks draw over about 2.8 s. |
| M7 | S09 long card holds | **Applied** | New {#list} and {#notes}. |
| M8 | S10 5.8 s gap | **Applied** | New {#must}, with an ACCENT down-arrow. |
| M9 | 22-word formula sentence | **Applied** | Now "Pick a number, s. / Then add one, plus one over two to the s, …". |
| M10 | S11 finale rushes | **Partly applied** | S11 P2 and P3 pauses are 1.0. The final pause stays 1.5 because the validator ERRORs above 1.5, even though timeline.py allows 2.0 there (see below). |
| M11 | Long hook | No change | As the reviewer recommended (runtime floor). |
| L1 | pron case-sensitive; foreign names | **Applied** | Added `Zeta`, `Vallée`, `Helge`, `Jacques` (listen-check, see below). |
| L2 | Shake used for a hypothetical | **Applied** | Replaced by a BAD tint pulse. |
| L3 | Ring slide lags | **Applied** | The slide starts at P_START, and {#twin} marks the arrival. The '≈ 60×' label is **rejected**: 63 is the computed ratio, and "about sixty" is a fair spoken rounding. |
| L4 | "By twenty twenty-one" fast | Not changed | Added to the listen-check notes, with a +2-word fallback. |
| L5 | GOOD check without a bookmark | **Applied** | New {#every}. |
| L6 | "167 years" dates the video | Noted | See below. |
| L7 | S04 zeta to knows | No change | |

## Other edits (mine, from the spacing check)

- S04 P4: {#product} moves to the sentence start, so the rearrangement runs through the 5 s sentence instead of freezing.
- S05 P3: the side demo's three continuations fan out over about 3 s. This covers the 5.5 s before {#patch}.
- S08 P1: the rogue slide is slowed to about 2.5 s, timed to "eight tenths of the way across".
- S10 P3: the rogue ring appears with its twin.
- S10 P3: two labels at size 22 are raised to 24 (STYLE.md minimum).

## Changes that must be made outside the script

1. **Validator vs engine on the final pause.** `tools/timeline.py` allows 2.0 s on the video's final paragraph (`FINAL_TAIL_MAX = 2.0`). `tools/validate_script.py` ERRORs on any `pause_after` above 1.5. Let the validator accept up to 2.0 on the last paragraph of the last scene. Then set S11 P4 `pause_after` to 2.0 (pacing M10).
2. **Listen-check pron entries** (already in `"pron"`): `Jacques` /ʒˈɑk/, `Vallée` /vɑlˈeɪ/, `Helge` /hˈɛlɡə/, `Zeta` /zˈeɪtə/. Also listen to "x's digits" (S03 P5) and "By twenty twenty-one" (S09 P4). Whisper is prompted with the script, so its match proves little. Fallbacks are in `pronunciation_notes`.
3. **topic.py requirements** stated in the storyboards:
   - `li_curve` = `mpmath.li`.
   - `rebuild` includes the trivial-zero term −1/ln x + arctan(π/ln x)/π, sums the zeros in height order with conjugate pairs as one wave, and keeps the midpoint overshoot at each jump.
   - The 0.6 + 3i spiral uses exact partial sums up to 2,000 terms.
4. **Measure the runtime** with `timeline.py`. The expected result is about 9:36. If it comes in under 9:30, raise mid-scene `pause_after` values after reveals (for example S01 P4, S06 P5, S07 P3) before adding words.
5. **Release checklist:** "A hundred and sixty-seven years later" (S11) is right only for a 2026 release.
