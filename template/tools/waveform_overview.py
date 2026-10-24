"""Whole-video voice waveform with scene cuts -> out/waveform_overview.png (run after build.sh concat).

    .venv/bin/python tools/waveform_overview.py

Blue = speech, grey = pause, gold lines = scene cuts. Show it to the user with the final video:
it proves the voice covers the whole video and every pause is a deliberate breath.
"""
import json
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

with wave.open(str(ROOT / "out" / "final" / "_voice.wav")) as wf:
    sr = wf.getframerate()
    x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
dur = len(x) / sr
hop = int(sr * 0.02)
rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same")[::hop])
idx = np.where(rms > 0.006)[0]
longest = float(np.diff(idx).max() * 0.02) if len(idx) > 1 else 0.0

W, H = 2400, 420
img = Image.new("RGB", (W, H), (14, 17, 22))
d = ImageDraw.Draw(img)
f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
per = max(1, len(x) // W)
for i in range(W):
    seg = x[i * per:(i + 1) * per]
    a = np.abs(seg).max() if len(seg) else 0
    h = int(min(1, a * 2.2) * 120)
    d.line([i, 200 - h, i, 200 + h], fill=(78, 168, 245) if a > 0.02 else (70, 80, 100))
script = json.loads((ROOT / "script" / "script.json").read_text())
t = 0.0
for k, sc in enumerate(script["scenes"]):
    tl = json.loads((ROOT / "timeline" / f"{sc['id']}.json").read_text())
    X = int(t / dur * W)
    d.line([X, 40, X, 380], fill=(255, 209, 102), width=2)
    d.text((X + 4, 44 + 18 * (k % 2)), sc["id"].split("_", 1)[1], fill=(255, 209, 102), font=f)
    t += tl["duration"]
for m in range(int(dur // 60) + 1):
    X = int(m * 60 / dur * W)
    d.text((X + 3, 392), f"{m}:00", fill=(150, 150, 150), font=f)
    d.line([X, 385, X, 395], fill=(150, 150, 150))
d.text((8, 8), f"Final voice track, {int(dur // 60)}:{dur % 60:04.1f}: blue = speech. Gold lines = scene cuts. "
               f"Longest pause: {longest:.2f} s.", fill=(220, 220, 220), font=f)
out = ROOT / "out" / "waveform_overview.png"
img.save(out)
print(out)
