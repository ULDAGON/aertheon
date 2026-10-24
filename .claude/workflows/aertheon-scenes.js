export const meta = {
  name: 'aertheon-scenes',
  description: 'Build every timeline-synced Manim scene of an AERTHEON video, review each with two lenses, fix, re-review, apply shared-helper requests once, a continuity pass, then verify every scene',
  whenToUse: 'Step 6 of the engine PIPELINE.md: after timeline/*.json exist and SCENE_GUIDE.md "This video" is filled in',
  phases: [
    { title: 'Build', detail: 'one builder per scene, QA loop until clean' },
    { title: 'Review', detail: 'two independent critics per scene (teaching lens, technical lens)' },
    { title: 'Fix', detail: 'apply review findings, re-run QA' },
    { title: 'Shared', detail: 'one owner applies all shared-helper requests, re-renders every scene' },
    { title: 'Continuity', detail: 'cross-scene consistency review + targeted fixes (shared files: one owner)' },
    { title: 'Verify', detail: 'every scene re-rendered, QA and last unresolved review issues re-checked' },
  ],
}

// args: { root: '/abs/videos/<slug>/src', engine: '/abs/path/to/engine', topic: 'one line', scenes: [{id: 'S01_Hook', file: 's01_hook.py'}, ...],
//         motif: 'the recurring device and its state progression across scenes, e.g. "scoreboard: 1 -> at least 3 -> 4..7 -> 5..7"' }
const ROOT = args.root
const ENGINE = args.engine || (() => { throw new Error('pass args.engine (the engine repository root)') })()
const SCENES = args.scenes

const BUILD_SCHEMA = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    duration_s: { type: 'number' },
    qa_errors: { type: 'integer' },
    qa_warnings: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    weaknesses: { type: 'string' },
    shared_requests: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' }, change: { type: 'string' }, reason: { type: 'string' },
    }, required: ['file', 'change', 'reason'] } },
  },
  required: ['file', 'duration_s', 'qa_errors', 'qa_warnings', 'summary', 'weaknesses', 'shared_requests'],
}
const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fix'] },
    issues: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
      where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' },
    }, required: ['severity', 'where', 'problem', 'fix'] } },
    praise: { type: 'string' },
  },
  required: ['verdict', 'issues'],
}

const COMMON = `Project root: ${ROOT}. This is an AERTHEON 3Blue1Brown-style explainer (${args.topic}) for NON-expert viewers, made with Manim Community.
FIRST read fully: ${ROOT}/SCENE_GUIDE.md (rules, API, QA workflow, "This video" section), ${ROOT}/common.py, ${ROOT}/topic.py.
The channel's finished scenes (the style to match) are in ${ENGINE}/reference/hadwiger-nelson/scenes/: read only, never render or write there.
The script is ${ROOT}/script/script.json; the narration timing for every scene is in ${ROOT}/timeline/<SceneId>.json (marks, sentences with word times).
The voice is final and fixed. Animation without voice, or a picture that does not follow the words, ruins a video, so voice/picture sync and pacing are the top priority.`

const OWN = `Edit only your scene file (and new scene-local helpers next to it). Shared files (common.py, topic.py, anything several scenes import) have ONE owner: never edit them; return each change you need there in shared_requests ({file, change, reason}; empty list if none) and work around it locally meanwhile.
If a render looks stale (closures over numpy/scipy, ValueTrackers, always_redraw), use NOCACHE=1 tools/render.sh <id> l; never delete caches or folders (no rm).`

function neighbors(i) {
  const prev = i > 0 ? SCENES[i - 1].id : null
  const next = i < SCENES.length - 1 ? SCENES[i + 1].id : null
  return `Neighbouring scenes (for continuity; they are being built in parallel by others): previous = ${prev || 'none (this opens the video)'}, next = ${next || 'none (this ends the video)'}. Read their storyboards in script.json so your first/last beats hand over smoothly (every scene starts and ends on the empty background; the recurring motif's state must continue the story: ${args.motif}).`
}

