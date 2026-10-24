"""Whole-video QA after build.sh:  .venv/bin/python tools/final_qa.py ../<name>.mp4

- video and audio stream lengths agree (<= 1 frame)
- the voice track never pauses longer than MAX_GAP (waveform check on out/final/_voice.wav)
- every sentence of the script is audible where the timeline says (RMS inside each sentence span)
- per-scene QA reports are all clean (collects ERROR/WARN lines)
- integrated loudness of the final mix
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MAX_GAP = 1.6


def probe(path, sel):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", "stream=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.split()
    return float(out[0]) if out else float("nan")


def main():
    final = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / (ROOT.parent.name.replace("-", "_") + ".mp4"))
    errors, warns = [], []
    v, a = probe(final, "v:0"), probe(final, "a:0")
    if abs(v - a) > 0.05:
        errors.append(f"stream lengths differ: video {v:.3f}s audio {a:.3f}s")

    with wave.open(str(ROOT / "out" / "final" / "_voice.wav")) as wf:
        sr = wf.getframerate()
        x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    hop = int(sr * 0.02)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same")[::hop])
    speech = rms > 0.006
    idx = np.where(speech)[0]
    gaps = np.diff(idx) * 0.02
    big = [(idx[i] * 0.02, g) for i, g in enumerate(gaps) if g > MAX_GAP]
    for t, g in big:
        errors.append(f"voice pauses {g:.2f}s at {t:.1f}s ({int(t // 60)}:{t % 60:04.1f})")

    # every sentence audible at its timeline position
    script = json.loads((ROOT / "script" / "script.json").read_text())
    off = 0.0
    missing = 0
    for sc in script["scenes"]:
        tl = json.loads((ROOT / "timeline" / f"{sc['id']}.json").read_text())
        for s in tl["sentences"]:
            i0, i1 = int((off + s["start"]) * sr), int((off + s["end"]) * sr)
            seg = x[i0:i1]
            if len(seg) == 0 or np.sqrt(np.mean(seg ** 2)) < 0.01:
                errors.append(f"sentence silent in final voice track: {sc['id']} {s['id']} {s['text'][:60]!r}")
                missing += 1
        off += tl["duration"]
    if abs(off - len(x) / sr) > 0.05:
        errors.append(f"voice track {len(x) / sr:.2f}s != sum of scene timelines {off:.2f}s")

    for rep in sorted((ROOT / "out" / "qa").glob("*.report.txt")):
        if rep.name.startswith("ZZ_"):
            continue
        for line in rep.read_text().splitlines():
            if line.startswith("ERROR"):
                errors.append(f"{rep.name.split('.')[0]}: {line[6:]}")
            elif line.startswith("WARN"):
                warns.append(f"{rep.name.split('.')[0]}: {line[6:]}")

    ld = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", ld)
    speech_pct = 100 * speech.mean()
    print(f"final {final.name}: video {v:.2f}s ({int(v // 60)}:{v % 60:05.2f}), audio {a:.2f}s, "
          f"speech {speech_pct:.0f}% of time, longest voice pause {max(gaps) if len(gaps) else 0:.2f}s, "
          f"loudness {m[-1] if m else '?'} LUFS")
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
