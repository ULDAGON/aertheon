export const meta = {
  name: 'aertheon-script',
  description: 'Research, draft (3 angles), judge, synthesize, adversarially review and finalize an AERTHEON explainer script',
  whenToUse: 'Step 3 of the engine PIPELINE.md: after new_video.sh scaffolded videos/<slug>/src/',
  phases: [
    { title: 'Research', detail: 'facts with sources + pedagogy/intuitions' },
    { title: 'Draft', detail: 'three competing full scripts from different angles' },
    { title: 'Judge', detail: 'two judges with different lenses score all drafts' },
    { title: 'Synthesize', detail: 'final script from winner + grafts' },
    { title: 'Verify', detail: 'fact-check, lay-viewer critic, TTS/pacing critic' },
    { title: 'Finalize', detail: 'apply all fixes, validate, write script/script.json' },
  ],
}

// args: { root: '/abs/videos/<slug>/src', engine: '/abs/path/to/engine', topic: 'one line', minutes: 10,
//         content: 'topic-specific must-cover list, fact targets, optional on-ramps, ending idea (from brief.md, PIPELINE.md step 2)' }
const ROOT = args.root
const SD = ROOT + '/script'
const ENGINE = args.engine || (() => { throw new Error('pass args.engine (the engine repository root)') })()
const MIN = Number(args.minutes) || 10
const WORDS = `${Math.round(135 * MIN)}–${Math.round(145 * MIN)}`
const SCENES_N = `${Math.max(1, Math.round(MIN * 0.9))}–${Math.max(2, Math.round(MIN * 1.1))}`
const SHORT = MIN < 5   // validate_script.py: 25–90 s scenes and the STYLE.md short-form arc under 5 minutes
const SCENE_S = `${SHORT ? 25 : 35}–90 s`
const SHORT_ARC = SHORT ? `
SHORT FORM (STYLE.md, "Short form"): compressed arc: hook image + the question in ≤ ${MIN <= 2 ? '10' : '~15'} s → optional fine print or warm-up in one paragraph → the one key idea shown step by step → the honest status in one sentence → callback to the opening image. No history chapter.
` : ''

const BRIEF = `
PROJECT: a ~${MIN} minute AERTHEON educational explainer video: ${args.topic}.
In the spirit of 3Blue1Brown, animated with Manim Community, narrated by a local TTS voice (Kokoro "af_heart" at speed 0.85, ~181 words/min).
Audience: curious people who are NOT experts in the field. Tone: warm, clear, curious, a little playful; calm specifics over hype; never condescending.
Project root: ${ROOT}. Channel style bible: ${ENGINE}/STYLE.md (read it). Script format spec: ${ENGINE}/SCRIPT_FORMAT.md (read it; follow it exactly).
The full brief is ${ROOT}/brief.md: if it exists, read it completely; it is the authoritative content list (CONTENT below is its summary).
Gold-standard finished script for tone, storyboard detail and bookmark density: ${ENGINE}/reference/hadwiger-nelson/script/script.json (skim 2–3 scenes; a second example: ${ENGINE}/reference/riemann-hypothesis/script/).

HARD CONSTRAINTS (breaking these ruins a video):
- Every visual beat is covered by narration. No silent title cards, no silent montages, no visual sequence needing more than ~1.5 s without speech.
- Breathing room: the engine inserts 0.55 s between sentences and each paragraph's pause_after (0.6–1.4 s) is where the visual payoff lands.
  Longer pauses (1.1–1.4) only after big reveals and questions to the viewer.

LENGTH: ${WORDS} spoken words total (bookmarks excluded). ${SCENES_N} scenes, each ${SCENE_S} (≈ ${SHORT ? 65 : 90}–220 words). Set "target_minutes": ${MIN} in the JSON.
${SHORT_ARC}
CONTENT (all facts must be verified):
${args.content}

Shared visual language: one recurring visual device that tracks the video's progress (the pilot used a "colors needed" scoreboard whose window narrows);
a seven-color content palette; storyboards animatable in Manim WITHOUT LaTeX; content mathematically/factually faithful.
A satisfying ending that returns to the opening image.
`

const SCRIPT_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    total_words: { type: 'integer' },
    scene_words: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, words: { type: 'integer' } }, required: ['id', 'words'] } },
    summary: { type: 'string' },
  },
  required: ['path', 'total_words', 'scene_words', 'summary'],
}

const WEB = 'Use web search/fetch (load WebSearch and WebFetch via ToolSearch first) and prefer primary or high-trust sources (papers, arXiv, Quanta Magazine, Wikipedia with its cited sources, university pages, official data).'
const VALIDATE = `Validate with: python3 ${ROOT}/tools/validate_script.py <file> --minutes ${MIN}  (fix every ERROR; address WARNs).`

