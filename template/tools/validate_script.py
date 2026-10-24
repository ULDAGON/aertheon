"""Validate a script JSON against the AERTHEON script format (engine/SCRIPT_FORMAT.md) and estimate its runtime.

    python3 tools/validate_script.py [script/script.json] [--minutes 10]

Prints per-scene words and estimated seconds, then ERROR / WARN lines. Exit code 1 on any ERROR.
The runtime model mirrors tools/timeline.py pacing with Kokoro af_heart at speed 0.85 (~181 wpm measured).
Budget scales with --minutes (default: script "target_minutes", else 10): words 135-145 per minute,
about one scene per minute of video, every scene 35-90 s (25-90 s for videos under 5 minutes).
Pacing WARNs (estimated times): bookmarks in one sentence < MARK_GAP_MIN s apart (two visual beats the eye cannot
separate), more than MARK_GAP_MAX s of speech without any mark (bookmark or sentence start: a static stretch), and
pause_after > 0.9 on a scene's last paragraph (timeline.py clamps that tail to 0.5-0.9 s; only the video's final
paragraph may hold up to 2.0). Not WARNed, because the pilot does it on purpose: rapid count/list beats one or two words
apart in one sentence (HN S01 "{#five} five, {#six} six, or {#seven} seven"; S08 seventy/ninety/twenty-ten/frozen), and
marks in different sentences (the 0.55 s sentence gap separates them).
"""
import argparse
import json
import re
import sys
from pathlib import Path

MARK = re.compile(r"\{#([^}]*)\}")
GOOD_MARK = re.compile(r"^[a-z]+(_[a-z]+)*$")
ID_RE = re.compile(r"^S\d\d_[A-Z][A-Za-z]+$")
AUTO_MARK = re.compile(r"^p\d+(s\d+)?(_end)?$|^end$")
BAD_CHARS = re.compile(r"[0-9()\[\]{}—–/%&+=<>*#@$≤≥χ√…•→]")
WPS = 181 / 60                # words per second at speed 0.85
SENT_GAP, LEAD = 0.55, 0.30
PAUSE = (0.55, 1.5)
TAIL = (0.5, 0.9)
MARK_GAP_MIN, MARK_GAP_MAX = 0.95, 5.0