const buildPrompt = (s, i) => `${COMMON}
YOUR SCENE: ${s.id}. Write ${ROOT}/scenes/${s.file} defining class ${s.id}(TimedScene).
Its storyboard = the "visual" of each paragraph of scene ${s.id} in script.json, synchronized to its {#bookmarks} (times in timeline/${s.id}.json). Realize the teaching intent of every paragraph; you may improve the storyboard where it helps clarity, but the picture must always show what the words say at that moment.
${neighbors(i)}
${OWN}
Iterate with \`tools/render.sh ${s.id} l\` and LOOK at out/qa/${s.id}.timeline.png, .marks.png and .sheet.png every round (use the Read tool on the PNGs). Stop only when QA shows 0 errors, warnings are fixed or justified, and the scene is genuinely clear and beautiful at 480p.
Return the schema fields (qa_warnings = remaining WARN lines verbatim).`

const LENSES = [
  { key: 'teach', text: `TEACHING / LAY-VIEWER lens. Watch it as a smart viewer with no background in the field: at every beat, would you understand what you are looking at and why it matters? Is the visual too busy, too small, too fast, ambiguous, or missing the key moment the words describe? Is the storytelling beautiful and calm (3Blue1Brown quality)? Are labels minimal and readable?` },
  { key: 'tech', text: `TECHNICAL lens. (1) Sync: at every bookmark (marks.png shows the frame 0.9 s after it, labelled with the words just spoken) does the picture show exactly what the words say? Any beat early/late? (2) Pacing: QA report errors/warnings, motion while silent, frozen picture while talking (timeline.png). (3) Faithfulness: geometry/data exact (use topic.py values), anything claimed valid is valid and anything claimed broken is broken, counts right, motif state right. (4) Guide compliance: colour semantics (PALETTE content, NEUTRAL structure, BAD only for wrong, GOOD only for checks), fonts, safe area, no overlap/clipping, starts and ends on empty background.` },
]

const reviewPrompt = (s, lens, round) => `${COMMON}
You are an independent, demanding REVIEWER (round ${round}) for scene ${s.id} (${ROOT}/scenes/${s.file}). You only read: leave every project file untouched and leave tools/render.sh to the agent that owns the render.
Review the existing outputs: out/qa/${s.id}.report.txt, out/qa/${s.id}.timeline.png, out/qa/${s.id}.marks.png, out/qa/${s.id}.sheet.png (Read the PNGs), the scene code, the scene's paragraphs in script/script.json and timeline/${s.id}.json.
For extra frames: ffmpeg -ss <t> -i out/preview/${s.id}_480p15.mp4 -frames:v 1 out/review/${s.id}_${lens.key}/f_<t>.png (mkdir it first), and Read them. Check at least the moments the words describe most visually.
LENS: ${lens.text}
Verdict "pass" only if there is no critical or major issue. Each issue: severity, where (bookmark name and/or time), the problem, and a concrete fix the builder can apply.`

const fixPrompt = (s, issues, round) => `${COMMON}
You own scene ${s.id}: ${ROOT}/scenes/${s.file} (class ${s.id}). Reviewers found these issues (round ${round}):
${JSON.stringify(issues, null, 1)}
Apply every critical and major fix, and every minor fix that improves the scene without risk. If you reject one, say why in "weaknesses".
${OWN}
Then iterate with \`tools/render.sh ${s.id} l\`, LOOK at the three QA PNGs, until QA has 0 errors and the scene is clearly better. Return the schema fields.`

