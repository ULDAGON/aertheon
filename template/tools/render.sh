#!/usr/bin/env bash
# Render one scene (silent, frame-exact), mux its narration into a preview, run speech-vs-picture QA.
#   tools/render.sh <SceneId> [l|m|h]      (default l = 480p15 draft)
#   NOCACHE=1 tools/render.sh <SceneId> l  passes --disable_caching (closures over numpy/scipy, ValueTrackers or
#                                          always_redraw can crash the hasher or replay stale partial movies; never rm caches)
# Outputs: out/media/<SceneId>/... (silent render), out/preview/<SceneId>_<res>.mp4 (with voice), out/qa/<SceneId>.*
set -euo pipefail
cd "$(dirname "$0")/.."
S="$1"; Q="${2:-l}"
case "$Q" in l) RES=480p15;; m) RES=720p30;; h) RES=1080p60;; esac
F=$(grep -l "^class $S(" scenes/*.py | head -1)
[ -n "$F" ] || { echo "no scene file defines class $S" >&2; exit 2; }
NC=""; [ "${NOCACHE:-0}" = 1 ] && NC="--disable_caching"
.venv/bin/manim -q"$Q" $NC -v WARNING --progress_bar none --media_dir "out/media/$S" "$F" "$S"
V="out/media/$S/videos/$(basename "$F" .py)/$RES/$S.mp4"
[ -f "$V" ] || { echo "render failed: $V missing" >&2; exit 3; }
mkdir -p out/preview
ffmpeg -loglevel error -y -i "$V" -i "audio/scenes/$S.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k "out/preview/${S}_$RES.mp4"
.venv/bin/python tools/qa.py "$S" "$Q"
