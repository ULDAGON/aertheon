# Lay-viewer comprehension review: script_synth.json

Reviewer role: a curious non-expert, listening once at normal speed, no pausing.
Current spoken total: **1,445 words** (budget cap 1,450). Every addition below has a word delta. The HIGH package comes with a matching cut list at the end, so it stays inside the budget.

Overall: the spine is strong and teachable. It runs gap, coin flips, dial, zeros, waves, the one-half argument, and it makes one real promise ("half the digits"). The risk is concentrated in four hinges where a lay listener loses the thread: (1) what the dial actually measures, (2) Euler's sum-to-product step, (3) "ratio" and "the edge" talk, and (4) the S08 conclusion "one half is the best possible", which currently rests on a sentence that does not follow.

---

## HIGH (the thread breaks for a lay listener)

### H1. S03 P5: the dial is never defined in words a listener can hold
"Let's put **this** on a dial." "This" has no clear referent (the gap? the coin walk? the square root?). The listener also never hears that the dial reading is the *power* of x. S07 ("x to the power of that position") and S08 ("x to the zero point eight", the dial marker at 0.8) depend entirely on that link.
- Rewrite, first sentence: "Let's rate the error on {#dial} a dial, by its share of the digits of x." (keep "{#zero} Zero would mean the error never grows; {#all} one, an error with as many digits as x.")
- Rewrite, second sentence: "{#coin_mark} One half, half the digits, is coin-flip size: x to the power one half."
- Delta: **+15** (6 to 15 words; 8 to 14 words).
- Storyboard: add a DIM caption under the ruler, 'share of x's digits in the error' (T, 22), at {#dial}.

### H2. S03 P6: "the primes sit somewhere in this window" is a mixed metaphor, and the lower end is never explained
A listener cannot picture primes sitting on a dial. They will also wonder why the window starts at one half and not at zero, because nothing says the lower end is proven too. It is proven (Littlewood: the error exceeds about the square root of x divided by ln x infinitely often).
- Rewrite: "So far, we can only prove {#window} the dial reads somewhere in this window: at least one half, at most one."
- Delta: **+7**. S08 P4 then pays off the "at least one half".

### H3. S01 P6: "Computers have confirmed **it** for more than twelve trillion special points, called zeros"
At this point "it" (the hypothesis) has not been stated. "Confirmed it for points" is also meaningless to a newcomer, and "zeros" is a forward reference the ear cannot use. This comes in the first minute, where lost attention costs the most.
- Rewrite: "Computers have checked it {#checked} more than twelve trillion times, and it has never failed."
- Delta: **+1**. Storyboard: change the counter's label to 'checks, all passed' and drop 'zeros checked · we'll meet them soon'. The word "zeros" then arrives cleanly in S06.

### H4. S04 P4: "the sum over all whole numbers equals a product over the primes alone"
"Product over the primes" is textbook phrasing. The logic also jumps. The screen shows "(factors) × sum = 1" and the narration then says "sum = product" with no step between. The phrase "only the one survives" is ambiguous too (the number one? one term?).
- Rewrite, sentence 1: "It's {#sieve} a sieve for primes inside the sum: in the end, {#lone} only the very first term, the one, survives." (**+3**)
- Rewrite, sentence 2: "Undo all those multiplications, and the sum over every whole number {#product} turns into a formula built from the primes alone." (**+6**)
- Delta: **+9**. (If budget is tight, take only sentence 2: +6.)

### H5. S02 P5: "the ratio of the two goes to one"
"Ratio goes to one" is maths-speak, and "the two" is a vague referent. The whole of S03 is built on this distinction (close in percentage, growing in plain numbers), so it has to land.
- Rewrite: "But read the fine print: {#ratio} the percentage error shrinks toward nothing, {#gap} while the actual gap keeps growing."
- Delta: **-2**. Storyboard: rename the table header 'staircase ÷ curve' to 'off by (%)' and show 5.4%, 0.16%, 0.013% (the same data as a percentage). Or keep the ratio column and add the DIM caption 'closer and closer in %'.

### H6. S08 P4: "Zeros on the line do exist, so one half is the best possible" does not follow for a listener
The real reason is the twins: every zero, or its mirror twin, sits at one half or further right, so the dial can never read below one half. The current line swaps in an unexplained premise ("zeros on the line exist") and skips the twin logic the scene just built. "The dial reads the rightmost zero" is also a new use of "reads" that needs its payoff in the same breath.
- Rewrite of P4:
  - "Only on the middle line {#equal} are the twins equally loud."
  - "So the dial {#reads} reads the rightmost zero, and thanks to the twins, that is never left of the middle."
  - "{#best} One half is the best the primes can do, and {#guessed} it is exactly what Riemann guessed."