const results = await pipeline(
  SCENES,
  (s, _o, i) => agent(buildPrompt(s, i), { label: `build:${s.id}`, phase: 'Build', schema: BUILD_SCHEMA }),
  async (built, s) => {
    let last = built
    const history = []
    const requests = []
    const take = r => { if (r && r.shared_requests) requests.push(...r.shared_requests.map(q => ({ ...q, scene: s.id }))) }
    take(built)
    let lastVerdict = 'pass'
    let openIssues = []
    for (let round = 1; round <= 2; round++) {
      const lenses = round === 1 ? LENSES : [{ key: 'final', text: LENSES[0].text + ' ALSO: ' + LENSES[1].text }]
      const reviews = (await parallel(lenses.map(l => () =>
        agent(reviewPrompt(s, l, round), { label: `review${round}:${s.id}:${l.key}`, phase: 'Review', schema: REVIEW_SCHEMA })))).filter(Boolean)
      const issues = reviews.flatMap(r => r.issues)
      const blocking = issues.filter(x => x.severity !== 'minor')
      if (!reviews.length) blocking.push({ severity: 'major', where: 'all', problem: 'no reviewer returned in this round', fix: 'full review with both lenses (teaching + technical)' })
      history.push({ round, verdicts: reviews.map(r => r.verdict), issues: issues.length, blocking: blocking.length })
      if (reviews.length && reviews.every(r => r.verdict === 'pass') && blocking.length === 0) {
        lastVerdict = 'pass'
        openIssues = []
        if (issues.length && round === 1) {
          const r = await agent(fixPrompt(s, issues, round), { label: `polish:${s.id}`, phase: 'Fix', schema: BUILD_SCHEMA })
          take(r)
          last = r || last
        }
        break
      }
      lastVerdict = 'fix'
      openIssues = blocking
      const r = await agent(fixPrompt(s, issues, round), { label: `fix${round}:${s.id}`, phase: 'Fix', schema: BUILD_SCHEMA })
      take(r)
      last = r || last
    }
    log(`${s.id}: ${JSON.stringify(history)}`)
    return { id: s.id, file: s.file, final: last, history, requests, lastVerdict, openIssues }
  },
)

const done = results.filter(Boolean)

// One owner for every shared file: dedupe requests, apply them once, re-render every scene, repair what broke.
const SHARED_SCHEMA = {
  type: 'object',
  properties: {
    applied: { type: 'array', items: { type: 'string' } },
    rejected: { type: 'array', items: { type: 'object', properties: { change: { type: 'string' }, why: { type: 'string' } }, required: ['change', 'why'] } },
    scenes: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, qa_errors: { type: 'integer' }, note: { type: 'string' },
    }, required: ['id', 'qa_errors', 'note'] } },
    summary: { type: 'string' },
  },
  required: ['applied', 'rejected', 'scenes', 'summary'],
}
function dedupe(reqs) {
  const m = new Map()
  for (const q of reqs) {
    const k = `${(q.file || '').trim()}|${(q.change || '').trim().toLowerCase().replace(/\s+/g, ' ')}`
    const e = m.get(k)
    if (e) { if (!e.scenes.includes(q.scene)) e.scenes.push(q.scene); if (q.reason && !e.reasons.includes(q.reason)) e.reasons.push(q.reason) }
    else m.set(k, { file: q.file, change: q.change, scenes: [q.scene], reasons: q.reason ? [q.reason] : [] })
  }
  return [...m.values()]
}
const sharedPrompt = (items, what) => `${COMMON}
You are the SINGLE OWNER of the shared files (common.py, topic.py, and anything several scenes import). Nobody else edits them; the scene agents are finished.
Apply these ${what} (JSON; "scenes" = who asked or is affected):
${JSON.stringify(items, null, 1)}
Merge duplicates and overlapping requests into one coherent change per helper. Apply each sound one; reject unsound ones with a reason. Never change the channel's style tokens in common.py (palette, fonts, sizes, timing constants); topic helpers, motif classes, layouts and constants in topic.py are yours to fix. Run .venv/bin/python topic.py after editing it (self-checks).
Then re-render EVERY scene, one at a time: ${SCENES.map(s => s.id).join(', ')} with \`tools/render.sh <id> l\` (NOCACHE=1 if a render looks stale; never delete caches or folders, no rm). For each, read out/qa/<id>.report.txt and LOOK at out/qa/<id>.sheet.png (Read the PNG). If your change broke a scene (QA errors, overlap, clipping, motif wrong, layout off), fix it with the smallest edit to that scene file and re-render until QA has 0 errors.
Return what you applied, what you rejected and why, and every scene's final qa_errors with a one-line note.`
async function applyShared(reqs, label, ph) {
  const items = dedupe(reqs)
  if (!items.length) return null
  log(`${label}: ${items.length} shared change(s) from ${reqs.length} request(s)`)
  return agent(sharedPrompt(items, 'shared-helper requests'), { label, phase: ph, schema: SHARED_SCHEMA })
}