phase('Research')
await parallel([
  () => agent(`${BRIEF}\n\nYOUR TASK: build a verified FACT SHEET for this video. ${WEB}
Cover every fact the content list needs: names, dates, numbers, who showed what and how, what is still open, and exact parameters of any construction the
animation must draw faithfully. Where a claim is mathematical, write a small runnable check in ${SD}/checks/<name>_check.py and run it.
Write the sheet to ${SD}/research_facts.md. Start with a quick-reference table: item | value | spoken form ("nineteen fifty").
Each fact: statement, exact numbers, source URL, confidence (high/medium/low; low = never narrate), and common misconceptions to avoid.
Return a short summary of the most important facts and anything surprising or commonly misstated.`, { label: 'research:facts', phase: 'Research' }),
  () => agent(`${BRIEF}\n\nYOUR TASK: PEDAGOGY research. ${WEB}
Find how the best explainers teach this topic (videos, Quanta-style articles, blog posts, lecture notes).
Collect: the most effective intuitions, analogies and "aha" framings for lay viewers; the usual points of confusion; visual ideas that make each step obvious;
good hooks and endings; the single biggest conceptual gap explainers tend to leave. Start the file with a numbered TL;DR for the script writer.
Write findings to ${SD}/research_pedagogy.md. Return a short summary.`, { label: 'research:pedagogy', phase: 'Research' }),
])
log('research done')

phase('Draft')
const ANGLES = [
  { key: 'A_story', desc: 'STORY-DRIVEN: the history and the people are the spine (the question, the struggle, the breakthrough, what is open), with each idea introduced exactly when the story needs it.' },
  { key: 'B_puzzle', desc: 'HANDS-ON PUZZLE: the viewer plays along. Each scene poses a small challenge ("could it work with less? try it"), lets the viewer fail, then reveals why. History is light seasoning.' },
  { key: 'C_visual', desc: 'VISUAL INTUITION (3Blue1Brown style): built on recurring visual devices and elegant reframings (a simpler warm-up case, a change of viewpoint) that make the viewer feel they discovered it.' },
]
const CLARITY = `CLARITY RULES (from the critics of past videos): ${SHORT ? `hook image + question in ≤ ${MIN <= 2 ? '10' : '~15'} s (short form)` : "name the question within ~20–25 s and keep the hook ≤45 s (the pilot's ran 38 s)"};
define each instrument in words at its first appearance; one name per concept; never say a technical word before it is introduced;
never use one word in two senses in one sentence (e.g. "zero" as a number and as a zeta zero); split long spoken formulas (the voice rushes them);
one sentence per string (two sentences in one string get no 0.55 s gap).`
const drafts = await parallel(ANGLES.map(a => () => agent(`${BRIEF}\n\nRead the research first: ${SD}/research_facts.md and ${SD}/research_pedagogy.md.
YOUR TASK: write a COMPLETE script draft with this angle: ${a.desc}
Follow the script format exactly and write it as JSON to ${SD}/draft_${a.key}.json. ${VALIDATE}
${CLARITY}
Make the central argument airtight and easy to follow by ear. Storyboards must be concrete and synced to bookmarks. Return path, word counts and a 3-sentence summary of what makes this draft good.`,
  { label: `draft:${a.key}`, phase: 'Draft', schema: SCRIPT_SCHEMA })))
const draftPaths = drafts.filter(Boolean).map(d => d.path)
log(`drafts: ${draftPaths.join(', ')}`)

phase('Judge')
const JUDGE_SCHEMA = {
  type: 'object',
  properties: {
    ranking: { type: 'array', items: { type: 'string' } },
    scores: { type: 'array', items: { type: 'object', properties: { draft: { type: 'string' }, score: { type: 'number' }, strengths: { type: 'string' }, weaknesses: { type: 'string' } }, required: ['draft', 'score', 'strengths', 'weaknesses'] } },
    grafts: { type: 'array', items: { type: 'string' } },
  },
  required: ['ranking', 'scores', 'grafts'],
}
const LENSES = [
  'LAY VIEWER: you are a smart 16-year-old / adult with no background in this field. Judge clarity (could you follow every step, especially the central argument?), engagement (would you keep watching to the end?), the hook and the ending.',
  'EXPERT PRODUCER: judge accuracy and honesty, pacing (word counts per scene, rhythm, pauses, no visual beat without narration), and animatability of the storyboards in Manim (concrete, faithful, bookmarks well placed).',
]
const judgements = await parallel(LENSES.map((lens, i) => () => agent(`${BRIEF}\n\nYou are judge ${i + 1}. LENS: ${lens}
Read these drafts: ${draftPaths.join(', ')}. Also skim ${SD}/research_facts.md.
Score each draft 0–10, rank them, and list the specific passages/ideas from each draft that the final script should graft in (quote them).`,
  { label: `judge:${i + 1}`, phase: 'Judge', schema: JUDGE_SCHEMA })))

