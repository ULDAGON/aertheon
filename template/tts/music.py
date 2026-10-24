"""Soft ambient pad bed (procedural, no samples): audio/bed.wav of the requested length.

tts/.venv/bin/python tts/music.py <seconds>
Slow Cmaj7 - Am9 - Fmaj7 - G6 progression, detuned sines with long attack/release, gentle
tremolo, one-pole low-pass. Meant to sit ~25 dB under the voice.
"""
import sys
from pathlib import Path
import numpy as np
import soundfile as sf

SR = 48000
dur = float(sys.argv[1]) if len(sys.argv) > 1 else 240
n = int(dur * SR)
t = np.arange(n) / SR

def hz(m): return 440 * 2 ** ((m - 69) / 12)
CHORDS = [[48, 55, 59, 64, 67], [45, 52, 57, 60, 64, 71], [41, 48, 53, 57, 64], [43, 50, 55, 59, 64]]
SEG = 8.0  # seconds per chord
out = np.zeros(n)
rng = np.random.default_rng(7)
k = 0
start = 0.0
while start < dur:
    notes = CHORDS[k % len(CHORDS)]
    a, b = int(start * SR), min(n, int((start + SEG + 4.0) * SR))  # 4 s overlap tail
    tt = t[a:b] - start
    env = np.clip(tt / 3.0, 0, 1) * np.clip((SEG + 4.0 - tt) / 4.0, 0, 1)
    env = env ** 1.5
    for m in notes:
        f = hz(m + 12)
        for det in (-0.12, 0.12):
            ph = rng.uniform(0, 2 * np.pi)
            out[a:b] += env * np.sin(2 * np.pi * f * (1 + det / 100) * tt + ph) / len(notes)
    k += 1
    start += SEG
# gentle tremolo + low-pass
out *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t)
F = np.fft.rfft(out); fr = np.fft.rfftfreq(n, 1 / SR)
y = np.fft.irfft(F / np.sqrt(1 + (fr / 1800) ** 2), n)  # 1-pole-ish low-pass
fade = int(3 * SR); y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
y = y / (np.max(np.abs(y)) + 1e-9) * 0.5
st = np.stack([y, np.roll(y, int(0.012 * SR))], axis=1)
Path("audio").mkdir(exist_ok=True)
sf.write("audio/bed.wav", st.astype(np.float32), SR)
print("bed", dur)
