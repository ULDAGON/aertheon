"""Build script.json from script_synth.json by applying the review fixes. Every edit asserts it hit its target."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # the video's script/ folder
src = json.loads((ROOT / "script_synth.json").read_text())
d = copy.deepcopy(src)
S = {sc["id"]: sc for sc in d["scenes"]}


def P(sid, i):
    return S[sid]["paragraphs"][i]


def rep(obj, key, old, new):
    assert old in obj[key], f"not found in {key}: {old[:70]!r}"
    obj[key] = obj[key].replace(old, new)


def sents(sid, i, new):
    P(sid, i)["sentences"] = new


# ---------------- S01 ----------------
sents("S01_Hook", 0, ["Here are {#grid} the numbers from one to a hundred, with {#primes} the primes lit up.",
                      "Primes, like seven or thirteen, can't be split {#split} into smaller factors."])
sents("S01_Hook", 2, ["No simple formula tells you; you check.",
                      "{#even} Ninety-eight and a hundred are even, {#nines} ninety-nine is nine times eleven, and {#found} a hundred and one is prime."])
rep(P("S01_Hook", 2), "visual", "On 'No formula tells you'", "On 'No simple formula tells you'")
sents("S01_Hook", 3, ["Up close, {#noise} the primes look like noise.",
                      "But {#count} count them, one step up per prime, and {#back} zoom out.",
                      "The staircase {#blur} blurs, and {#curve} a smooth curve follows it with astonishing precision."])
rep(P("S01_Hook", 3), "visual", "from 100 to 100,000 over about 2 s, landing by {#blur}",
    "from 100 to 100,000 over about 1.7 s, landing by {#blur}")
sents("S01_Hook", 5, ["Today it's worth {#prize} a million dollars.",
                      "Computers have checked it {#checked} more than twelve trillion times, and it has never failed.",
                      "{#never} Nobody has proved it."])
rep(P("S01_Hook", 5), "visual", "a DIM label under it: 'zeros checked · we'll meet them soon' (T, 24)",
    "a DIM label under it: 'checks, all passed' (T, 24) (the word 'zeros' is kept for S06, where it arrives cleanly)")
rep(S["S01_Hook"], "purpose", "more than twelve trillion zeros checked", "checked more than twelve trillion times")

# ---------------- S02 ----------------
sents("S02_Gauss", 0, ["That smooth curve goes back to {#gauss} a teenager, Carl Friedrich Gauss, {#year} around seventeen ninety-two.",
                       "Over the years, {#blocks} he counted primes in blocks of a thousand."])
P("S02_Gauss", 0)["visual"] = (
    "Empty BG. At the paragraph start: a small echo of the S01 end state (teal curve over the blue staircase, about "
    "3 by 1.5 manim) sits at the top right, so the scene never opens on an empty frame while 'That smooth curve' is "
    "spoken; it fades out at {#gauss}. At {#gauss}: a caption card at the top left: 'Carl Friedrich Gauss' (T, 30, INK). "
    "At {#year}: the card's second line 'about 1792 · age 15 or 16' (T, 24, DIM) writes in. At {#blocks}: seven tall "
    "bars grow across the middle of the frame, one per block of a thousand numbers, for the blocks starting at 1, "
    "1,000, 10,000, 100,000, 1,000,000, 10,000,000 and 100,000,000 (labels under them in N 24: '1', '1k', '10k', "
    "'100k', '1M', '10M', '100M'). Bar heights are the true prime counts in each block: 168, 135, 106, 81, 75, 61, 54 "
    "(topic.block_counts), PALETTE blue fill, each count in small N INK on top. Honesty about what Gauss himself "
    "counted: a thin DIM dashed vertical divider stands between the 1M and 10M bars with the DIM label 'Gauss's tables "
    "reached 3 million' (T, 24) above it, and the 10M and 100M bars carry a small DIM tag 'counted today' (T, 24). "
    "Pause: hold.")
sents("S02_Gauss", 2, ["That typical gap is {#log} the natural logarithm of the number.",
                       "It grows by about two point three {#digit} with every extra digit."])
sents("S02_Gauss", 3, ["{#chance} Near any number, the chance of a prime is about one in its logarithm.",
                       "{#add} Add those chances up, and {#curve} out comes Gauss's smooth curve."])
rep(P("S02_Gauss", 3), "visual", "one of them lights blue; the label",
    "one of them lights blue, and the lit tile keeps hopping to a new random tile about every 0.6 s until {#add} "
    "(one lit in fourteen, so the beat never freezes); the label")
rep(P("S02_Gauss", 3), "visual", "(at this scale li and Li are identical)",
    "(topic.li_curve is li(x) = mpmath.li, not li(x) − li(2); at this scale the two are identical)")
sents("S02_Gauss", 4, ["In {#proof} eighteen ninety-six, Jacques Hadamard and Charles de la Vallée Poussin {#right} proved Gauss right.",
                       "But {#fine} read the fine print: {#ratio} the percentage error shrinks toward nothing, {#gap} while the actual gap keeps growing."])
P("S02_Gauss", 4)["visual"] = (
    "At {#proof}: caption at the top right: '1896 · Hadamard · de la Vallée Poussin' (T, 26, INK) with 'prime number "
    "theorem' (T, 24, DIM) below. At {#right}: a small GOOD check appears beside the teal label 'Gauss's curve'. At "
    "{#fine}: the graph shrinks to the left third and a table's headers appear at the right: 'up to', 'off by', "
    "'curve − staircase' (T, 24, DIM), with a tiny DIM note under 'off by': 'as % of the curve'. At {#ratio}: the rows "
    "fill in turn: '1,000 | 5.4% | 9.6', '1,000,000 | 0.16% | 129.5', '100,000,000 | 0.013% | 754.4' (N, 28, INK; exact: "
    "li(x) against the prime count); the percentage column tints GOOD as it shrinks toward nothing. At {#gap}: the right "
    "column pulses ACCENT, its numbers visibly growing. Pause (scene end, 0.9 s): hold on the growing gap while "
    "everything fades out.")
P("S02_Gauss", 4)["pause_after"] = 0.9
rep(S["S02_Gauss"], "purpose", "Gauss (about 1792, aged 15 or 16) counted primes in blocks of a thousand",
    "Gauss (starting about 1792, aged 15 or 16, and over many years) counted primes in blocks of a thousand")
rep(S["S02_Gauss"], "purpose", "proved it right only as a ratio, while the gap keeps growing",
    "proved it right only in percentage terms, while the actual gap keeps growing")

# ---------------- S03 ----------------
sents("S03_CoinFlips", 1, ["For scale, {#coin} let's flip a coin. Heads, {#up} step up; tails, {#down} step down.",
                           "{#walks} After a million flips, you typically end up {#thousand} about a thousand steps from the start."])
rep(P("S03_CoinFlips", 1), "visual", "draw together from the origin to 1,000,000 flips;",
    "draw together from the origin to 1,000,000 flips over about 2.8 s (they run from {#walks} to {#thousand});")
sents("S03_CoinFlips", 2, ["A million, a thousand: {#root} that's the square root, {#half} with half as many zeros.",
                           "Pure chance strays {#digits} by about half the digits."])
rep(P("S03_CoinFlips", 2), "visual", "each get a small ACCENT underline, three against six.",
    "each get a small ACCENT underline, three against six (underline zeros, not digits: 1,000,000 has seven digits).")
rep(P("S03_CoinFlips", 3), "visual",
    "and the staircase sits visibly inside it. Pause",
    "and the staircase sits visibly inside it. The band carries two DIM tags (T, 24) so a pausing viewer never reads it "
    "as a proven fence or as a mismatch with the spoken 'square root of x, times a logarithm': 'if the Riemann "
    "Hypothesis is true' and 'Schoenfeld's exact version (÷ 8π)'. Pause")
sents("S03_CoinFlips", 4, ["Let's rate the error on {#dial} a dial by its share of x's digits.",
                           "{#zero} Zero would mean the error never grows.",
                           "{#all} One would mean an error with as many digits as x.",
                           "{#coin_mark} One half, half the digits, is coin-flip size."])
rep(P("S03_CoinFlips", 4), "visual", "and a DIM caption 'error dial' (T, 24) at its left end.",
    "a DIM caption 'error dial' (T, 24) at its left end, and a DIM caption 'share of x's digits in the error' (T, 24) "
    "at its right end (x = 2.9 onward). The ruler, ticks, labels and captions build together over about 1.5 s, before "
    "{#zero}.")
sents("S03_CoinFlips", 5, ["So far, we can only prove {#window} the dial reads between one half and one.",
                           "Riemann's guess: {#pin} right at one half, as unruly as coin flips, and no more."])
P("S03_CoinFlips", 5)["visual"] = (
    "At {#window}: a translucent ACCENT window (opacity 0.25, ACCENT rim) grows over the ruler from ½ to 1, with a "
    "small DIM label 'proven range' above it. At {#pin}: a small ACCENT pin labelled 'Riemann?' (T, 24) drops onto ½ "
    "beside the coin and glows once while the rest of the sentence plays (the hold lives inside the speech; the window "
    "itself stays wide: it narrows only in the hypothetical beat of S11, and even then only as a dashed 'if'). Pause "
    "(scene end, 0.9 s): all content above the dial fades; the dial fades last.")
P("S03_CoinFlips", 5)["pause_after"] = 0.9

# ---------------- S04 ----------------
sents("S04_Zeta", 0, ["To see why one half, we need Riemann's tool.",
                      "{#pick} Pick a number, s.",
                      "Then add {#terms} one, plus one over two to the s, plus one over three to the s, forever."])
rep(P("S04_Zeta", 0), "visual", "writes in term by term, timed to the words.",
    "writes in term by term, timed to the words of each 'one over …'.")
sents("S04_Zeta", 1, ["With s equal to two, {#two} the sum settles on pi squared over six.",
                      "With s equal to one, {#one} it grows forever."])
sents("S04_Zeta", 2, ["In {#euler} seventeen thirty-seven, Euler found {#bridge} a bridge to the primes.",
                      "Multiply the sum by {#factor} one minus one over two to the s, and {#evens} every even term drops out.",
                      "Then three, {#threes} and its multiples drop out too."])
P("S04_Zeta", 2)["visual"] = (
    "At {#euler}: caption 'Euler · 1737' (T, 24, DIM) at the top left. At {#bridge}: the general row becomes tiles "
    "'1', '1/2ˢ', '1/3ˢ', … up to '1/30ˢ', in three rows of ten, centered (N, 28). At {#factor}: to the left of the "
    "tiles a factor '(1 − 1/2ˢ)' (N, 28, PALETTE blue) appears. At {#evens}: for about 1.5 s the one-line reason "
    "flashes above the tiles: '1/2ˢ × (1 + 1/2ˢ + 1/3ˢ + …) = 1/2ˢ + 1/4ˢ + 1/6ˢ + …' (N, 26, DIM), then every tile "
    "with an even denominator (2, 4, 6, …, 30) flashes blue and fades to FAINT and the reason line fades. At {#threes}: "
    "a second factor '(1 − 1/3ˢ)' (PALETTE yellow) joins; the surviving multiples of 3 (3, 9, 15, 21, 27) flash yellow "
    "and fade. Exact: multiplying by (1 − 1/pˢ) removes exactly the remaining terms whose n is a multiple of p. Pause: "
    "survivors 1, 5, 7, 11, 13, 17, 19, 23, 25, 29 wait.")
sents("S04_Zeta", 3, ["It's {#sieve} a sieve for primes inside the sum: in the end, {#lone} only the first term survives.",
                      "{#product} Undo those multiplications, and the sum over all whole numbers becomes a formula built from primes alone."])
rep(P("S04_Zeta", 3), "visual", "At {#product}: the display rearranges into",
    "At {#product}: each factor visibly moves across the '=' and flips into its reciprocal (undoing the "
    "multiplication), so the display rearranges into")
rep(P("S04_Zeta", 3), "visual", "the right side 'only primes' (T, 24, DIM). Pause: hold.",
    "the right side 'only primes' (T, 24, DIM), and a small DIM tag 's > 1' (N, 24) beside the equation (the identity "
    "holds only there; at s = 1 both sides are infinite). Pause: hold.")
rep(S["S04_Zeta"], "purpose", "until only 1 is left, turns the sum over all whole numbers into a product over the primes alone",
    "until only the first term, 1, is left; undoing the multiplications turns the sum over all whole numbers into a "
    "product built from the primes alone (for s > 1)")

# ---------------- S05 ----------------
rep(P("S05_Plane", 0), "visual", "a small N label '2 + 3i' by the dot and a DIM note 'i marks the up-part' under it.",
    "a small N label '2 + 3i' by the dot, a DIM note 'points like 2 + 3i: complex numbers' (T, 24) under it and "
    "'i marks the up-part' (T, 24, DIM) under that. The words 'complex numbers' then stay as a small DIM tag in the "
    "input panel's top-left corner through P3, so 'complex' is on screen before it is spoken in P3.")
rep(P("S05_Plane", 1), "visual",
    "the spiral redraws with 2,000 terms and keeps looping outward without settling (exact partial sums);",
    "the spiral redraws with 2,000 terms and keeps looping outward without settling (exact partial sums; they "
    "behave like ζ(s) + N^(1−s)/(1−s): a spiral of slowly growing radius, about N^0.4/3, centred on the extended value "
    "ζ(0.6 + 3i) ≈ 0.55 − 0.09i, which is not marked here; distance from it 0.85 at 10 terms, 2.09 at 100, 5.24 at "
    "1,000, 6.91 at 2,000, only about 3.6 turns in all; frame the output panel so the growth is visible and the path "
    "never looks as if it settles);")
sents("S05_Plane", 2, ["On a line, {#strict} a curve can be continued smoothly in many ways.",
                       "But with complex inputs, smoothness is {#patch} so rigid that one small patch {#locked} fixes the whole function."])
P("S05_Plane", 2)["visual"] = (
    "The output panel fades; the input plane returns to full width. At {#strict}: a small side demo at the top left: a "
    "short curve on a line with three different dashed smooth continuations fanning out, and the DIM caption 'on a "
    "line: many ways' (T, 24); the three continuations fan out one after another over about 3 s, so the demo keeps "
    "moving until {#patch}. At {#patch}: on the plane, a small square patch (about 1 by 1 unit, around 3 + 1i) fills "
    "with domain colouring of ζ (hue = angle of the output, steady brightness; topic.domain_color, computed with "
    "mpmath), and a small colour-wheel legend appears beside it: 'colour = direction of ζ's output' (T, 24, DIM). At "
    "{#locked}: the colouring spreads outward from the patch like ink until it covers the whole region right of 1 "
    "(real mpmath ζ values everywhere the colour spreads; the 'ink' is a metaphor for uniqueness, nothing is made up); "
    "the side demo's caption is replaced by 'complex inputs: only one way' (T, 24, DIM), and the side demo fades. "
    "Pause: hold.")
rep(S["S05_Plane"], "purpose", "because complex smoothness is so rigid",
    "because smoothness for complex inputs is so rigid (on a line it is not)")

# ---------------- S06 ----------------
sents("S06_Zeros", 0, ["Now, where does the extended zeta equal zero?",
                       "Some are easy: {#trivial} minus two, minus four, minus six, and on forever."])
rep(P("S06_Zeros", 0), "visual", "Empty BG. The plane from S05 fades in without colouring:",
    "Empty BG. At the paragraph start, all of these fade in together over 0.8 s: the error dial at its home in its S03 "
    "state (ruler, coin and pin 'Riemann?' at ½, ACCENT window ½ to 1), and the plane from S05 without colouring:")
rep(P("S06_Zeros", 0), "visual", "On the question: a small DIM caption", "On the first sentence: a small DIM caption")
rep(P("S06_Zeros", 1), "visual",
    "The error dial fades in at its home with its S03 state (ruler, coin and pin 'Riemann?' at ½, ACCENT window ½ to 1). Then the plane content group transforms (not the camera)",
    "In the same single quick move (about 1 s, no extra flourish; the payoff of the alignment comes only in P6, at "
    "the strip's floor), the plane content group transforms (not the camera)")
sents("S06_Zeros", 2, ["Walk {#walk} up the middle of the strip, and {#watch} watch where zeta sends you.",
                       "At height fourteen point one three, {#first} the output lands exactly on zero."])
sents("S06_Zeros", 3, ["{#more} Again at twenty-one, twenty-five, thirty, and on.",
                       "And zeros come in {#pairs} mirror pairs: {#fold} fold the strip down the middle, and they pair up or sit on the fold."])
P("S06_Zeros", 3)["visual"] = (
    "At {#more}: the climb continues; each time the output path passes through the origin (heights 21.022, 25.011, "
    "30.425), the origin flashes and a zero dot lands on the middle line with a small N height label, each flash timed "
    "to its spoken number 'twenty-one', 'twenty-five', 'thirty'; then, on 'and on', quickly 32.935, 37.586, 40.919, "
    "43.327, 48.005, 49.774 (exact, mpmath.zetazero); ten dots in all. The output panel fades. At {#pairs}: two hollow "
    "BAD dashed rings, tagged 'hypothetical' (T, 24, DIM; not 'imaginary', which a viewer would read as the up-part), "
    "appear at 0.8 + 35i and 0.2 + 35i (illustration only; no such zero is known). At {#fold}: the strip's left half "
    "folds over onto its right half about the middle line (a 1 s flip about the vertical axis at real part ½): the two "
    "rings land on each other, and the ten real zeros stay put on the fold; then the fold opens back. Pause: hold.")
sents("S06_Zeros", 4, ["The Riemann Hypothesis says {#claim} every zero in the strip sits exactly on this middle line, at one half."])
P("S06_Zeros", 6)["visual"] = (
    "On 'It isn't': the '?' dissolves. At {#goal}: the three dashed verticals glow once and the strip with its zeros "
    "dims to 60%. No inset move and no staircase preview here (S07 builds both). Pause (scene end): everything fades "
    "out to the empty background, the dial last.")
rep(S["S06_Zeros"], "purpose", "RH says every zero in the strip sits on the fold at one half",
    "RH says every zero in the strip sits on this middle line, at one half")

# ---------------- S07 ----------------
p0, p1 = P("S07_Waves", 0), P("S07_Waves", 1)
merged = {
    "sentences": ["Riemann's real goal was {#recipe} an exact recipe for the prime staircase.",
                  "It starts with {#smooth} a sharpened version of Gauss's curve."],
    "visual": (
        "Empty BG. On the opening words, all of these fade in together over 0.8 s: the error dial at its home (S03 "
        "state) and the strip as the INSET on the right (real part 0 to 1 over x = 4.2 to 6.4, height 0 to 50 over "
        "y = -2.4 to 3.2, ACCENT line at ½ with the first ten zeros, tiny labels '0 ½ 1' under it). At {#recipe}: left "
        "two thirds: axes for x from 0 to 100 (x = -6.6 to 3.4) and y from 0 to 26 (y = -2.4 to 3.2); the blue prime "
        "staircase up to 100 draws (topic.staircase), and a DIM caption at the top: 'Riemann 1859: staircase = smooth "
        "curve + one wave per zero' (T, 24) with a smaller DIM line under it: 'fully proved by von Mangoldt, 1895' "
        "(T, 24). Formula used, Riemann's prime-counting form (research_facts §8.1 B): π(x) = R(x) − Σ R(x^ρ) − 1/ln x "
        "+ (1/π)·arctan(π/ln x), computed in topic.R_curve, topic.zero_wave(k, xs) and topic.rebuild(n, xs). "
        "topic.rebuild MUST include the trivial-zero term −1/ln x + arctan(π/ln x)/π (−0.68 at x = 2.5, −0.14 at 10, "
        "−0.03 at 100), mirroring script/checks/staircase_rebuild_check.py, or the 'exactly' claim visibly fails near "
        "x = 2 to 10; sum the zeros in order of height, each conjugate pair as one real wave (the series converges only "
        "conditionally); at each jump the rebuilt curve passes through the midpoint, and the small overshoots are "
        "correct behaviour, never 'fix' them. At {#smooth}: the PALETTE teal curve R(x) draws over the staircase "
        "(R(100) = 25.66), labelled 'sharpened curve' (T, 24, teal). Pause: hold."),
    "pause_after": 0.8,
}
S["S07_Waves"]["paragraphs"] = [merged] + S["S07_Waves"]["paragraphs"][2:]
sents("S07_Waves", 3, ["A zero's height sets how fast {#height} its wave wiggles.",
                       "{#across} Its position across the strip sets how big the wave's swings grow: {#power} roughly x to the power of that position."])
P("S07_Waves", 3)["visual"] = (
    "At the paragraph start (under 'A zero's height sets how fast', about 1.9 s): the staircase graph shrinks to a "
    "thumbnail at the top left and the main area becomes a new graph with a LOG horizontal axis from x = 10 to "
    "x = 1,000,000 (DIM tick labels '10', '100', '1,000', '10,000', '100,000', '1,000,000' and a DIM tag 'log scale' "
    "(T, 24) that stays on screen for the rest of the scene and in S08), on which each wave wiggles evenly. At "
    "{#height}: wave 1 (pink, height 14.13) and wave 5 (PALETTE green, height 32.94) draw one above the other; wave 5 "
    "wiggles more than twice as often; their zero dots in the inset pulse in their colours with the heights '14.13' and "
    "'32.94' highlighted. At {#across}: wave 5 fades; wave 1 alone fills the graph and its envelope ±2√x/(|ρ₁|·ln x) "
    "draws as a DIM dashed funnel widening to the right (exact, topic.zero_wave). At {#power}: a DIM label "
    "'size ≈ x^position' (T/N, 24; Unicode, no LaTeX) appears beside the funnel. Pause: hold.")
sents("S07_Waves", 4, ["On the middle line, that position is {#half} one half, and x to the one half {#root} is the square root of x.",
                       "It's {#digits} the same one half: half the digits, coin-flip size."])
P("S07_Waves", 4)["visual"] = (
    "At {#half}: in the inset the ACCENT line's '½' label pulses, and the funnel gains the ACCENT label 'x^½' (N, 30). "
    "At {#root}: 'x^½' morphs into '√x' (N, 30, ACCENT). At {#digits}: a thin ACCENT dashed line drops from the inset's "
    "'½' label to the dial's ½ tick; the coin icon on the dial flips once and the pin 'Riemann?' glows (this, the key "
    "reveal, lands about 3 s before the scene tail, inside the speech). Pause (scene end, 0.9 s): everything fades "
    "out, the dial last.")
P("S07_Waves", 4)["pause_after"] = 0.9
rep(S["S07_Waves"], "purpose", "from a sharpened version of Gauss's curve (which comes from the pole at 1) plus one wave per zero",
    "from a sharpened version of Gauss's curve plus one wave per zero")
rep(S["S07_Waves"], "purpose", "is the power of x at which the wave grows",
    "sets how big the wave's swings grow (about x to that power)")

# ---------------- S08 ----------------
sents("S08_OneHalf", 0, ["Now try to cheat. {#rogue} Slide one zero off the line, eight tenths of the way across.",
                         "Its wave grows like {#faster} x to the zero point eight."])
rep(P("S08_OneHalf", 0), "visual", "Empty BG, then the dial (S03 state),",
    "Empty BG, then, all fading in together over 0.8 s on 'Now try to cheat', the dial (S03 state),")
rep(P("S08_OneHalf", 0), "visual", "a hollow BAD dashed ring tagged 'imaginary' (T, 22, DIM)",
    "a hollow BAD dashed ring tagged 'hypothetical' (T, 24, DIM)")
rep(P("S08_OneHalf", 0), "visual", "slides from ½ to 0.8 at height 14.13, and its mirror twin",
    "slides from ½ to 0.8 at height 14.13 (screen label '0.8'), and at the same moment its mirror twin")
rep(P("S08_OneHalf", 1), "visual", "in BAD tint; one small shake.",
    "in BAD tint, with a single BAD tint pulse (no shake: STYLE.md keeps the shake for contradictions).")
rep(P("S08_OneHalf", 2), "visual",
    "At {#twin}: in the inset, the rogue ring slides left from 0.8 to 0.2 while its twin slides from 0.2 to 0.8 at the same time",
    "From the paragraph start (on 'Slide it left instead'): in the inset, the rogue ring slides left from 0.8 to 0.2 "
    "while its twin slides from 0.2 to 0.8 at the same time. At {#twin}: the twin arrives at 0.8 and pulses BAD")
sents("S08_OneHalf", 3, ["Only on the middle line {#equal} are the twins equally loud.",
                         "So the dial {#reads} reads the rightmost zero, which, thanks to the twins, is never left of the middle.",
                         "{#best} One half is the best the primes can do, and {#guessed} exactly what Riemann guessed."])
P("S08_OneHalf", 3)["visual"] = (
    "At {#equal}: the two rings slide toward each other; their two envelopes on the log graph close in on the √x funnel "
    "from above and below; when both reach ½ they merge into the real first zero on the line, the BAD waves become the "
    "pink √x wave, and the dial's BAD marker slides back to ½ and fades. At {#reads}: in the inset a vertical DIM dashed "
    "line sweeps in from the strip's right edge and stops at the rightmost zeros, the ACCENT line at ½, with a thin "
    "dashed drop to the dial's ½ tick; on 'thanks to the twins', a hypothetical mirror pair (two hollow BAD dashed "
    "rings at 0.3 and 0.7, height 40, tag 'hypothetical', illustration) blinks in, the one at 0.7 lights to show that "
    "the right-hand twin is never left of the middle, and the pair fades. At {#best}: the dial's '½' glows ACCENT with a "
    "small GOOD check above it and the DIM label 'best possible'. The dial never shows a reading below ½. At "
    "{#guessed}: the pin 'Riemann?' glows at ½. Pause (1.2 s, the key logic): hold.")
sents("S08_OneHalf", 4, ["The eighteen ninety-six proof only showed {#edge} no zero sits on the right edge: {#enough} enough for percentages, not for the gap.",
                         "Riemann's guess puts them {#middle} all in the middle, and the primes stray like coin flips, {#coins} and no more."])
S["S08_OneHalf"]["purpose"] = (
    "A zero off the line at 0.8 would make a wave growing like x^0.8, about sixty times the on-line size by a million, "
    "and the primes would clump; sliding it left just moves its mirror twin to the right, and the louder twin sets the "
    "error; so the dial reads the rightmost zero, which thanks to the twins is never left of one half, so one half is "
    "the best possible: exactly Riemann's guess; the 1896 proof only cleared the strip's right edge (enough for the "
    "percentages, not the gap); all zeros in the middle means the primes stray like coin flips, and no more.")

# ---------------- S09 ----------------
sents("S09_Evidence", 0, ["What made Riemann so sure? {#hint} His paper offers only a hint.",
                          "In {#hilbert} nineteen hundred, David Hilbert put Riemann's guess on his {#list} list of problems."])
P("S09_Evidence", 0)["visual"] = (
    "Empty BG; on the question, all of these fade in together over 0.8 s: the error dial at its home (state: window ½ "
    "to 1, coin and pin at ½, GOOD check 'best possible'); the strip at the left third (real part 0 to 1 over "
    "x = -6.4 to -2.6, height 0 to 50 over y = -2.5 to 3.2; ACCENT line; no zeros yet); and a thin NEUTRAL timeline "
    "across the right two thirds at y = 2.8 from 1850 to 2030 with DIM decade ticks. Then the tick at 1859 lights with "
    "a tiny paper icon and a small DIM card 'Riemann · 1826 to 1866' (T, 24). At {#hint}: under the card, a DIM "
    "one-liner (T, 24): 'his one line: about as many zeros on the line as expected' (Riemann 1859: 'etwa so viel "
    "reelle Wurzeln'). At {#hilbert}: a card at 1900: 'Hilbert · 1900 · problem 8' (T, 24, INK). At {#list}: a small "
    "scroll icon draws under it, listing faint lines, the eighth line lit ACCENT. Pause: hold.")
sents("S09_Evidence", 2, ["In {#siegel} nineteen thirty-two, Carl Ludwig Siegel dug through {#notes} Riemann's unpublished notes.",
                          "{#hand} Riemann had worked out a few zeros by hand.",
                          "So very probable {#wild} was no wild guess."])
P("S09_Evidence", 2)["visual"] = (
    "At {#siegel}: a card at 1932: 'Siegel · 1932' (T, 24, INK). At {#notes}: a sketch of a notebook page draws beside "
    "it (NEUTRAL rectangle, faint DIM handwriting squiggles; illustration). At {#hand}: from the notebook, two small "
    "ACCENT dots fly into the strip and land on the line at heights 14.13 and 25.01 (the first and third zeros), "
    "labelled with Riemann's own values 'Riemann: 14.1386' and 'Riemann: 25.31' (N, 24, DIM), then fade to INK. At "
    "{#wild}: the 'sehr wahrscheinlich · very probable' card (from S01) reappears under the timeline and gets a small "
    "GOOD check (the notes showed the work behind his one-line hint). Pause (1.1 s): hold.")
sents("S09_Evidence", 3, ["By twenty twenty-one, Dave Platt and Tim Trudgian had confirmed {#trillion} more than twelve trillion zeros, {#every} all exactly on the line."])
rep(P("S09_Evidence", 3), "visual", "on 'every one exactly on the line' a GOOD check pops",
    "At {#every}: a GOOD check pops")
sents("S09_Evidence", 4, ["For decades, the proven share of zeros on the line stayed {#forty} around forty percent.",
                          "Then {#thirds} a new proof in twenty twenty-six, still under review, pushed it past two thirds."])
rep(P("S09_Evidence", 4), "visual", "A thin DIM note under the bar: 'a share, not all'.",
    "A thin DIM note under the bar: 'a share, not all' (T, 24). Keep the 'preprint' tag on the card; do not remove it.")
S["S09_Evidence"]["purpose"] = (
    "Riemann's paper gives only a one-line hint for his confidence (about as many zeros on the line as he expected); "
    "Hilbert put the problem on his 1900 list; Hardy proved in 1914 that infinitely many zeros are on the line (not "
    "necessarily all); in 1932 Siegel found in Riemann's notes that he had computed a few zeros by hand; by 2021 more "
    "than twelve trillion zeros were checked, all on the line; the proven share on the line stayed at about forty "
    "percent for decades, and a 2026 proof, still under review, pushes it past two thirds.")

# ---------------- S10 ----------------
sents("S10_WhyHard", 1, ["And the primes have fooled us before. {#below} For every number ever checked, the staircase stays below Gauss's curve.",
                         "Yet in {#littlewood} nineteen fourteen, John Littlewood proved {#must} the staircase must cross above, {#cross} possibly first near a number three hundred and seventeen digits long."])
rep(P("S10_WhyHard", 1), "visual", "At {#littlewood}: caption 'Littlewood · 1914' (T, 24, INK).",
    "Gauss's curve here is li(x) exactly (topic.li_curve = mpmath.li, not li(x) − 1.045, which would fail the 'below' "
    "claim at x = 2 to 7); the graph starts at x = 10, where li − π = 2.17 > 0. At {#littlewood}: caption "
    "'Littlewood · 1914' (T, 24, INK). At {#must}: a small ACCENT down-arrow appears at the far right of the gap line, "
    "pointing at the zero line.")
sents("S10_WhyHard", 2, ["Even proving that almost all zeros are on the line {#almost} wouldn't rule out a single rogue, and one would {#moves} move the dial.",
                         "{#window} The dial's window has never narrowed: nobody can even prove it reads {#below_one} below zero point nine nine."])
rep(P("S10_WhyHard", 2), "visual",
    "a single hollow BAD dashed ring tagged 'one rogue?' (illustration; no such zero is known) blinks off the line; the bar's 100% label stays DIM.",
    "a single hollow BAD dashed ring tagged 'one rogue?' (T, 24; illustration; no such zero is known) blinks off the "
    "line, its mirror twin blinking in at the same moment; the bar's 100% label stays DIM. At {#moves}: a small BAD "
    "marker on the dial jumps from ½ to the rogue's real part and hangs there, dashed (illustration).")
rep(P("S10_WhyHard", 2), "visual", "At {#window}: the ring and bar fade;",
    "At {#window}: the ring, its twin, the BAD dial marker and the bar fade;")
sents("S10_WhyHard", 3, ["In {#guth} twenty twenty-four, Larry Guth and James Maynard proved {#few} there can't be too many zeros far from the line.",
                         "It beat {#ingham} a record that had stood since nineteen forty."])
rep(P("S10_WhyHard", 3), "visual", "At {#ingham}: a small DIM tag 'best since Ingham, 1940' under the caption.",
    "At {#ingham}: a small DIM tag under the caption: 'beats Ingham's 1940 bound (near real part ¾)' (T, 24). Nothing "
    "suggests that Guth and Maynard found or excluded specific zeros.")
rep(S["S10_WhyHard"], "purpose", "the first real progress there since 1940",
    "beating Ingham's 1940 bound near real part 3/4, a record that had stood since 1940")

# ---------------- S11 ----------------
P("S11_Callback", 1)["pause_after"] = 1.0
P("S11_Callback", 2)["pause_after"] = 1.0
rep(P("S11_Callback", 3), "visual", "Final pause (2.0 s):",
    "Final pause (1.5 s in the script; the engine allows 2.0 on the video's last paragraph once the validator does, "
    "see CHANGELOG):")

sents("S11_Callback", 0, ["Let's go back to the start: {#grid} the numbers up to a hundred, and {#stair} their staircase."])

sents("S09_Evidence", 1, ["In {#hardy} nineteen fourteen, Godfrey Hardy proved infinitely many zeros sit on the line, {#notall} though not necessarily all."])
sents("S05_Plane", 0, ["Riemann's leap was to feed zeta {#plane} points on a plane, not numbers on a line: {#right} how far right, and {#up} how far up."])
sents("S08_OneHalf", 2, ["Slide it left instead, and {#twin} its mirror twin lands on the right.", "{#louder} The louder of the two sets the error."])

rep(P("S04_Zeta", 3), "visual", "the right side 'only primes' (T, 24, DIM)",
    "the right side 'only primes' (T, 24, DIM) (the two labels appear as 'all whole numbers' and 'primes alone' are spoken; the whole rearrangement runs through the sentence, about 5 s)")
rep(P("S08_OneHalf", 0), "visual", "on the dial a small BAD marker slides from ½ to 0.8 in sync.",
    "on the dial a small BAD marker slides from ½ to 0.8 in sync; the slide is slow (about 2.5 s), timed to 'eight tenths of the way across'.")
rep(P("S08_OneHalf", 4), "visual", "At {#middle}:",
    "At {#enough}: a small echo of the S02 table pops in beside the inset: the percentage column '5.4% → 0.013%' with a GOOD check, and the gap column '9.6 → 754.4' with a DIM '?'; the dial's window pulses once and stays ½ to 1. At {#middle}: the table echo fades;")
S["S08_OneHalf"]["paragraphs"][4]["visual"] = S["S08_OneHalf"]["paragraphs"][4]["visual"].replace("'1896: no zeros on the edge'", "'1896: no zeros on the right edge'")

rep(P("S10_WhyHard", 2), "visual", "labelled '0.99' (N, 22), with 'proved?' (T, 22, DIM)", "labelled '0.99' (N, 24), with 'proved?' (T, 24, DIM)")

# ---------------- pron, notes, facts ----------------
d["pron"].update({"Zeta": "/zˈeɪtə/", "Vallée": "/vɑlˈeɪ/", "Helge": "/hˈɛlɡə/", "Jacques": "/ʒˈɑk/"})

notes = d["pronunciation_notes"]
notes[4] = ("'fourteen point one three', 'two point three', 'zero point eight', 'zero point nine nine' are read digit "
            "by digit. S08 P1 says 'eight tenths of the way across' (not 'to zero point eight') so the number 'zero' "
            "does not tangle with a zero of zeta; the screen label stays '0.8'.")
notes[7] = ("'Very probable' is a thread: S01 (the guess), S09 ('So very probable was no wild guess'), S11 (final "
            "line). S09 now says the paper 'offers only a hint' (it gives one line: about as many zeros on the line as "
            "expected), not that it gives no reason.")
notes.append("Names for the critical line, in order: 'the middle of the strip' (S06 P3), 'this middle line' (S06 P5), "
             "'the middle line' (S07 P5, S08), then 'the line'. 'Fold' is only the action (S06 P4). S11 calls back to "
             "'one straight line'.")
notes.append("Listen-check once: 'Jacques', 'Vallée', 'Helge' (new pron entries; Whisper is prompted with the script, so "
             "its match proves little) and 'By twenty twenty-one' (S09 P4). If the year sounds clipped, change it to "
             "'By the year twenty twenty-one' (+2 words).")
notes.append("S03 P5 says 'x's digits': listen once that Kokoro reads it as 'ex-iz digits'; if not, use 'the digits of x' (+1 word, still inside the 1,450 cap).")
notes.append("The pron table is case-sensitive: 'Zeta' (sentence start, S04 P5) has its own entry.")
notes.append("'A hundred and sixty-seven years later' (S11) is right for 2026 only; update it if the video is released "
             "in 2027 or later.")

F = d["facts"]


def fact(prefix):
    hits = [f for f in F if f["claim"].startswith(prefix)]
    assert len(hits) == 1, prefix
    return hits[0]


fact("Bernhard Riemann's paper")["claim"] = (
    "Bernhard Riemann's paper 'Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse' appeared in November 1859 "
    "in the Monthly Reports of the Berlin Academy, about eight pages; its only stated reason is one clause, 'one finds "
    "between those limits about that many real roots' (etwa so viel reelle Wurzeln), followed by 'it is very probable "
    "(sehr wahrscheinlich) that all roots are real'; after some fleeting vain attempts he set the search for a proof "
    "aside because his next objective did not need it.")
fact("Bernhard Riemann's paper")["source"] += (" ; Bombieri, Clay problem description (quotes the clause): "
                                                "https://www.math.ucdavis.edu/~tracy/courses/math205A/riemann.pdf")
fact("Gauss first studied")["claim"] = (
    "Gauss first studied prime density 'in the year 1792 or 1793', aged 15 or 16, and over the following decades "
    "counted primes in blocks of a thousand ('chiliads') in idle quarter hours; by 1849 his tables reached about three "
    "million (letter to Encke, 24 December 1849).")
fact("Gauss first studied")["source"] += " ; https://arxiv.org/pdf/1311.1093"
fact("The prime number theorem was proved")["claim"] = (
    "The prime number theorem was proved independently in 1896 by Jacques Hadamard and Charles-Jean de la Vallée "
    "Poussin; the percentage error (li(x) − prime count)/li(x) tends to 0 while the difference is unbounded (5.4% and "
    "9.6 at 1,000; 0.16% and 129.5 at 10^6; 0.013% and 754.4 at 10^8). The key step was that zeta has no zeros on the "
    "line with real part 1.")
fact("Zeros on the critical line exist")["claim"] = (
    "Mirror pairs force every zero or its twin to have real part at least 1/2, so the supremum of the real parts (the "
    "dial reading) is never below 1/2; zeros on the line exist (the first at 14.13; infinitely many by Hardy 1914); so "
    "one half is the best possible error exponent (Littlewood: the error exceeds about √x/ln x infinitely often).")
fact("Carl Ludwig Siegel")["claim"] = (
    "Carl Ludwig Siegel published in 1932 his study of Riemann's unpublished notes, showing Riemann had computed a few "
    "zeros by hand (certainly near 14.1386 and 25.31, the first and third) with the method now called the "
    "Riemann–Siegel formula.")
fact("Conrey (1989)")["claim"] = (
    "Conrey (1989) proved more than two fifths (40%) of the zeros lie on the line; the record stayed near 41.7% (Pratt "
    "et al. 2020) until Alpöge and Furman (arXiv 2608.13637, August 2026, preprint, not yet refereed, Lean-formalized) "
    "proved more than two thirds (67.25%), independently reproved by Lamzouri (arXiv 2609.02882).")
fact("π(x) < li(x)")["claim"] = (
    "π(x) < li(x) for every x ever checked (proved up to 10^19), yet Littlewood proved in 1914 that the difference "
    "changes sign infinitely often; crossings are known near 1.397·10^316 (a 317-digit number), and it is not known "
    "whether that is the first crossing (hence 'possibly first').")
fact("Larry Guth and James Maynard")["claim"] = (
    "Larry Guth and James Maynard (arXiv May 2024; Annals of Mathematics 203(2), 2026) proved a new bound limiting how "
    "many zeros can lie far from the critical line, beating Ingham's 1940 bound in the critical range near real part "
    "3/4, a record that had stood for more than 80 years (Ingham's bound had been improved earlier only for real part "
    "above 3/4, e.g. Huxley 1972).")
F.append({"claim": "Exact prime-generating formulas exist (Willans 1964, Mills' constant) but are useless in practice; "
                   "no simple formula gives the next prime, hence 'No simple formula tells you'.",
          "source": "https://en.wikipedia.org/wiki/Formula_for_primes"})
F.append({"claim": "Riemann stated the explicit formula in 1859; von Mangoldt gave the full proof in 1895.",
          "source": "https://en.wikipedia.org/wiki/Explicit_formulae_for_L-functions ; "
                    "https://en.wikipedia.org/wiki/Riemann_hypothesis"})
F.append({"claim": "The error dial reads the share of x's digits in the error: an error of size x^θ has about θ times "
                   "as many digits as x; the dial reading is the supremum of the real parts of the zeros.",
          "source": "Ingham, The Distribution of Prime Numbers (1932), Thm 30 ; research_facts.md §4.2"})

out = ROOT / "script.json"
out.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("wrote", out)