- Delta: **+8** (37 to 45). This also echoes the scene title. Storyboard: at {#reads}, briefly re-show a mirror pair so "thanks to the twins" has a picture; drop the "Zeros on the line do exist" pulse.

### H7. S08 P5: "only kept zeros off the strip's edge: enough for the ratio"
"Kept zeros off" is unclear (which edge? why does it matter?), and "enough for the ratio" is a callback to jargon.
- Rewrite: "The eighteen ninety-six proof only showed {#edge} no zero sits on the strip's right edge: enough for Gauss's percentages, not for the gap."
- Delta: **+7**. This pairs with H5.

**HIGH package total: +45** (with H4 in full). Fund it with the cut list at the end (-38, or -43 with C7). Net: **1,447 to 1,452**. Take C7, or H4 sentence 2 only, to land at 1,447 or below.

---

## MEDIUM (a listener stumbles but recovers; fix if the budget allows)

### M1. S06 P1: no reason given to care about zeros
"Now, where does the extended zeta equal zero?" To a newcomer, zeros look like a random thing to ask about. The motivation only arrives in S07.
- Rewrite: "Riemann found that one thing about zeta matters most for the primes: where it equals zero." Then "Some zeros are easy: …"
- Delta: **+9**.

### M2. S02 P3: "That typical gap is the natural logarithm". Of what? And what is that?
- Rewrite: "That typical gap has a name: {#log} the natural logarithm of the number. It grows by about two point three {#digit} with every extra digit."
- Delta: **+5**.

### M3. S03 P2/P3: why do coin flips matter here, and what does chance "miss"?
"For scale, let's flip a coin" gives no reason why coin flips relate to primes. "Pure chance **misses** by about half the digits": misses what?
- P2 rewrite: "For a yardstick, imagine the primes were sprinkled purely at random, like coin flips." (**+7**)
- P3 rewrite: "Pure chance strays by a number with about half the digits." (**+4**)
- Delta: **+11** (the P3 fix alone, +4, is the priority).

### M4. S05 P3: "being smooth is a far stricter demand" is abstract, and the colours are never explained
The domain colouring bursts onto the screen at {#patch}, and nothing in the narration says what the colours mean. That is a visual the viewer cannot read, in the most abstract scene, which is where attention is most likely to drop. "Such a function" is also a weak referent.
- Rewrite of P3:
  - "On a line, {#strict} a curve can be continued smoothly in many ways."
  - "On a plane, smooth functions are so rigid that {#patch} one small patch, coloured here by the direction of zeta's output, {#locked} fixes them everywhere."
- Delta: **+5**.

### M5. The critical line has four names
"The middle of the strip" (S06 P3), "the fold" (S06 P4, P5), "the line" (S07, S08, S09), "the middle line" (S08), "one straight line" (S11). Heard once, "sits exactly on the fold" sounds like a new object.
- Fix: keep "fold" only as the action. S06 P5: "…sits exactly on **this middle line**, at one half." (+2). S07 P6: "On **the middle** line…" (+1). Everything after that uses "the line".
- Delta: **+3**.

### M6. Aural collision between "zero" the number and "zero" of zeta (S08 P1)
"Slide one zero off the line, to zero point eight." On one hearing, "zero … zero point eight" tangles. The same happens more mildly in "lands exactly on zero" and "the strip between zero and one".
- Rewrite: "Slide one zero off the line, {#rogue} eight tenths of the way across." Keep the screen label '0.8'. Keep "x to the zero point eight" in the next sentence, where it is unambiguous.
- Delta: **+2**.

### M7. S10 P3: link "shares" to the dial, or viewers conflate 67% with the dial
Straight after S09's "past two thirds", a listener may think the dial is about two thirds of the way done. The script never says why the share does not move the dial.
- Rewrite, sentence 1: "Even proving that almost all zeros are on the line {#almost} wouldn't rule out a single rogue, and one rogue is enough to move the dial."
- Delta: **+9**. (22 words, still under 24.)

### M8. S09 P5: "the proven share on the line": a share of what?
A share of infinitely many is a strange idea when heard once. The new result is also a six-week-old preprint, and the narration presents it as settled.
- Rewrite:
  - "For decades, the best proof showed {#forty} at least forty percent of all zeros sit on the line."
  - "Then {#thirds} a brand-new proof in twenty twenty-six, still under review, pushed it past two thirds."
- Delta: **+8**.

### M9. S04 P3: "every even term drops out" is magic without the one-line reason
The sieve visual carries this beat, but a curious viewer will ask *why* multiplying removes the even terms.
- Option A, no words: at {#evens}, flash '1/2ˢ × (1 + 1/2ˢ + 1/3ˢ + …) = 1/2ˢ + 1/4ˢ + 1/6ˢ + …' above the tiles for about 1.5 s before they fade.
- Option B, spoken: add "Because one over two to the s, times the sum, is exactly the even terms." (**+14**)
- Recommend A.

### M10. S03 P4: the listener is told "off by about a hundred and thirty" and is not told what to make of it
Right after hearing "coin flips give a thousand", 130 sounds like a contradiction, or like good news.
- Rewrite: "Up to a million, {#miss} Gauss's curve is off by about a hundred and thirty, well inside coin-flip size."
- Delta: **+4**.

### M11. S04 P1: "To see **why**, we need Riemann's tool": why what?
It follows S03's "right at one half, as unruly as coin flips", so the "why" is unanchored.
- Rewrite: "To see where that guess comes from, we need Riemann's tool."
- Delta: **+4**.

### M12. S07 P5: "sets how fast the wave **grows**"
"Grows" is ambiguous. Does the wave get taller, or wiggle faster? The previous sentence just used "how fast … wiggles".
- Rewrite: "{#across} Its position across the strip sets how big the wave's swings get: about x to the power of that position."
- Delta: **+1**.

---

## LOW (polish)

- **L1. S01 P4: "and step back."** Right after "one step up per prime", "step back" reads as another step of the staircase. Use "and zoom out". **0**.
- **L2. S01 P1: "split into smaller factors."** "Factors" is school jargon. Use "A prime, like seven or thirteen, can't be made by multiplying smaller whole numbers." **+4**. Move {#split} to "multiplying".
- **L3. S07 P3: seed "hum" early.** S11's "the hum of those zeros" is the payoff metaphor, but "hum" and "music" never appear before it. Change to "Then, for every zero, {#wave} add one wave, like one note in a chord." **+6**.
- **L4. S10 P2: "Littlewood proved **it** must cross above."** "It" could be the curve. Use "proved the staircase must eventually cross above it". **+3**.
- **L5. S06 P3: "it lands exactly on zero."** Use "the output lands exactly on zero". **+1**.
- **L6. S04 P1: "one over two to the s."** At the first occurrence only, say "one over two to the power s". **+2**.
- **L7. S05 P2: "Moving up makes each term spin"** is asserted, not shown. One honest clause helps: "…each term spin, a rule we'll take on trust". **+6**. Optional.
- **L8. S06 P2 storyboard.** The dial silently fades in, and the strip visibly re-stretches to align with it, while the narration talks about something else. This is a long, unexplained visual move that is only justified in P6. Make the alignment a quick, unshowy snap, or delay it to P6 {#floor}. Storyboard only.
- **L9. S03 P4 storyboard.** Narration says "square root of x, times a logarithm" (about 13,800 at a million), but the band shows Schoenfeld's √x·ln x/(8π) = 549.7. A pausing viewer sees a mismatch. Label the band 'Schoenfeld's exact version (÷ 8π)'. Storyboard only.
- **L10. "Half the digits" vs. real digit counts.** 1,000,000 has 7 digits and 1,000 has 4. A pausing viewer may count. The S03 P3 underline correctly says "half as many zeros". Keep "about half the digits" in speech where possible, and underline zeros (as specified), not digits.
- **L11. S09 roll call.** Six names and dates in about 40 s (Hilbert, Hardy, Siegel, Platt and Trudgian, Conrey, Alpöge and Furman). This is the attention dip. If words are needed, compress Hilbert: "In nineteen hundred, David Hilbert put it on his famous list of problems." **-4**.
- **L12. S07 P5 log axis.** The narration never says the horizontal axis is logarithmic, and a lay viewer will read the evenly spaced wiggles literally. The DIM 'log scale' tag is enough if it is at least size 24 and stays on screen. Storyboard only.

---

## Cut list to fund the HIGH package (each also helps clarity or loses nothing a listener needs)

| id | where | cut | delta |
|---|---|---|---|
| C1 | S07 P2 | Drop ", {#pole} which comes from the one point where zeta blows up". A curve that "comes from a point" is an unsupported leap for a lay viewer. Keep the thread visual as silent decoration, or drop it. | **-10** |
| C2 | S07 P1 | Drop "Riemann set the proof of his guess aside." Start P1 with "Riemann was after something bigger: {#recipe} an exact recipe for the prime staircase." | **-8** |
| C3 | S10 P4 | Drop "It was the first real progress there since nineteen forty." (vague "there"). The on-screen tag 'best since Ingham, 1940' keeps the fact. | **-10** |
| C4 | S02 P1 | "In idle quarter hours," becomes "He counted primes in blocks of a thousand." | **-4** |
| C5 | S04 P2 | Drop ", just very slowly". The bar crawling past the frame says it. | **-3** |
| C6 | S11 P1 | "Let's go back to where we started:" becomes "Back where we started:" | **-3** |
| C7 | S09 P1 | Drop ", and he died at thirty-nine" (optional; the 1826 to 1866 card stays). | **-5** |

C1 to C6: **-38**. With C7: **-43**.

**Ledger:** 1,445 + 45 (HIGH) - 43 (C1 to C7) = **1,447**. To adopt MEDIUM items as well, prioritise M1 (+9), M3 P3 fix (+4), M5 (+3), M6 (+2), M7 (+9) and M9 option A (0), and fund them by taking L11 (-4) plus trimming the lowest-value MEDIUMs. A realistic final is about 1,450 with HIGH + M1 + M5 + M6 + M9A, and C1 to C7 + L11 (1,447 + 14 - 4 = 1,457, so also drop H4 sentence 1 (-3) and one of M1/M7 to stay at or below 1,450). Re-run the validator after edits.