phase('Shared')
const shared = await applyShared(done.flatMap(r => r.requests || []), 'shared', 'Shared')

phase('Continuity')
const CONT_SCHEMA = {
  type: 'object',
  properties: {
    per_scene: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      issues: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' }, shared_file: { type: 'string' } }, required: ['severity', 'problem', 'fix', 'shared_file'] } },
    }, required: ['id', 'issues'] } },
    overall: { type: 'string' },
  },
  required: ['per_scene', 'overall'],
}
const cont = await agent(`${COMMON}
You are the CONTINUITY reviewer for the whole video. All ${SCENES.length} scenes are built: ${SCENES.map(s => s.id + ' -> scenes/' + s.file).join(', ')}.
You only read: leave project files untouched and never run tools/render.sh. Look at every scene's out/qa/<id>.sheet.png and .marks.png (Read the PNGs), the first and last seconds of each out/preview/<id>_480p15.mp4 (extract frames with ffmpeg into out/review/_continuity/), and skim the code.
Check across scenes: consistent visual language (dot sizes, line widths/colours, fonts and text sizes, palette semantics, where the recurring motif sits and how it looks), the motif's state progression (${args.motif}) never contradicts the narration, recurring objects look the same when they recur, every scene starts and ends on the empty background, and the visual storytelling feels like ONE video. Report per-scene issues with concrete fixes (only real problems; empty list if a scene is fine). For each issue set shared_file to the shared file the fix must change (topic.py, common.py, ...) or "" when editing the scene file alone fixes it.`,
  { label: 'continuity', phase: 'Continuity', schema: CONT_SCHEMA })

const perScene = (cont && cont.per_scene || []).filter(p => p.issues && p.issues.length && SCENES.some(x => x.id === p.id))
// Fixes that touch a shared file go to ONE owner first (it re-renders every scene); scene-local fixes then run in parallel.
const sharedCont = perScene.flatMap(p => p.issues.filter(x => (x.shared_file || '').trim()).map(x => ({ file: x.shared_file, change: x.fix, reason: `${x.severity}: ${x.problem}`, scene: p.id })))
const contShared = sharedCont.length
  ? await agent(sharedPrompt(dedupe(sharedCont), 'continuity fixes to shared files'), { label: 'contfix:shared', phase: 'Continuity', schema: SHARED_SCHEMA })
  : null
const localCont = perScene.map(p => ({ id: p.id, issues: p.issues.filter(x => !(x.shared_file || '').trim()) })).filter(p => p.issues.length)
const contFixes = await parallel(localCont.map(p => () => {
  const s = SCENES.find(x => x.id === p.id)
  return agent(fixPrompt(s, p.issues, 'continuity'), { label: `contfix:${s.id}`, phase: 'Continuity', schema: BUILD_SCHEMA })
    .then(r => ({ id: s.id, r }))
}))
const late = await applyShared(contFixes.filter(Boolean).flatMap(x => (x.r && x.r.shared_requests || []).map(q => ({ ...q, scene: x.id }))), 'contfix:shared2', 'Continuity')