def words_of(sentence):
    return MARK.sub(" ", sentence).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parent.parent / "script" / "script.json"))
    ap.add_argument("--minutes", type=float, default=None)
    args = ap.parse_args()
    errors, warns = [], []
    try:
        s = json.loads(Path(args.path).read_text())
    except Exception as e:  # noqa: BLE001
        sys.exit(f"ERROR cannot load {args.path}: {e}")

    minutes = args.minutes or float(s.get("target_minutes", 10))
    w_lo, w_hi = round(135 * minutes), round(145 * minutes)
    sc_lo, sc_hi = max(1, round(minutes * 0.9)), max(2, round(minutes * 1.1))

    for key in ("title", "scenes", "pronunciation_notes", "facts"):
        if key not in s:
            errors.append(f"missing top-level key {key!r}")
    scenes = s.get("scenes", [])
    if not sc_lo <= len(scenes) <= sc_hi:
        errors.append(f"{len(scenes)} scenes; target {sc_lo}-{sc_hi} for {minutes:g} min")
    pron = s.get("pron", {})
    if not isinstance(pron, dict) or any(not (isinstance(v, str) and v.startswith("/") and v.endswith("/")) for v in pron.values()):
        errors.append('"pron" must map Name -> "/ipa/"')

    total_words, total_s, ids = 0, 0.0, set()
    rows = []
    for si, sc in enumerate(scenes):
        sid = sc.get("id", f"#{si}")
        if not ID_RE.match(sid):
            errors.append(f"{sid}: id must look like S01_CamelCase")
        if sid in ids:
            errors.append(f"{sid}: duplicate id")
        ids.add(sid)
        for key in ("title", "purpose", "paragraphs"):
            if not sc.get(key):
                errors.append(f"{sid}: missing {key!r}")
        paras = sc.get("paragraphs", [])
        if not 2 <= len(paras) <= 7:
            errors.append(f"{sid}: {len(paras)} paragraphs (2-7)")
        seen, scene_words, t = {}, 0, LEAD
        bm_times = []   # (estimated seconds, "P2 {#name}", (paragraph, sentence), word index) of every bookmark
        last_scene = si == len(scenes) - 1
        for pi, p in enumerate(paras, 1):
            where = f"{sid} P{pi}"
            sents = p.get("sentences", [])
            if not 1 <= len(sents) <= 4:
                errors.append(f"{where}: {len(sents)} sentences (1-4)")
            vis = p.get("visual", "")
            if len(vis.strip()) < 40:
                errors.append(f"{where}: storyboard 'visual' missing or too thin")
            pa = p.get("pause_after")
            pa_max = 2.0 if last_scene and pi == len(paras) else 1.5   # the video's final hold may be longer
            if not isinstance(pa, (int, float)) or not 0.5 <= pa <= pa_max:
                errors.append(f"{where}: pause_after {pa!r} (0.5-{pa_max})")
                pa = 0.8
            elif pa > 1.4 and not (last_scene and pi == len(paras)):
                # the clip's own trailing silence adds ~0.1 s: 1.5 measured 1.62 s in final QA (limit 1.6)
                warns.append(f"{where}: pause_after {pa} > 1.4 makes a voice gap over final QA's 1.6 s limit")
            elif pi == len(paras) and not last_scene and pa > TAIL[1]:
                warns.append(f"{where}: pause_after {pa} on the scene's last paragraph is clamped to {TAIL[1]}; "
                             f"plan no reveal in that tail")
            pmarks = []
            for k, sent in enumerate(sents, 1):
                ws = words_of(sent)
                scene_words += len(ws)
                # word index of each bookmark (as timeline.py parses it), then the longest unmarked stretch
                idx, n = [], 0
                for piece in re.split(r"(\{#[^}]*\})", sent):
                    if MARK.fullmatch(piece):
                        idx.append(n)
                        bm_times.append((t + n / WPS, f"P{pi} {piece}", (pi, k), n))
                    else:
                        n += len(piece.split())
                cuts = [0] + idx + [len(ws)]
                run = max(b - a for a, b in zip(cuts, cuts[1:])) / WPS
                if run > MARK_GAP_MAX:
                    warns.append(f"{where}s{k}: ~{run:.1f}s of speech without a mark; add a bookmark "
                                 f"(>{MARK_GAP_MAX:g} s static): {' '.join(ws)[:60]!r}")
                t += len(ws) / WPS + (SENT_GAP if k < len(sents) else 0)
                if len(ws) > 24:
                    errors.append(f"{where}s{k}: {len(ws)} words (max 24): {sent[:60]!r}")
                clean = MARK.sub("", sent)
                bad = sorted(set(BAD_CHARS.findall(clean)))
                if bad:
                    errors.append(f"{where}s{k}: spell out / remove {''.join(bad)!r} (spoken text only): {clean[:60]!r}")
                if re.search(r"\{#[^}]*\}\s*[.?!,;:\"']*\s*$", sent):
                    errors.append(f"{where}s{k}: bookmark at sentence end; put it before the word that triggers the visual")
                if "{" in MARK.sub("", sent) or "}" in MARK.sub("", sent):
                    errors.append(f"{where}s{k}: malformed bookmark braces")
                for m in MARK.findall(sent):
                    pmarks.append(m)
                    if not GOOD_MARK.match(m):
                        errors.append(f"{where}: bookmark {{#{m}}} must be lowercase snake_case letters, no digits")
                    if AUTO_MARK.match(m):
                        errors.append(f"{where}: bookmark {{#{m}}} collides with automatic marks (p1, p1s2, p1_end, end)")
                    if m in seen:
                        errors.append(f"{where}: bookmark {{#{m}}} already used in {seen[m]}")
                    seen[m] = f"P{pi}"
            if not 1 <= len(pmarks) <= 5:
                (errors if not pmarks else warns).append(f"{where}: {len(pmarks)} bookmarks (1-5)")
            for m in pmarks:
                if f"{{#{m}}}" not in vis:
                    warns.append(f"{where}: storyboard never says what happens at {{#{m}}}")
            for m in MARK.findall(vis):
                if m not in pmarks and m not in seen:
                    warns.append(f"{where}: storyboard references {{#{m}}}, not a bookmark of this paragraph")
            if pi < len(paras):
                t += min(max(pa, PAUSE[0]), PAUSE[1])
            else:
                t += min(max(pa, TAIL[0]), 2.0 if last_scene else TAIL[1])
        for (t0, m0, s0, n0), (t1, m1, s1, n1) in zip(bm_times, bm_times[1:]):
            if s0 != s1 or 1 <= n1 - n0 <= 2:   # other sentence, or a pilot-style count/list beat
                continue
            if t1 - t0 < MARK_GAP_MIN:
                warns.append(f"{sid}: {m0} -> {m1} only ~{t1 - t0:.2f}s apart (min {MARK_GAP_MIN}); merge or spread them")
        sc_min = 35 if minutes >= 5 else 25   # short videos: two ~30 s scenes beat one long one
        if not sc_min <= t <= 90:
            warns.append(f"{sid}: estimated {t:.0f}s ({sc_min}-90 s per scene)")
        rows.append((sid, scene_words, t))
        total_words += scene_words
        total_s += t

    if not w_lo <= total_words <= w_hi:
        errors.append(f"{total_words} spoken words; target {w_lo}-{w_hi} for {minutes:g} min")
    for i, f in enumerate(s.get("facts", [])):
        if not (isinstance(f, dict) and f.get("claim") and f.get("source")):
            errors.append(f"facts[{i}]: needs 'claim' and 'source'")
    if not s.get("facts"):
        errors.append("no facts: every narrated factual claim needs a source")

    for sid, w, t in rows:
        print(f"{sid:24s} {w:5d} words  ~{t:5.1f}s")
    print(f"TOTAL {total_words} words, ~{int(total_s // 60)}:{total_s % 60:04.1f} "
          f"(target {minutes:g} min, {w_lo}-{w_hi} words)")
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
