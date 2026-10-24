# AERTHEON style bible

AERTHEON makes calm, beautiful educational explainers on **mathematics, computer science and engineering**, in the spirit
of 3Blue1Brown. Every video must
feel like a sibling of the pilot, *Five, Six, or Seven? The Hadwiger–Nelson Problem* (its full source is in
`$E/reference/hadwiger-nelson/`; the second video, *The Riemann Hypothesis*, is in `reference/riemann-hypothesis/`).
When in doubt, match the pilot.

## Audience and voice
- For curious people who are **not** experts: a smart 16-year-old or an adult who left maths behind. They can follow
  anything that is shown step by step; they cannot follow jargon, skipped steps or "it is easy to see".
- Tone: warm, clear, curious, a little playful. Calm specifics beat hype: "five, six, or seven, and we don't know which"
  beats "nobody on Earth knows!". Never condescending, never filler ("a beautiful pattern comes to the rescue").
- The viewer should feel they discovered it. Pose small questions to them ("Could two colors work?"), give them a pause
  of 1.2–1.3 s, then show the answer. "Pause and try, if you like." is on-brand once per video.

## Shape of a video
Default length **~10 minutes** (9:30–10:30) unless the user asks otherwise. The pilot's arc, which works for most topics:
1. **Hook**: one concrete, visual image (an endless floor, a box of paints, one stick), the question in one sentence,
   and the honest status up front.
2. **The rules / fine print**: what exactly is asked, and the most common misconception busted on screen.
3. **Warm-up**: a simpler case solved completely (the line needs exactly two colours).
4. **Build the argument step by step**, one idea per scene. Name each reusable lemma ("the diamond rule") and reuse the
   name. State the plan before a construction ("force a match, then forbid it"). Say out loud *why* the small case says
   something about the whole problem.
5. **The other side** (a construction, a pattern, the upper bound), with an honest sentence on any subtle point.
6. **The human story**: who asked, the long stall, the breakthrough, how it was checked, who improved it.
7. **Today**: where it stands, why it is hard, what is open.
8. **Callback ending** that returns to the opening image.

One **recurring visual device** tracks the story across the whole video (the pilot's "colors needed" scoreboard
`1 2 3 4 5 6 7 8 …` whose gold window narrows 1 → ≥3 → ≥4 → 4..7 → 5..7). It has a fixed home on screen and a state that
changes only when the narration earns it.

**Short form (under 5 minutes, as the validator counts it):** the budget scales (135–145 words per minute, about one
scene per minute, 1–2 scenes for a 1-minute short, each 25–90 s); the 8-part arc compresses to one line:
hook image + the question (≤ 10 s up to 2 minutes, ≤ ~15 s up to 5) → optional fine print or warm-up in one paragraph →
the one key idea shown step by step → the honest status in one sentence → callback to the opening image. No history
chapter. Everything else stays: one recurring motif, breathing room, every bookmark synced, same palette, fonts, voice
and music.

## Picture
- 1920×1080 at 60 fps, Manim Community, dark background. Tokens (`$E/template/common.py`):

  | token | hex | meaning |
  |---|---|---|
  | `BG` | `#0E1116` | near-black blue background |
  | `INK` | `#ECEFF4` | main text and lines |
  | `DIM` | `#8A93A3` | secondary text, captions |
  | `FAINT` | `#3A4150` | grids, guides, ruled-out things |
  | `NEUTRAL` | `#D5DCE6` | structural lines that are not content colour |
  | `ACCENT` | `#FFD166` | emphasis, key numbers, the motif's highlight |
  | `BAD` | `#FF5C5C` | only for something wrong, broken, contradicted |
  | `GOOD` | `#6BCB77` | only for check marks |
  | `PALETTE` | `#4EA8F5 #F2C14E #EE6BAE #6BCB77 #B084F5 #F29E4C #43D9C8` | content colours: blue, yellow, pink, green, purple, orange, teal, in this order |

- Fonts: Avenir Next for words (`T()`), Palatino for numbers and math-style labels (`N()`). No LaTeX; Unicode in `Text`.
- Text on screen is short labels and titles, never narration sentences. Minimum size ~24 so it reads at 480p.
- Minimal, uncluttered frames; thin rims on dots so they read on any colour; generous negative space.
- Motion is calm, eased and meaningful: progressive builds, highlights, transforms, gentle camera or group scaling.
  One small shake for a contradiction is the only effect.
- Every scene starts and ends on the empty background, so cuts are seamless.
- Faithful content: exact geometry, real data, anything claimed valid really is valid. Viewers pause.

## Sound
- Voice: Kokoro `af_heart` via mlx-audio, speed **0.85** (~181 wpm), one clip per sentence. This is the channel voice;
  never substitute another voice preference (e.g. an audiobook narrator) and never pass `--speed`.
- Breathing room: 0.55 s between sentences, 0.55–1.5 s between paragraphs (from `pause_after`).
- The voice covers the whole video: no animation runs more than 1.6 s without speech, and no voice pause is longer than 1.6 s.
- A soft procedural ambient pad (`tts/music.py`) sits ~25 dB under the voice with sidechain ducking; master at −16 LUFS.
- Deliverables: `videos/<slug>/<name>.mp4` (1080p60), `youtube.md` (`YOUTUBE.md`); in `src/out/`: `<name>_720p_share.mp4` (~25–30 MB), `<name>.srt`,
  `waveform_overview.png`; and three thumbnails in `videos/<slug>/thumbnails/` (`$E/THUMBNAIL.md`).
