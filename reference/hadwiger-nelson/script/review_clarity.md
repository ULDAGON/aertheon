# Clarity review: script_synth.json (lay-viewer comprehension)

Reviewer role: a curious viewer with no math background, listening once at normal speed.
Scope: jargon, logical leaps, unclear referents, steps the storyboard does not show, attention drops, textbook tone.
Accuracy is checked only where a wording change could affect it.

## Verdict

The structure is right, and most individual beats are excellent. The problems cluster in three places:

1. **The foundations are missing three definitions.** The script never says why the unit's size does not matter, never says what "the plane" is, and never says what a stick means inside a dots-and-sticks drawing.
2. **The Moser spindle (S06), the heart of the video, has three gaps.** It gives no goal before the construction. It never says why the new stick is allowed. Its key "try it" paragraph is abstract and hard to follow by ear.
3. **Referent chains break in the abstract passages.** S09 uses "one structure / another / the second / the first / such a triple", and S08 uses "rule a number out" and "it did".

Word budget: every must-fix below, plus cutting S11 P4, gives **1,441 words**. Adding the optional "keep score" line brings it to **1,447**. Both are inside 1,350–1,450. The table is at the end.

Bookmarks keep their original names where the event is unchanged. New bookmarks are marked. All of them are unique within their scene.

---

## HIGH: blocks understanding of the core argument

### H1. S06 P4: the key moment of the proof is abstract and elliptical
Lay viewer: *"The bottom takes one color, the first middle pair the other two..."*. "The other two" of what? By ear, "the first middle pair the other two" has no verb, and Kokoro will read the gapped clause with flat, confusing prosody. "The second diamond goes the same way, until its top tip has nothing left" gives no reason why nothing is left. The storyboard shows the colors (A pink, B blue, C yellow, D pink), but the narration names none of them. Picture and voice do not match at the most important moment.