phase('Synthesize')
await agent(`${BRIEF}\n\nDrafts: ${draftPaths.join(', ')}. Research: ${SD}/research_facts.md, ${SD}/research_pedagogy.md.
Judges' verdicts (JSON): ${JSON.stringify(judgements.filter(Boolean))}
YOUR TASK: write the FINAL script. Start from the top-ranked draft and graft in the best ideas the judges listed, fixing every weakness they named.
Keep one consistent voice. ${CLARITY}
Follow the script format exactly. Write it to ${SD}/script_synth.json. ${VALIDATE}`,
  { label: 'synthesize', phase: 'Synthesize', schema: SCRIPT_SCHEMA })

phase('Verify')
const CRITICS = [
  { key: 'facts', prompt: `ADVERSARIAL FACT-CHECK. ${WEB} Check EVERY factual claim in the narration (names, dates, numbers, who proved/found what, how, what is still open). Also check every mathematical or technical statement and every storyboard that claims something is valid/exact (re-run or write checks in ${SD}/checks/). Assume nothing; try to refute each claim. List each problem with the exact sentence, what is wrong, and the corrected wording (spoken style, numbers spelled out). Add a section of visual/animator notes on faithfulness.` },
  { key: 'clarity', prompt: `LAY-VIEWER COMPREHENSION CRITIC. Read it as someone with no background, listening once at normal speed. Flag jargon, logical leaps, missing definitions, unclear referents ("it", "this"), steps that need a visual the storyboard does not provide, places where attention would drop, and anything that sounds like a textbook. Give concrete rewrites with their word-count delta, ordered HIGH / MEDIUM / LOW.` },
  { key: 'pacing', prompt: `TTS & PACING & ANIMATION CRITIC. MEASURE, do not estimate: S=${ROOT}/out/_scratch/pacing; mkdir -p $S/tools $S/script; cp ${ROOT}/tools/timeline.py $S/tools/; ${ROOT}/tts/.venv/bin/python $S/tools/timeline.py --script ${SD}/script_synth.json  (the copy writes audio/timeline into $S only) to get real sentence and bookmark times from $S/timeline/*.json. Check: total length vs target; per-scene length ${SCENE_S}; sentences natural when read by the TTS voice (no tongue-twisters; names that Whisper mishears need a "pron" entry); bookmarks placed right before the word where the event happens and not crammed; every paragraph's storyboard fits the measured time between its bookmarks (no beat that would spill into silence); no picture frozen > 5 s while talking; pause_after values sensible. Give concrete fixes (BLOCKER / HIGH / MEDIUM / LOW).` },
]
await parallel(CRITICS.map(c => () => agent(`${BRIEF}\n\nScript to review: ${SD}/script_synth.json (facts sheet: ${SD}/research_facts.md).\nYOUR ROLE: ${c.prompt}\nWrite your review to ${SD}/review_${c.key}.md and return it as text (issues ordered by severity, each with a concrete fix).`,
  { label: `verify:${c.key}`, phase: 'Verify' })))

phase('Finalize')
const final = await agent(`${BRIEF}\n\nScript: ${SD}/script_synth.json. Reviews: ${SD}/review_facts.md, ${SD}/review_clarity.md, ${SD}/review_pacing.md (read all three fully).
YOUR TASK: produce the final script by applying every valid fix from the reviews (fact errors are mandatory; if two reviews conflict, prefer accuracy, then clarity, then budget).
Keep the script format exactly. Never hand-edit the JSON: write ${SD}/build_final.py that loads script_synth.json, applies each fix through small helpers
that assert their target exists (e.g. rep(obj, key, old, new) asserts old in obj[key]; sents(scene, i, [...]) replaces a paragraph's sentences),
and writes ${SD}/script.json; then run it with python3. ${VALIDATE} Fix build_final.py and repeat until zero ERRORs. Print the per-scene word counts.
Also write ${SD}/CHANGELOG.md: the result line (scenes, words, estimated runtime), a table per review of what you applied and what you rejected and why,
and a section "Changes that must be made outside the script" (engine settings, pron entries) if any.`,
  { label: 'finalize', phase: 'Finalize', schema: SCRIPT_SCHEMA })
return { final }
