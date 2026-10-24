"""Narration -> per-sentence TTS -> word alignment -> per-scene audio + timeline.

    tts/.venv/bin/python tools/timeline.py [--voice af_heart] [--speed 0.85]

Reads  script/script.json   (scenes -> paragraphs -> sentences with {#bookmark} markers, pause_after; "pron" table)
Writes audio/sent/<key>.wav|.json   cached per-sentence audio + word timings (key = hash of voice/speed/text)
       audio/scenes/<Scene>.wav     the scene's narration track (24 kHz mono), length = timeline duration
       timeline/<Scene>.json        exact times of every paragraph, sentence and bookmark
       timeline/_summary.json       per-scene durations, total, pronunciation warnings
       script/captions.srt          sentence-level subtitles for the whole video

Pacing (seconds): LEAD before the first sentence, SENT_GAP between sentences of a paragraph,
paragraph.pause_after between paragraphs (clamped), TAIL after the last sentence. Scene durations are
rounded up to a multiple of 1/15 s so they are frame-exact at 15, 30 and 60 fps.
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "script" / "script.json"
SENT_DIR = ROOT / "audio" / "sent"
SCENE_DIR = ROOT / "audio" / "scenes"
TL_DIR = ROOT / "timeline"

SR = 24000
GRID = 1 / 15
LEAD = 0.30
SENT_GAP = 0.55
PAUSE_MIN, PAUSE_MAX = 0.55, 1.5
TAIL_MIN, TAIL_MAX = 0.5, 0.9
FINAL_TAIL_MAX = 2.0   # the very last scene may hold its final image a little longer

MARK_RE = re.compile(r"\{#([a-z0-9_]+)\}")
# Kokoro/misaki inline pronunciations for names it would otherwise mangle: script.json "pron" {"Name": "/ipa/"}.
# Filled in main(). Check every proper noun: Whisper "heard" text that differs from the script is printed as WARN.
PRON = {}


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


def parse_sentence(raw):
    """-> clean text, list of words, {mark: word_index}."""
    marks, words = {}, []
    pos = 0
    for m in MARK_RE.finditer(raw):
        before = raw[pos:m.start()]
        words += before.split()
        marks[m.group(1)] = len(words)
        pos = m.end()
    words += raw[pos:].split()
    clean = " ".join(words)
    return clean, words, marks


def tts_text(clean):
    out = clean
    for name, ph in PRON.items():
        out = re.sub(rf"\b{name}\b", f"[{name}]({ph})", out)
    return out


def trim(a, thresh=0.008, pad=0.04):
    idx = np.where(np.abs(a) > thresh)[0]
    if len(idx) == 0:
        return a
    p = int(pad * SR)
    a = a[max(0, idx[0] - p): idx[-1] + p]
    f = int(0.01 * SR)  # 10 ms fades against clicks
    a[:f] *= np.linspace(0, 1, f)
    a[-f:] *= np.linspace(1, 0, f)
    return a


class Engine:
    def __init__(self, voice, speed):
        self.voice, self.speed = voice, speed
        self._tts = None
        self._asr = None

    def tts(self, text):
        if self._tts is None:
            from mlx_audio.tts.utils import load_model
            self._tts = load_model("prince-canuma/Kokoro-82M")
        chunks = [np.array(r.audio) for r in
                  self._tts.generate(text, voice=self.voice, speed=self.speed, lang_code="a", split_pattern=r"\n+")]
        return trim(np.concatenate(chunks).astype(np.float32))

    def align(self, wav_path, clean):
        if self._asr is None:
            from faster_whisper import WhisperModel
            self._asr = WhisperModel("mobiuslabsgmbh/faster-whisper-large-v3-turbo", device="cpu", compute_type="int8")
        segs, _ = self._asr.transcribe(str(wav_path), word_timestamps=True, language="en",
                                       initial_prompt=clean, beam_size=5, vad_filter=False)
        return [{"w": w.word.strip(), "s": float(w.start), "e": float(w.end)} for s in segs for w in s.words]


def word_times(words, asr, dur):
    """Start/end time for every script word: exact where whisper matched, interpolated elsewhere."""
    a = [norm(w) for w in words]
    b = [norm(x["w"]) for x in asr]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    start = [None] * len(words)
    end = [None] * len(words)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            start[blk.a + k] = asr[blk.b + k]["s"]
            end[blk.a + k] = asr[blk.b + k]["e"]
    matched = sum(s is not None for s in start)
    # interpolate unmatched words by character position between anchors
    chars = np.cumsum([0] + [len(w) + 1 for w in words])
    anchors = [(-1, 0.0)] + [(i, start[i]) for i in range(len(words)) if start[i] is not None] + [(len(words), dur)]
    for (i0, t0), (i1, t1) in zip(anchors, anchors[1:]):
        c0 = chars[max(i0, 0)] if i0 >= 0 else 0
        c1 = chars[i1] if i1 < len(words) else chars[-1]
        for i in range(i0 + 1, i1):
            f = (chars[i] - c0) / max(1, c1 - c0)
            start[i] = t0 + f * (t1 - t0)
    for i in range(len(words)):
        if end[i] is None:
            end[i] = start[i + 1] if i + 1 < len(words) else dur
    heard = " ".join(x["w"] for x in asr)
    sim = difflib.SequenceMatcher(a=" ".join(a), b=" ".join(b)).ratio()
    return start, end, matched, heard, sim


def fmt_srt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="af_heart")
    ap.add_argument("--speed", type=float, default=0.85)
    ap.add_argument("--script", default=str(SCRIPT))
    args = ap.parse_args()

    script = json.loads(Path(args.script).read_text())
    PRON.update(script.get("pron", {}))
    for d in (SENT_DIR, SCENE_DIR, TL_DIR):
        d.mkdir(parents=True, exist_ok=True)
    eng = Engine(args.voice, args.speed)
    summary = {"scenes": [], "warnings": []}
    srt, srt_i, offset = [], 1, 0.0

    for scene in script["scenes"]:
        sid = scene["id"]
        marks, sentences, paragraphs = {}, [], []
        pieces = []  # (start_time, audio)
        t = LEAD
        for pi, para in enumerate(scene["paragraphs"], 1):
            p_start = t
            marks[f"p{pi}"] = round(t, 4)
            for si, raw in enumerate(para["sentences"], 1):
                clean, words, bm = parse_sentence(raw)
                text = tts_text(clean)
                key = hashlib.sha1(f"{args.voice}|{args.speed}|{text}".encode()).hexdigest()[:16]
                wav, meta = SENT_DIR / f"{key}.wav", SENT_DIR / f"{key}.json"
                if wav.exists() and meta.exists():
                    audio, _ = sf.read(wav, dtype="float32")
                    info = json.loads(meta.read_text())
                else:
                    audio = eng.tts(text)
                    sf.write(wav, audio, SR)
                    asr = eng.align(wav, clean)
                    info = {"text": clean, "asr": asr}
                    meta.write_text(json.dumps(info, ensure_ascii=False))
                dur = len(audio) / SR
                st, en, matched, heard, sim = word_times(words, info["asr"], dur)
                if sim < 0.85 or matched < 0.7 * len(words):
                    summary["warnings"].append({"scene": sid, "sentence": clean, "heard": heard, "similarity": round(sim, 3)})
                sid_s = f"p{pi}s{si}"
                marks[sid_s] = round(t, 4)
                marks[f"{sid_s}_end"] = round(t + dur, 4)
                for name, wi in bm.items():
                    if name in marks:
                        raise SystemExit(f"{sid}: bookmark {name!r} collides with another mark")
                    marks[name] = round(t + (st[wi] if wi < len(words) else dur), 4)
                sentences.append({"id": sid_s, "start": round(t, 4), "end": round(t + dur, 4), "text": clean,
                                  "words": [{"w": w, "s": round(t + a, 3), "e": round(t + b, 3)} for w, a, b in zip(words, st, en)]})
                pieces.append((t, audio))
                srt.append(f"{srt_i}\n{fmt_srt(offset + t)} --> {fmt_srt(offset + t + dur)}\n{clean}\n")
                srt_i += 1
                t += dur
                if si < len(para["sentences"]):
                    t += SENT_GAP
            marks[f"p{pi}_end"] = round(t, 4)
            paragraphs.append({"id": f"p{pi}", "start": round(p_start, 4), "end": round(t, 4),
                               "visual": para.get("visual", "")})
            last = pi == len(scene["paragraphs"])
            pause = float(para.get("pause_after", 0.8))
            tail_max = FINAL_TAIL_MAX if scene is script["scenes"][-1] else TAIL_MAX
            t += min(max(pause, TAIL_MIN), tail_max) if last else min(max(pause, PAUSE_MIN), PAUSE_MAX)
        duration = float(np.ceil(t / GRID - 1e-9) * GRID)
        n = int(round(duration * SR))
        track = np.zeros(n, dtype=np.float32)
        for t0, a in pieces:
            i0 = int(round(t0 * SR))
            track[i0:i0 + len(a)] += a[: max(0, n - i0)]
        sf.write(SCENE_DIR / f"{sid}.wav", track, SR)
        tl = {"scene": sid, "title": scene.get("title", ""), "duration": round(duration, 6), "marks": marks,
              "paragraphs": paragraphs, "sentences": sentences}
        (TL_DIR / f"{sid}.json").write_text(json.dumps(tl, indent=1, ensure_ascii=False))
        speech = sum(s["end"] - s["start"] for s in sentences)
        summary["scenes"].append({"id": sid, "duration": round(duration, 3), "speech": round(speech, 3),
                                  "sentences": len(sentences), "marks": len(marks)})
        print(f"{sid:22s} {duration:7.2f}s  speech {speech:6.2f}s  {len(sentences):3d} sentences", flush=True)
        offset += duration

    summary["total"] = round(offset, 3)
    (TL_DIR / "_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    (ROOT / "script" / "captions.srt").write_text("\n".join(srt))
    print(f"TOTAL {int(offset // 60)}:{offset % 60:05.2f}  ({offset:.1f}s)")
    for w in summary["warnings"]:
        print(f"WARN {w['scene']} sim={w['similarity']}: said {w['sentence']!r} / heard {w['heard']!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