Rewrite (use the colors on screen, and reuse the word "leftover" from S05):
> Say {#bottom} the bottom tip is pink. The first diamond's middle dots {#pair} take blue and yellow, so {#top1} the first top tip gets the leftover: pink. {#second} The second top tip can't be blue or yellow either, and the new stick {#stuck} rules out pink.

Storyboard: keep the order. At {#second}, B2 and C2 fill yellow and blue, and D2 gets mini swatches for blue and yellow, both crossed out. At {#stuck}, the D–D2 stick flashes and a pink swatch is crossed out, then D2 flashes BAD.
Words: 35 → 41 (+6).

### H2. S06 P2: the new stick is not justified, and "Its" has two possible referents
Lay viewer: *"Stop right there, and join the tips with a stick."* Why am I allowed to add a stick? The voice never says the tips are now **exactly one unit apart**, and that is the whole point. Only an on-screen readout shows it. Also, "Its top tip" comes right after "every stick keeps its length", so "its" could mean the stick.

Rewrite (the first sentence stays as it is):
> {#swing} Swing the copy open, and every stick {#keeps} keeps its length. The copy's top tip drifts outward from the ring's center, so at some moment {#reach} it lands on the ring. Stop there: the tips are exactly one unit apart, {#join} so join them.

Words: 29 → 31 for the changed sentences (+2).

### H3. S06: the viewer watches a construction without knowing its goal
Lay viewer: *"Why are we copying the diamond? Why are we swinging it?"* The purpose ("force a match, then forbid it") is only named in P7, after the payoff. Following 40 seconds of construction with no goal is where attention drops. 3Blue1Brown-style exposition states the plan first.

Fix: add the plan as the first sentence of P1. Use new bookmark names, because P7 already uses {#force} and {#forbid}.
> The plan: {#plan_match} force two dots to match, {#plan_stick} then join them with a stick.

Storyboard: under the 'diamond rule' badge at the top left, a small DIM line appears: 'plan: force a match' at {#plan_match}, then '… then forbid it' at {#plan_stick}.
Then shorten P7 to a callback, since the plan has already been stated:
> This is {#moser} the Moser spindle, published by the brothers Leo and William Moser in nineteen sixty-one. {#force} Force a match, {#forbid} then forbid it. Remember that trick.

Words: +13 and −7 (net +6).
Note: after H1–H3, S06 has about 216 words, which is about 90 s at speed 0.9. That is at the top of the allowed range, so do not add anything else to this scene.

### H4. S04 P6: the dots-and-sticks rule is never stated, and "some number of colors" is vague
Lay viewer: in S01, a "stick" was something you drop on the floor. Here, sticks suddenly become fixed lines in a drawing. Nothing says **a stick goes exactly where two dots are one unit apart**. S05 and S06 depend on this completely. "If a shape can't be colored with some number of colors, it's a trap: neither can the plane" is abstract, and "neither can the plane" is an ellipsis the ear has to resolve.

Rewrite:
> So we can forget the plane and study {#dots} dots and sticks, with a stick wherever two dots are one unit apart. If a drawing can't be colored with, say, three colors, {#trap} it's a trap: neither can the plane.

Storyboard: at {#dots}, add a caption under 'dots and sticks': 'stick = exactly 1 apart → different colors'.
Words: 30 → 38 (+8).

### H5. S02: "one unit" is never explained, although the scene's purpose says it is
Lay viewer: from the first line of S01, *"one unit of what? An inch? A meter? Does it matter?"* The S02 purpose lists "the unit's size is irrelevant", but no sentence says so.

Fix: add a new paragraph **after P3** (the disk) and before P4 (borders), with pause_after 0.6:
> The unit can be an inch or a mile: {#zoom} zooming doesn't change the puzzle.

Storyboard: a dot pair joined by a stick labeled '1'. A DIM caption under it reads 'inch'. At {#zoom}, the camera zooms far out while the caption changes to 'mile', and the stick keeps its '1' label: the picture is unchanged. Fade.
Words: +14.

### H6. "The plane" is used from S03 onward but never defined, and S01 P5 is a vague promise
Lay viewer: S01 and S02 say "floor". S03 P4 suddenly says "across the plane", and from S04 on the script says "plane" 15 or more times. Some listeners will hear "plane" as an aircraft for a moment. Separately, S01 P5 ("you'll solve some puzzles and fail others, and the failures hide the best ideas") is generic, and its card-flip visual carries no content. It is an attention leak right after the strongest line of the hook.

Fix:
- **Cut S01 P5.** End S01 on "We just don't know which." Move P5's "everything fades out" instruction into the P4 pause.
- Define the word at its first use, in S03 P4:
> Stretch the stripes {#bands} into bands across the whole floor, which mathematicians call {#plane} the plane.

Storyboard: at {#plane}, a small DIM caption 'the plane' appears at the top left and fades after 1.5 s.
Words: −17 and +6 (net −11).

### H7. S07 P2: "Squares like that work with nine colors" is a leap
Lay viewer: *"Why nine? Why do squares work?"* Only one condition is spoken (too small to hold a stick). The second condition, that **same-colored patches must be more than one unit apart**, is shown on screen (the gap of 1.33) but never said. P5's summary "too far to reach a twin" then refers back to something that was never introduced.

Rewrite:
> A patch can be one color {#small} if it's too small to hold a stick. Same-colored patches must also stay {#apart} more than one unit apart. Squares {#block} manage both with nine colors. Can you {#beat} beat nine?

Storyboard: new {#apart}. Two same-colored squares get the dashed gap measure '1.33' next to a UNIT_COLOR stick '1'. Move that measure out of {#block}, which keeps the 3-by-3 block and its tiling.
Words: 21 → 30 (+9).

### H8. S09 P3–P5: the referent chain collapses and "alternate corners" is jargon
Lay viewer: *"One structure forces such a triple in at least one of its wheels. Another... forbids it in its central wheel. Attach a copy of the second to every wheel of the first."* By this point the listener cannot track what "the second" and "the first" mean. "Alternate corners" and "triple" are textbook words. Nothing says why three same-colored rim dots are even allowed, so a viewer who remembers the rule will object.

Rewrite: give the two parts names that match the force/forbid idea, and say why a match is legal.
- P3, second sentence:
> With four colors, watch {#triple} every other dot around the rim. Sometimes all three match, and that's allowed: {#allowed} no sticks join them.
- P4:
> One shape, {#forces} the forcer, guarantees a match like that in some wheel. Another, {#forbids} the blocker, built from Moser spindles, rules it out on its central wheel.
- P5:
> Attach a blocker {#attach} to every wheel of the forcer. The match is forced somewhere {#nowhere} but blocked everywhere, so four colors have nowhere to go.

Storyboard: the labels become 'forcer' (ACCENT) and 'blocker' (BAD). At {#allowed}, the dashed √3 triangle gets a DIM tag 'not sticks'.
Accuracy check: this matches the fact sheet §7.2. L forces a monochromatic triple in some copy of H. M forbids it in its central H. One M is attached to each H in L.
Words: +5, +2 and −3 (net +4).

---

## MEDIUM: causes confusion or drift

### M1. S08 P4: "rule a number out" and "show a number works" are ambiguous
Lay viewer: does "ruling out four" mean four is too few, or four is too many? Tie the sentences to the scoreboard ends, which the storyboard already shows with arrows.
> Why so stuck? To push the four up, you need {#trap} a trap. To pull the seven down, you need {#pattern} a better pattern for the whole endless plane.

Words: 24 → 24 (+0).

### M2. S08 P1 contradicts what the viewer just heard in S06
Lay viewer: S06 said the Mosers showed "at least four" in 1961. S08 says "Nelson already knew four were needed". *"Wait, who was first?"* Put the year into the sentence so the order is clear:
> Nelson {#nelson} already knew in nineteen fifty that four were needed, so from the start, {#pinned} the answer sat between four and seven.

Words: 18 → 21 (+3).

### M3. S04 P3: "one unit from both" and "So it can be" have unclear referents
"Both" what: rings or points? "It" could be either crossing, or the ring.
> The two rings {#cross} cross, and each crossing is one unit from both points. So a crossing can be {#neither} neither blue nor yellow.

Words: +2.

### M4. S03 P2: "each keeping its left end but not its right" is textbook shorthand for half-open intervals
Lay viewer: *"Keeping its end? Why do ends matter?"* Connect it to the border rule already set up in S02 P4:
> Two colors work: {#stripes} alternating stripes one unit long. {#left} Each border point belongs to the stripe on its right.

Words: +1.

### M5. S02 P3: the disk sentence skips the reason
*"A tiny disk alone would need endless colors."* Why? The missing step is that every two points in the disk are closer than one unit, so they would all clash.
> Ban shorter distances too, and {#disk} every point in a tiny disk clashes with every other: endless colors.

Words: +2.

### M6. S08 P5–P6: a cryptic hedge, an unexplained "reassuring", and a dangling "it did"
"Under the standard rules of mathematics" makes the lay viewer ask what other rules there are, and the video never answers. "Proved something reassuring" does not say why it reassures. "Erdős himself suspected it did" has a referent two sentences back.
> In nineteen fifty-one, {#dbe} de Bruijn and Erdős showed that hunting for a trap wasn't hopeless. If the plane needs a fifth color, {#finite} some finite trap proves it. Erdős himself suspected {#erdos} five were needed.

Keep the on-screen tag 'with the usual axioms' from the existing storyboard. It carries the accuracy caveat (fact sheet §9.1) without a spoken detour. If the fact reviewer insists on a spoken hedge, use "Assuming the usual rules for infinite sets," and not "standard rules of mathematics".
Words: 34 → 33 (−1).

### M7. S11 P2: "To prove six" is ambiguous, and "forty-two dots" works against the point
"Prove six" could mean six is the answer, or six are needed. "It would need at least forty-two dots" sounds *small* right after 509. A lay viewer concludes "so just search forty-two dots", which is the opposite of "why so hard".
> Why so hard? To show six colors are needed, you'd need {#six} a trap that five colors can't escape. {#none} None is known.

Storyboard: at {#none}, the '?' cloud stays empty, with the tag 'none known'.
Words: 26 → 21 (−5).

### M8. S07 P1: "is some number of colors always enough?" reads oddly
It sounds like a yes-or-no question whose answer is obviously "yes".
> Now flip it around: {#enough} how many colors are definitely enough?

Words: −1.

### M9. S07 P5: "with room to spare" is unclear, and the honest note about borders is lost
The brief asks for a brief, honest note about borders. "Room to spare" does not tell a lay viewer that the size margins are what make any border choice safe.
> Border points {#border} just take a neighbor's color. There's enough slack that {#slack} nothing breaks.

Storyboard: new {#slack}. The '0.90 < 1' and '1.19 > 1' readouts flash briefly while the camera eases back out.
Words: +2.

### M10. S11 P4: recommend cutting it (the budget and the ending both benefit)
This is the third "why so hard" beat in a row, and it arrives after the viewer has already heard "five, six, or seven, and we still don't know which". "Exactly" is used in two senses in two consecutive sentences (the exact distance, then "exactly seven"). The underlying result is a preprint (fact sheet §1.2, medium confidence). Cutting it (−31 against the original) makes room for H1–H8 and gets the ending to its callback faster.
If it stays, use this tighter version (26 words, −5), and cut about 15 words elsewhere:
> The whole mystery lives {#exactly} in one word: exactly. Ban every distance near one too, {#band} thickening each ring into a band, and the answer is known: {#seven} seven.

### M11. Visual beats that will outrun the voice (the v1 failure mode)
- **S04 P5.** "However you paint the plane, these three points get painted too" is about 4 s. The storyboard fits a mosaic fade-in, a zoom-out, three glide-and-sample landings with BAD flashes, and a zoom back in (only 0.8 s of pause) into that time. Expect 3–4 s of silent motion. Fix: two landings only, with 0.6 s glides, and move "camera eases back in" to the lead-in of P6.
- **S06 P6.** There are three landings between {#sits} and {#four}, about 4.5 s of voice. This is tight. Cap it at two landings.
- **S09 P5.** Copies fly onto "every wheel" one after another. Make the whole fly-in finish before {#nowhere}, for example by snapping on 13 copies at 0.15 s intervals.

---

## LOW: polish

### L1. S05 P5: "We never chose which three colors, so this always happens" is confusing and repeats the next sentence
Merge the two sentences:
> No problem yet: the tips are about {#dist} one point seven three units apart. Call it {#rule} the diamond rule: with any three colors, {#any} a diamond's tips always match.

Storyboard: the card slides in at {#rule}, and the reshuffle happens at {#any} (the order is swapped).
Words: −9.

### L2. S06 P3: "crossings don't matter, only lengths" is cryptic
> Seven dots, {#count} eleven sticks, and where sticks cross, there's no dot.

Words: +1.

### L3. S06 P5: "must match the bottom" should say "the bottom tip"
> Both top tips must match the bottom tip, so {#same} they match each other.

Words: +1.

### L4. S10 P6: "five hundred and nine" has no noun
By ear, "found one with just five hundred and nine, still the smallest known" drops the unit. Change it to "five hundred and nine dots". Words: +1.

### L5. S02 P6: the scoreboard resets without comment (optional)
In S01 the bar lit 5, 6 and 7. In S02 it reappears fully open. A viewer may wonder why it went backwards. The word "scoreboard" is also first spoken only in S10.
> So what's the fewest colors {#board} that respect every ring at once? Let's keep score, starting from scratch.

Words: +6 (fits the budget if M10's cut is taken).

### L6. S10 P5: no reason is given for shrinking a trap that already works (optional)
"...teamed up online to shrink the trap, making it easier to check." Words: +5. Only add this if the budget allows.

### L7. S11 P3: "ordinary polygon patches" (optional)
Most adults know "polygon". "Any patchwork of polygons provably needs all seven" reads slightly better. Words: +2.

### Not an issue (leave as is)
- **S09 P1**, "He *was* a biologist": the past tense is intentional (fact sheet §7.1 sensitivity note).
- **S06 P3**, "Pause and try, if you like" with a 0.9 s pause: this is fine. Viewers who want to try will pause the video.

---

## What already works (do not touch)
- S02 P1–P2: the three-pairs quiz, then "Just one." This is the best misconception-buster in the video.
- S02 P5: the spinning stick drawing a forbidden ring. It is one image that everything later builds on.
- S03 P4–P5: the stick stands upright inside one band. This is a perfect demonstration of why the plane is harder than the line.
- S04 P2–P4: getting to the triangle through two rings instead of just announcing it.
- S05 P2–P4: "Try a few times. What do you notice? They always match." followed by the leftover argument. This is textbook-clear without sounding like a textbook.
- S05 P5: "No problem yet: … one point seven three units apart." It pre-empts the exact objection a viewer would raise.
- S06 P5: "That's not bad luck. It's the diamond rule, twice." This is the generalization moment.
- S10 P2: "fix a few colors, follow the forced ones, back up at dead ends" is the viewer's own method, applied by a computer.
- S11 P5–P7: the ending returns to the line, the floor, and the box of paints.

---

## Word budget (spoken words, bookmarks excluded)

| change | delta |
|---|---|
| H1 S06 P4 colors | +6 |
| H2 S06 P2 exact one | +2 |
| H3 S06 plan line / P7 trim | +13 / −7 |
| H4 S04 P6 dots and sticks | +8 |
| H5 S02 unit size (new paragraph) | +14 |
| H6 cut S01 P5 / define plane in S03 P4 | −17 / +6 |
| H7 S07 P2 twins | +9 |
| H8 S09 P3 / P4 / P5 | +5 / +2 / −3 |
| M1 S08 P4 | 0 |
| M2 S08 P1 | +3 |
| M3 S04 P3 | +2 |
| M4 S03 P2 | +1 |
| M5 S02 P3 | +2 |
| M6 S08 P5–P6 | −1 |
| M7 S11 P2 | −5 |
| M8 S07 P1 | −1 |
| M9 S07 P5 | +2 |
| L1 S05 P5 | −9 |
| L2 / L3 / L4 | +1 / +1 / +1 |
| (drop the "Swiss mathematician" words in S08 P2, keep the on-screen caption: "Hugo Hadwiger helped spread it, so it's called the Hadwiger Nelson problem.") | −3 |
| **Subtotal (all must-fixes, S11 P4 untouched)** | **+32 → 1,472** |
| M10 cut S11 P4 entirely | −31 → **1,441** |
| optional L5 "keep score" | +6 → **1,447** |

All rewritten sentences are 24 words or fewer, contain no symbols, and spell out every number.

