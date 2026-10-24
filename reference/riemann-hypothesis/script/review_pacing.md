# Pacing, TTS and animation review: script_synth.json

Measured with Kokoro af_heart at speed 0.85, running `timeline.py` on a scratch copy (`out/pacing_scratch/timeline/*.json`). `validate_script.py` reports 0 ERRORs. Whisper reported 0 WARNs, but Whisper gets the script as its `initial_prompt`, so that check is weak. I also ran an unprompted Whisper pass on the risky lines (see LOW-4).

## Measured totals

| scene | dur (s) | words | notes |
|---|---|---|---|
| S01_Hook | 63.5 | 148 | longest; "Riemann Hypothesis" is first said at 44.6 s |
| S02_Gauss | 50.1 | 121 | two freezes of 6 to 7.5 s |
| S03_CoinFlips | 64.9 | 169 | |
| S04_Zeta | 49.3 | 127 | 8.45 s freeze in p3 |
| S05_Plane | 43.5 | 118 | |
| S06_Zeros | 55.7 | 138 | |
| S07_Waves | 54.9 | 143 | |
| S08_OneHalf | 52.2 | 139 | |
| S09_Evidence | 51.7 | 122 | |
| S10_WhyHard | 51.1 | 124 | |
| S11_Callback | 36.3 | 96 | close to the 35 s floor |
| **Total** | **9:33.3 (573.3 s)** | **1445** | |

