# Script format (`videos/<slug>/script/script.json`)

The script is the single source of truth for narration, timing and storyboard. `tools/timeline.py` turns it into audio and
exact timestamps. Scene builders treat each paragraph's `visual` as their spec. `tools/validate_script.py` enforces every
rule below that a machine can check. A script is done when the validator shows zero ERRORs.

Gold standard: `$E/reference/hadwiger-nelson/script/script.json`.

## Shape

```json
{
  "title": "Five, Six, or Seven? The Hadwiger–Nelson Problem",
  "target_minutes": 10,
  "scenes": [
    {
      "id": "S01_Hook",
      "title": "An endless floor and one stick",
      "purpose": "One line: what the viewer understands after this scene.",
      "paragraphs": [
        {
          "sentences": ["There's just one rule.",
                        "{#stick} Drop a stick exactly one unit long anywhere, {#angle} at any angle."],
          "visual": "Concrete storyboard: what is on screen and where, what changes at {#stick} and at {#angle}, what lands in the pause.",
          "pause_after": 1.0
        }
      ]
    }
  ],
  "pron": {"Hadwiger": "/hˈædvɪɡəɹ/", "Jaan": "/jˈɑn/"},
  "pronunciation_notes": ["Human notes on names, years as spoken, intended beats."],
  "facts": [{"claim": "Edward Nelson asked the question in 1950, aged eighteen.", "source": "https://… ; https://…"}]
}
```

`target_minutes` is the requested length (`1`, `3`, `10`), a number: the validator budgets words and scenes from it when
`--minutes` is not given.

## Budget (default 10 minutes; scales with `target_minutes`)
- 135–145 spoken words per minute of video: **1,350–1,450 words** for 10 minutes (bookmarks excluded).
- About one scene per minute (9–11 for 10 minutes), each **35–90 s** (≈ 90–220 words; 25–90 s for videos under 5 minutes, e.g. two scenes for a 1-minute short).
- Scene ids: `S` + two digits + `_` + CamelCase (`S01_Hook`, `S06_Spindle`). The id is also the Manim class name.
- 2–7 paragraphs per scene. 1–4 sentences per paragraph. A paragraph is one coherent visual beat.
- The validator's length estimate runs ~15 s short (real pauses are longer: RH estimated 9:24.6, real 9:40.3), so an
  estimate just under the target is fine.
- Hook ≤ 45 s: name the question within ~20–25 s (the pilot's hook is 38 s; RH's 63.5 s was too long). This is for
  10-minute videos; shorter videos: see `STYLE.md` short form.

## Spoken text (`sentences`)
- One sentence per string: two sentences in one string get no 0.55 s gap between them.
- Spoken English, at most 24 words per sentence. Short punchlines rush in Kokoro: give them `pause_after` ≥ 0.9 or merge them
  into a slightly longer sentence.
- Only letters and ordinary punctuation. Spell out every number and year as it is spoken ("nineteen fifty",
  "fifteen hundred and eighty-one", "one point seven three"). Write "one unit", never "1u". No parentheses, symbols,
  abbreviations, em or en dashes.
- Names go in plainly. If Kokoro or Whisper mangles a name, add it to `"pron"` as `"Name": "/ipa/"`; `timeline.py`
  substitutes it at synthesis time and prints a WARN for every sentence Whisper hears differently from the script. That
  Whisper is primed with the sentence and misses most errors (it passed "Hadviger", "Jan Parts"); `tools/pron_check.py`
  is the real check. Keys are case-sensitive whole words: a sentence-initial "Zeta" needs its own key besides "zeta".
- Kokoro rushes long spoken formulas (213–231 wpm): split them into short sentences.
- Pronouns need an unmistakable referent when heard once. Name colours and objects that are on screen.

## Clarity (what the critics flag)
- Define each instrument (graph, dial, strip) in words the first time it appears.
- One name per concept, used every time. Never say a technical word before it is introduced.
- One meaning per word per sentence (not "zero" as a number and as a zeta zero together).

## Bookmarks (`{#name}`)
- Put `{#name}` immediately **before** the word at which a visual event must happen: "Now draw a triangle {#tri} whose sides…".
  Never at the end of a sentence.
- Lowercase snake_case letters only (no digits: `first_ring`, `twenty_ten`), unique within the scene, 1–5 per paragraph.
- Automatic marks exist too and cannot be used as names: `p3` (paragraph 3 starts), `p3_end`, `p3s2` (sentence 2 of
  paragraph 3 starts), `p3s2_end`, `end`.
- Space them out: each bookmark needs time for its visual (≥ ~1 s before the next one) and nothing may freeze for more than 5 s
  of speech, so add a bookmark wherever a long sentence would otherwise show a still picture. The validator WARNs on
  estimated gaps < 0.95 s within one sentence and on > 5 s of speech without any mark (bookmark or automatic sentence mark).
  Rapid one-word count/list beats are pilot style and fine: HN S01 "{#five} five, {#six} six, or {#seven} seven" puts each
  number on screen as it is spoken (the validator skips marks one or two words apart in one sentence).

## Storyboard (`visual`)
The animator builds exactly this, so make it concrete: positions, colours (by token: `PALETTE` names, `ACCENT`, `BAD`, `GOOD`,
`NEUTRAL`, `DIM`), sizes, what happens at each `{#bookmark}` (mention every bookmark of the paragraph), and what lands during
the pause. Every visual is animatable in Manim without LaTeX. Geometry and data are faithful: give exact values or name the
`topic.py` constructor. Say explicitly when something is only an illustration. Motion that needs more than ~1.5 s without
speech gets its own narration instead.

## `pause_after`
Seconds of silence after the paragraph. Range 0.5–1.5 (up to 2.0 on the final paragraph of the video); the engine clamps it to 0.55–1.5 between paragraphs and to 0.5–0.9 after
the last paragraph of a scene (2.0 for the video's final paragraph). Use 0.6–0.9 normally, 1.0–1.4 after a reveal or a question (never above 1.4 mid-video: with the clip's own trailing
silence, 1.5 measures ~1.62 s and fails final QA's 1.6 s gap limit; to lengthen a short scene, spread +0.1 s over several
pauses)
to the viewer. Because of the clamp, never plan a reveal in a scene's closing pause; the validator WARNs on
`pause_after` > 0.9 on a scene's last paragraph (except the video's final one).

## `facts`
Every factual claim in the narration (names, dates, numbers, results, "still open") with a source URL, primary or high-trust.
Mathematical claims may cite a runnable check in `script/checks/`. Low-confidence facts stay out of the narration.
