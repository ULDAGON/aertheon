#!/usr/bin/env bash
# One-time: create the two shared Python environments every video links to.
#   .venv   Manim (render, QA)     tts/.venv   Kokoro TTS + Whisper (narration timeline)
# Needs: uv, ffmpeg, rsvg-convert, pkg-config + cairo + pango to build pycairo/manimpango
#   (brew install uv ffmpeg librsvg pkgconf cairo pango). Models download to ~/.cache/huggingface on first use.
set -euo pipefail
cd "$(dirname "$0")"
export UV_HTTP_TIMEOUT=${UV_HTTP_TIMEOUT:-120}   # the first TTS install timed out on PyPI at uv's default
.venv/bin/python -c "import manim, scipy, mpmath" 2>/dev/null || { [ -d .venv ] || uv venv --python 3.12 .venv; uv pip install --python .venv/bin/python -r requirements-manim.txt; }
mkdir -p tts
tts/.venv/bin/python -c "import mlx_audio, faster_whisper, misaki, soundfile" 2>/dev/null || { [ -d tts/.venv ] || uv venv --python 3.12 tts/.venv; uv pip install --python tts/.venv/bin/python -r requirements-tts.txt; }
.venv/bin/manim --version
tts/.venv/bin/python -c "import mlx_audio, faster_whisper, soundfile; print('tts env ok')"
for t in ffmpeg ffprobe rsvg-convert; do command -v $t >/dev/null || echo "MISSING: $t"; done