- Total: 9:33 is inside the style band (9:30 to 10:30), but only 3 s above its floor. The word count (1445) is 5 below the cap. Every fix below adds bookmarks only, or at most +4 words. **Do not make net word cuts.** A cut of 20 words drops the video below 9:30.
- Every scene is 35 to 90 s. No pause is longer than 1.53 s, so there is no silent stretch that violates the hard constraint.
- Delivery rate: the median is about 180 wpm, which is on spec. Kokoro rushes some sentences: S06 p3s1 at 231 wpm, S01 p1s1 (the video's first line) at 228, S11 p4s1 at 217, S11 p3s1 at 215, S04 p1s2 (the formula) at 213.

## BLOCKER
None. Every problem below can be fixed by moving bookmarks, editing storyboards or making tiny text edits.

## HIGH

**H1. S04 p3: the picture freezes for 8.45 s** (euler@19.22 to evens@27.67). The factor `(1 − 1/2ˢ)` appears at {#evens}, but the voice says "one minus one over two to the s" about 2.7 s before that.
Fix (no word change):
`In {#euler} seventeen thirty-seven, Euler found {#bridge} a bridge to the primes.` / `Multiply the sum by {#factor} one minus one over two to the s, and {#evens} every even term drops out.`
Storyboard: the 30 tiles lay out at {#bridge} (21.74), not at the paragraph start. The blue factor appears at {#factor} (24.99). The evens flash and fade at {#evens} (27.67). The gaps become 2.5 s, 3.3 s and 2.7 s.

**H2. S02 p4: {#add} → {#curve} is only 0.30 s** (34.38 → 34.68). The axes, the density panel and the area sweep must all appear in 0.3 s before the teal curve starts. {#add} also lands after "Add those chances up", which is late.
Fix: `{#add} Add those chances up, and {#curve} out comes Gauss's smooth curve.` This gives 1.6 s. Also, chance→add is still 4.9 s, so give that beat motion: the single lit tile hops to a new random tile about every 0.6 s ("about one in fourteen").

**H3. S02 p5: the picture freezes for 7.45 s** (proof@37.42 → ratio@44.87). Only a caption is on screen while two long names and "proved Gauss right. But read the fine print" play.
Fix: `…Poussin {#right} proved Gauss right.` (41.52): a GOOD check appears by the teal curve. `But {#fine} read the fine print:` (43.49): the graph shrinks left and the table headers appear. The rows then fill from {#ratio}. The gaps become 4.1, 2.0, 1.4 and 2.3 s.

**H4. S02 p1: the picture freezes for 6.4 s** (gauss@2.14 → blocks@8.52). The scene also opens on an empty background for 1.8 s while the voice says "That smooth curve".
Fix: `…Carl Friedrich Gauss, {#year} around seventeen ninety-two.` (4.60): the second line of the card, 'about 1792 · age 15 or 16', writes in. Storyboard: at P_START, show a small echo of the S01 teal curve at the top right, then let it fade at {#gauss}.

**H5. S07 p5: {#height} sits at the paragraph start (0.0 s), and the graph change has no time.** The whole change (the staircase shrinks to a thumbnail and a new log-axis graph appears) must then run inside p4's 1.1 s pause, which is meant to hold the reveal "it is the staircase, exactly". After {#across} there is a 7.1 s static stretch (+0.8 s pause).
Fix: `A zero's height sets how fast {#height} its wave wiggles.` (34.76). The graph change runs at P_START (1.9 s), and waves 1 and 5 draw at {#height}. Then `…how fast the wave grows: {#power} roughly like x to the power of that position.` (40.53): the label 'size ≈ x^position' appears here, not at {#across}.

**H6. S06 p7: the scene end is overloaded** (goal@52.86 → scene end 55.67, 2.8 s). The storyboard fits a shrink into the inset, a staircase preview drawing and a full fade-out into that time. S07 then fades the same inset and dial back in, so the move is also wasted motion.
Fix: at {#goal}, the three dashed verticals glow and the strip and zeros dim to 60%. Everything fades out in the tail with the dial last. Delete the inset move and the staircase preview. S07 already builds both.

**H7. Scene-end pauses above 0.9 are silently clamped to 0.9, yet their storyboards promise longer holds.**
- S03 p6: pause 1.1, measured 0.93. The storyboard wants "pin glows, content fades, dial fades last" inside that time.
- S07 p6: pause 1.2, measured 0.92. It is labelled "the key reveal" and must also fade everything out.
- S02 p5: pause 1.0, measured 0.93.

Fix: set these pause_after values to 0.9 and move each hold into speech.
- S07: `It's {#digits} the same one half: half the digits, coin-flip size.` (50.82). The ACCENT drop line and the coin flip then land about 3 s before the tail, and the tail is only the fade.
- S03: the pin glow lands at {#pin} (60.60). There are 3.3 s of speech after it, and the tail is only the fade.

**H8. S03 p5: {#dial} → {#zero} is only 0.80 s.** The whole dial must build in that time (backing panel, ruler, three ticks, labels, caption). Also, "one, an error with as many digits as x" is ambiguous when heard once. Kokoro reads the 22-word string as one clip, so the two sentences get no 0.55 s gap between them.
Fix (+3 words, total 1448): `Let's put {#dial} this on a dial.` / `{#zero} Zero would mean the error never grows.` / `{#all} One would mean an error with as many digits as x.` This gives the dial about 1.9 s and makes the "one" clear.

## MEDIUM

**M1. S07 p1 / S06 p7 / S08 p1 / S09 p1: scene openings stack several fade-ins into 1 to 2 s of speech.** For example, S09 fades in the dial, the strip and the timeline, and lights the 1859 tick, all during "What made Riemann so sure?" (1.6 s). That is fine if they fade together in 0.8 s. Say so in the storyboards ("all fade in together over 0.8 s"), or animators will chain them and spill past the first bookmark.

**M2. S06 p2: {#strip} → {#only} is 2.95 s** and must fit the strip tint, the dial fade-in and a large layout transform. Fix: fade the dial in at S06 p1 start (under "Now, where does the extended zeta equal zero?", 3 s of speech with little on screen). {#strip} then only has to carry the tint and the transform.

**M3. S06 p4: the BAD "hypothetical" rings have no bookmark of their own.** They appear at {#fold} (32.16), together with a 1 s flip and the opening back, but the voice says "mirror pairs" 1.3 s earlier. Fix: `And zeros come in {#pairs} mirror pairs: {#fold} fold the strip…` (30.82). The rings appear at {#pairs} and the flip runs at {#fold}. Also sync the {#more} zero flashes to the word times of "twenty-one", "twenty-five" and "thirty" (26.1 to 28.4 s).

**M4. The 'imaginary' tag on the hypothetical rings (S06 p4, S08 p1) will be misread.** Five scenes earlier, S05 put "i marks the up-part" on screen. A viewer will read 'imaginary' as the imaginary part. Change the tag to 'hypothetical' (T, 22, DIM).

**M5. S01 p4: count→back is 1.52 s**, which is too fast for the signature moment where the grid tiles fly into the staircase. Fix: `But {#count} count them, one step up per prime, and {#back} step back.` This gives about 1.9 s. The zoom then has 1.86 s to reach {#blur}, and the storyboard asks for 2 s. Make it 1.7 s.

**M6. S03 p2: walks→thousand is 1.2 s** for drawing seven million-step walks. Fix: `{#walks} After a million flips, you typically end up {#thousand} about a thousand steps from the start.` This gives about 2.9 s of drawing before the envelope.

**M7. S09 p1 and p3 hold cards too long.**
- hilbert→end is 5.4 s, plus a 0.8 s pause. Add `on his {#list} list of problems` (9.24) so the scroll icon draws with its eighth line lit.
- siegel→hand is 5.7 s. Add `dug through {#notes} Riemann's unpublished notes` (23.64) so the notebook sketch draws there.

**M8. S10 p2: below→littlewood is 5.8 s.** Give the gap line a slow draw across the full 5 s, or add `proved it {#must} must cross above` so an ACCENT down-arrow appears at the far right before the axis break at {#cross}.

**M9. S04 p1s2 is a 22-word spoken formula at 213 wpm (6.2 s).** A non-expert hears the whole definition of zeta in one breath. Split it with a sentence gap (+1 word): `{#pick} Pick a number, s.` / `Then add {#terms} one, plus one over two to the s, plus one over three to the s, forever.` The terms still write in on the word times of each "one over …".

**M10. S11 finale rushes** (p3s1 at 215 wpm, p4s1 at 217). Kokoro speed is global, so give the ending more air instead:
- p2 pause from 0.8 to 1.0 and p3 from 0.8 to 1.0.
- p4 pause_after from 1.5 to 2.0. The storyboard already says "Final pause (2.0 s)", but 1.5 is what the engine uses. The engine allows 2.0 on the final paragraph.

This adds about 0.9 s and lifts S11 to about 37.2 s.

**M11. S01 is 63.5 s against the pilot's 38 s hook.** The title is said at 44.6 s and the honest status lands at 53 to 62 s. I am not recommending cuts, because of the time floor. If the synthesizer wants a faster hook, move the p3 "101" beat's words to S02 or S11, and do not delete them.

## LOW

**L1. The pron table is case-sensitive** (`\bzeta\b`). "Zeta knows the primes" (S04 p5) does not get the IPA, so Kokoro uses its default and may say it differently from "zeta" in the sentence before. Add `"Zeta": "/zˈeɪtə/"`. Also consider `"Vallée": "/vɑlˈeɪ/"`, `"Helge": "/hˈɛlɡə/"` and `"Jacques": "/ʒˈɑk/"`. Listen-check these three: Whisper was prompted with the script, so its match proves little.

**L2. S08 p2 uses "one small shake" for a hypothetical lumpy staircase.** STYLE.md keeps the shake for contradictions. Use a BAD tint pulse instead.

**L3. S08 p3: the ring slide lags the words.** The voice says "Slide it left instead" at 17.57, but the slide starts at {#twin} (19.33). Start the slide at P_START (p3s1) and keep {#twin} for the twin's arrival. Also, S08 p2's '≈ 63 ×' against the spoken "about sixty" is fine, but the label could read '≈ 60×' to match the voice.

**L4. "By twenty twenty-one" (S09 p4) comes out fast** (0.52 s for the year). Unprompted Whisper hears "By 2021", so it is intelligible. Prompted Whisper heard "By twenty -one", so the alignment skips one word; the bookmarks are unaffected. Listen once. If it sounds clipped, use "By the year twenty twenty-one" (+2 words; measured: the year then takes 0.62 s and is heard as "2021").

**L5. S09 p4: the GOOD check is tied to "every one exactly on the line", which has no bookmark.** Add `{#every} every one exactly on the line` (39.66).

**L6. S11 p4: "A hundred and sixty-seven years later" is correct for 2026 (1859 + 167).** It goes out of date if the video is released after 2026. Note this in the release checklist.

**L7. S04 p5: zeta→knows is 0.86 s.** The collapse into ζ(s) and the bridge arc are close together but fine. Keep the collapse at 0.7 s.

