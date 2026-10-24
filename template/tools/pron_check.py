"""Unprimed pronunciation check: what does a listener hear Kokoro say for names, years and "pron" words?

    tts/.venv/bin/python tools/pron_check.py [--all] [--voice af_heart] [--speed 0.85]

timeline.py aligns each clip with Whisper PRIMED by the sentence text (initial_prompt), so it hears the script back and
its WARNs almost never fire (HN: 0 WARN while Kokoro said "Hadviger-Nelson", "de Brown", "Jan Parts"). This tool
re-transcribes the cached clips audio/sent/<key>.wav with NO prompt and prints SAID / HEARD for every sentence that
contains a capitalised word after its first word, a number word (years are spelled out) or a "pron" key
(--all: every sentence). CHECK = similarity < SIM_MIN or a target word missing from what was heard: listen to that
clip, then fix the "pron" IPA (keys are case-sensitive: a sentence-initial "Zeta" needs its own key) or reword,
re-run timeline.py and this tool. Run after timeline.py; it reads the same cache keys, never synthesises.
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import timeline as tl  # noqa: E402  (same parse/pron/cache key as the clips were made with)

SIM_MIN = 0.9
NUM_WORDS = {"zero", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
             "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
             "thousand", "million", "billion", "trillion"}


def targets(words, pron):
    """Words worth checking: capitalised (not first, not 'I'), number words, digits, pron keys (any case: a key
    that misses only by case, like sentence-initial "Zeta" for key "zeta", is not voiced with its IPA)."""
    out = []
    for i, w in enumerate(words):
        n = tl.norm(w)
        if not n:
            continue
        core = re.sub(r"^[^\w]+", "", w)
        if (i > 0 and core[:1].isupper() and n != "i") or any(x in NUM_WORDS for x in re.split(r"[^a-z]+", w.lower())) \
                or re.search(r"\d", n) or any(re.search(rf"\b{re.escape(k)}\b", w, re.I) for k in pron):
            out.append(w)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="check every sentence, not only names/numbers/pron")
    ap.add_argument("--voice", default="af_heart")
    ap.add_argument("--speed", type=float, default=0.85)
    ap.add_argument("--script", default=str(tl.SCRIPT))
    args = ap.parse_args()

    script = json.loads(Path(args.script).read_text())
    tl.PRON.clear()
    tl.PRON.update(script.get("pron", {}))
    asr = None
    n_checked, flagged, missing = 0, [], []
    for scene in script["scenes"]:
        for pi, para in enumerate(scene["paragraphs"], 1):
            for si, raw in enumerate(para["sentences"], 1):
                where = f"{scene['id']} p{pi}s{si}"
                clean, words, _ = tl.parse_sentence(raw)
                tw = targets(words, tl.PRON)
                if not (tw or args.all):
                    continue
                text = tl.tts_text(clean)
                key = hashlib.sha1(f"{args.voice}|{args.speed}|{text}".encode()).hexdigest()[:16]
                wav = tl.SENT_DIR / f"{key}.wav"
                if not wav.exists():
                    missing.append(where)
                    print(f"MISSING {where}: no clip {wav.name} (run tools/timeline.py first)")
                    continue
                if asr is None:
                    from faster_whisper import WhisperModel
                    asr = WhisperModel("mobiuslabsgmbh/faster-whisper-large-v3-turbo", device="cpu", compute_type="int8")
                segs, _ = asr.transcribe(str(wav), language="en", beam_size=5)   # deliberately NO initial_prompt
                heard = " ".join(s.text.strip() for s in segs).strip()
                a = [tl.norm(w) for w in words]
                b = [tl.norm(w) for w in heard.split()]
                sim = difflib.SequenceMatcher(a=" ".join(a), b=" ".join(b)).ratio()
                lost = [w for w in tw if tl.norm(w) not in b]
                bad = sim < SIM_MIN or bool(lost)
                n_checked += 1
                tag = "CHECK" if bad else "ok   "
                note = f"  missing: {', '.join(lost)}" if lost else ""
                print(f"{tag} {where} sim={sim:.3f}{note}\n      SAID:  {clean}\n      HEARD: {heard}", flush=True)
                if bad:
                    flagged.append(where)
    print(f"{n_checked} sentences checked, {len(flagged)} CHECK, {len(missing)} missing clips"
          + (f": listen to {', '.join(flagged)}" if flagged else ""))


if __name__ == "__main__":
    main()
