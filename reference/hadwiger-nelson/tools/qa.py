"""Speech-vs-picture QA for one rendered scene.

    .venv/bin/python tools/qa.py <SceneId> [l|m|h]

Compares the scene's narration waveform (audio/scenes/<Scene>.wav) with the rendered picture
(out/media/<Scene>/.../<Scene>.mp4) frame by frame and writes into out/qa/:
  <Scene>.report.txt     errors / warnings (also printed)
  <Scene>.timeline.png   waveform, motion curve, sentences, bookmarks, flagged spans (red)
  <Scene>.marks.png      one labelled frame shortly after every bookmark  (does the picture match the word?)
  <Scene>.sheet.png      one labelled frame every ~2.5 s with the sentence being spoken
Exit code 1 if there are errors.

Checks
  ERROR  frame count != audio length (frame-exact sync is required)
  ERROR  overrun / late marks (from the TimedScene timing report), lateness > 0.25 s
  ERROR  motion while nobody speaks for more than MAX_SILENT_MOTION s   ("animation without voice")
  ERROR  a silence in the narration longer than MAX_GAP s
  WARN   picture frozen for more than MAX_STATIC s while the narrator talks ("dead visuals")
  WARN   no visual change within [-0.3, +1.0] s of a bookmark
"""
import glob
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / "out" / "qa"
MAX_SILENT_MOTION = 1.6
MAX_GAP = 1.6
MAX_STATIC = 5.0
RES = {"l": (15, "480p15"), "m": (30, "720p30"), "h": (60, "1080p60"), "k": (60, "2160p60")}