phase('Verify')
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    qa_errors: { type: 'integer' },
    qa_warnings: { type: 'array', items: { type: 'string' } },
    resolved: { type: 'array', items: { type: 'string' } },
    unresolved: { type: 'array', items: { type: 'object', properties: { problem: { type: 'string' }, why: { type: 'string' } }, required: ['problem', 'why'] } },
    changes: { type: 'string' },
    shared_requests: BUILD_SCHEMA.properties.shared_requests,
  },
  required: ['qa_errors', 'qa_warnings', 'resolved', 'unresolved', 'changes', 'shared_requests'],
}
const contIssues = id => (perScene.find(p => p.id === id) || { issues: [] }).issues
const verifyPrompt = (s, r) => {
  const open = r && r.lastVerdict === 'fix' ? r.openIssues || [] : []
  const ci = contIssues(s.id)
  return `${COMMON}
You VERIFY scene ${s.id}: ${ROOT}/scenes/${s.file} (class ${s.id}). Shared files may have changed since it was last reviewed.
Re-render it: \`tools/render.sh ${s.id} l\` (NOCACHE=1 if a render looks stale), read out/qa/${s.id}.report.txt and LOOK at out/qa/${s.id}.timeline.png, .marks.png and .sheet.png (Read the PNGs). For extra frames: ffmpeg -y -ss <t> -i out/preview/${s.id}_480p15.mp4 -frames:v 1 out/review/${s.id}_verify/f_<t>.png (mkdir it first).
${open.length ? `The last review round ended in "fix" and its fixes were never re-reviewed. Check each of these blocking issues against the new render; it is resolved only if you can see it is:
${JSON.stringify(open, null, 1)}` : !r ? 'Its build/review did not complete: review it fully with both lenses before fixing. TEACHING: ' + LENSES[0].text + ' TECHNICAL: ' + LENSES[1].text
  : r.lastVerdict === 'fix' ? 'Its last review round asked for fixes but raised no blocking issue: confirm its fixes held.' : 'Its last review round passed.'}
${ci.length ? `Continuity issues raised for this scene (confirm the fixes held):
${JSON.stringify(ci, null, 1)}` : ''}
Apply small, safe fixes yourself (sync, holds, sizes, overlaps, QA errors) and re-render until QA has 0 errors; do not redesign the scene. ${OWN}
Return QA results, the issues you confirmed resolved, those still open with why, and what you changed.`
}
const verified = await parallel(SCENES.map(s => () =>
  agent(verifyPrompt(s, done.find(r => r.id === s.id)), { label: `verify:${s.id}`, phase: 'Verify', schema: VERIFY_SCHEMA })
    .then(v => ({ id: s.id, v }))))
const leftover = dedupe(verified.filter(Boolean).flatMap(x => (x.v && x.v.shared_requests || []).map(q => ({ ...q, scene: x.id }))))
if (leftover.length) log(`verify left ${leftover.length} shared request(s) for the orchestrator`)

return {
  scenes: done.map(r => ({ id: r.id, history: r.history, last_verdict: r.lastVerdict, qa_errors: r.final && r.final.qa_errors, warnings: r.final && r.final.qa_warnings, weaknesses: r.final && r.final.weaknesses })),
  shared: shared && { applied: shared.applied, rejected: shared.rejected, summary: shared.summary },
  continuity: cont && cont.overall,
  continuity_shared: contShared && { applied: contShared.applied, rejected: contShared.rejected, summary: contShared.summary },
  continuity_fixed: contFixes.filter(Boolean).map(x => ({ id: x.id, qa_errors: x.r && x.r.qa_errors, weaknesses: x.r && x.r.weaknesses })),
  continuity_shared_late: late && { applied: late.applied, rejected: late.rejected, summary: late.summary },
  verify: verified.filter(Boolean).map(x => ({ id: x.id, qa_errors: x.v && x.v.qa_errors, warnings: x.v && x.v.qa_warnings, unresolved: x.v && x.v.unresolved, changes: x.v && x.v.changes })),
  shared_requests_left: leftover,
}