def font(size):
    for f in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def runs(mask):
    """[(start_idx, end_idx_exclusive)] of True runs."""
    m = np.concatenate([[False], mask, [False]]).astype(int)
    d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def grab(video, times, w=480):
    """RGB frames (PIL) at the given times, in order."""
    out = []
    for t in times:
        p = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{max(0, t):.3f}", "-i", video, "-frames:v", "1",
                            "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        from io import BytesIO
        out.append(Image.open(BytesIO(p.stdout)).convert("RGB") if p.stdout else Image.new("RGB", (w, w * 9 // 16)))
    return out


def sheet(frames, labels, cols, path, w=480):
    h = frames[0].height if frames else 270
    lab_h = 44
    rows = (len(frames) + cols - 1) // cols
    img = Image.new("RGB", (cols * (w + 6), max(1, rows) * (h + lab_h + 6)), (0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(15)
    for i, (fr, lab) in enumerate(zip(frames, labels)):
        x, y = (i % cols) * (w + 6), (i // cols) * (h + lab_h + 6)
        img.paste(fr, (x, y))
        lines = [lab[:62], lab[62:124]]
        for k, ln in enumerate(lines):
            d.text((x + 4, y + h + 3 + 19 * k), ln, fill=(230, 230, 230), font=f)
    img.save(path)


def main():
    sid = sys.argv[1]
    q = sys.argv[2] if len(sys.argv) > 2 else "l"
    fps, res = RES[q]
    tl = json.loads((ROOT / "timeline" / f"{sid}.json").read_text())
    vids = glob.glob(str(ROOT / "out" / "media" / sid / "videos" / "*" / res / f"{sid}.mp4"))
    if not vids:
        sys.exit(f"no {res} render for {sid}; run tools/render.sh {sid} {q}")
    video = vids[0]
    QA.mkdir(parents=True, exist_ok=True)
    errors, warns, flagged = [], [], []

    # ---- picture: motion per frame (tiny grayscale)
    W, H = 320, 180
    proc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", video, "-vf", f"scale={W}:{H}:flags=area,format=gray",
                             "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    motion, changed, prev = [], [], None
    while True:
        buf = proc.stdout.read(W * H)
        if len(buf) < W * H:
            break
        cur = np.frombuffer(buf, np.uint8).astype(np.int16)
        if prev is None:
            motion.append(0.0); changed.append(0)
        else:
            dd = np.abs(cur - prev)
            motion.append(float(dd.mean())); changed.append(int((dd > 10).sum()))
        prev = cur
    proc.wait()
    motion, changed = np.array(motion), np.array(changed)
    nf = len(motion)
    moving = changed >= 3   # a few pixels really changed (codec noise stays below the threshold)

    # ---- sound: speech per frame
    import wave
    with wave.open(str(ROOT / "audio" / "scenes" / f"{sid}.wav")) as wf:
        sr = wf.getframerate()
        a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    spf = sr / fps
    n_audio_frames = int(round(len(a) / spf))
    rms = np.array([np.sqrt(np.mean(a[int(i * spf):int((i + 1) * spf)] ** 2) + 1e-12) for i in range(n_audio_frames)])
    speech = rms > 0.006
    for s, e in runs(~speech):  # close short intra-sentence gaps
        if (e - s) / fps < 0.3 and s > 0 and e < len(speech):
            speech[s:e] = True

    # ---- checks
    target = int(round(tl["duration"] * fps))
    if nf != target:
        errors.append(f"frame count {nf} != audio length {target} frames ({tl['duration']:.3f}s)")
    tj = QA / f"{sid}.timing.{fps}.json"
    if tj.exists():
        tr = json.loads(tj.read_text())
        if tr["overrun_s"] > 0.05:
            errors.append(f"scene overran its audio by {tr['overrun_s']:.2f}s")
        for L in tr["late"]:
            (errors if L["late_s"] > 0.25 else warns).append(f"late by {L['late_s']:.2f}s at mark {L['mark']!r} ({L['kind']})")
    n = min(nf, len(speech))
    sp, mv = speech[:n], moving[:n]
    for s, e in runs(~sp):
        dur = (e - s) / fps
        if dur > MAX_GAP and not (s == 0 or e >= n):
            errors.append(f"narration silent for {dur:.2f}s at {s / fps:.2f}-{e / fps:.2f}s")
            flagged.append((s / fps, e / fps))
        mv_in = mv[s:e]
        if mv_in.any():
            # longest stretch from first to last moving frame inside this silence
            idx = np.where(mv_in)[0]
            span = (idx[-1] - idx[0] + 1) / fps
            if span > MAX_SILENT_MOTION:
                errors.append(f"animation without voice for {span:.2f}s at {(s + idx[0]) / fps:.2f}s")
                flagged.append(((s + idx[0]) / fps, (s + idx[-1] + 1) / fps))
    for s, e in runs(sp & ~mv):
        dur = (e - s) / fps
        if dur > MAX_STATIC:
            said = " / ".join(x["text"][:50] for x in tl["sentences"] if x["end"] > s / fps and x["start"] < e / fps)
            warns.append(f"picture frozen {dur:.1f}s while speaking at {s / fps:.1f}-{e / fps:.1f}s: {said}")
            flagged.append((s / fps, e / fps))
    auto = {k for k in tl["marks"] if k.startswith("p") and (k[1:].split("s")[0].split("_")[0]).isdigit()}
    bookmarks = {k: v for k, v in tl["marks"].items() if k not in auto}
    for k, t in sorted(bookmarks.items(), key=lambda kv: kv[1]):
        i0, i1 = max(0, int((t - 0.3) * fps)), min(n, int((t + 1.0) * fps) + 1)
        if not mv[i0:i1].any():
            warns.append(f"no visual change near bookmark {k!r} at {t:.2f}s")

    speech_s = sp.sum() / fps
    silent_motion = (mv & ~sp).sum() / fps
    stats = (f"{sid} [{res}] duration {nf / fps:.2f}s, speech {speech_s:.1f}s ({100 * speech_s / max(1e-9, n / fps):.0f}%), "
             f"motion {100 * mv.mean():.0f}% of frames, motion-while-silent {silent_motion:.1f}s")

    # ---- timeline plot
    Wp = max(1200, int(n / fps * 24))
    img = Image.new("RGB", (Wp, 330), (14, 17, 22))
    d = ImageDraw.Draw(img)
    f = font(12)
    X = lambda t: int(t / (n / fps) * (Wp - 1))
    for s, e in flagged:
        d.rectangle([X(s), 0, X(e), 329], fill=(70, 20, 24))
    env = np.array([np.abs(a[int(i * spf):int((i + 1) * spf)]).max() if i < n_audio_frames else 0 for i in range(n)])
    for i in range(n):
        x = X(i / fps)
        h = int(min(1, env[i] * 2.2) * 55)
        d.line([x, 70 - h, x, 70 + h], fill=(78, 168, 245) if sp[i] else (60, 70, 90))
        m = int(min(1, np.log1p(changed[i]) / np.log1p(W * H * 0.25)) * 70)
        d.line([x, 220, x, 220 - m], fill=(242, 158, 76) if sp[i] else (255, 92, 92))
    for sent in tl["sentences"]:
        d.rectangle([X(sent["start"]), 236, X(sent["end"]), 252], outline=(140, 147, 163))
        d.text((X(sent["start"]) + 2, 238), sent["id"], fill=(200, 200, 200), font=f)
    for j, (k, t) in enumerate(sorted(bookmarks.items(), key=lambda kv: kv[1])):
        d.line([X(t), 128, X(t), 150], fill=(255, 209, 102), width=2)
        d.text((X(t) + 2, 256 + 14 * (j % 4)), k, fill=(255, 209, 102), font=f)
    for sec in range(int(n / fps) + 1):
        d.line([X(sec), 318, X(sec), 324 if sec % 5 else 329], fill=(120, 120, 120))
        if sec % 5 == 0:
            d.text((X(sec) + 2, 305), f"{sec}s", fill=(150, 150, 150), font=f)
    d.text((6, 4), "narration (blue = speech)", fill=(160, 170, 190), font=f)
    d.text((6, 134), "picture motion (red = while silent)", fill=(242, 158, 76), font=f)
    img.save(QA / f"{sid}.timeline.png")

    # ---- contact sheets
    def said_at(t):
        for x in tl["sentences"]:
            if x["start"] - 0.2 <= t <= x["end"] + 0.2:
                words = [w["w"] for w in x["words"] if w["s"] <= t + 0.05]
                return " ".join(words[-7:])
        return "(pause)"
    mk = sorted(bookmarks.items(), key=lambda kv: kv[1])
    mt = [min(t + 0.9, n / fps - 0.05) for _, t in mk]
    if mk:
        sheet(grab(video, mt), [f"{k} @{t:.1f}s: ..{said_at(t)}" for (k, t) in mk], 4, QA / f"{sid}.marks.png")
    st = list(np.arange(0.5, n / fps, 2.5))
    sheet(grab(video, st), [f"{t:.1f}s: ..{said_at(t)}" for t in st], 5, QA / f"{sid}.sheet.png")

    lines = [stats] + [f"ERROR {e}" for e in errors] + [f"WARN  {w}" for w in warns]
    lines += [f"files: out/qa/{sid}.timeline.png, out/qa/{sid}.marks.png, out/qa/{sid}.sheet.png"]
    (QA / f"{sid}.report.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
