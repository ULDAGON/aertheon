#!/usr/bin/env bash
# Small 720p30 copy (~25-30 MB for 10 min) for messengers / phones:  tools/share.sh ../<name>.mp4 [out/<name>_720p_share.mp4]
set -euo pipefail
cd "$(dirname "$0")/.."
IN="$1"; OUT="${2:-${IN%.mp4}_720p_share.mp4}"
ffmpeg -loglevel error -y -i "$IN" -vf "scale=1280:720:flags=lanczos,fps=30" -c:v libx264 -preset slow -b:v 300k -pass 1 -passlogfile out/ffmpeg2pass -an -f null /dev/null
ffmpeg -loglevel error -y -i "$IN" -vf "scale=1280:720:flags=lanczos,fps=30" -c:v libx264 -preset slow -b:v 300k -pass 2 -passlogfile out/ffmpeg2pass -c:a aac -b:a 80k -movflags +faststart "$OUT"
rm -f out/ffmpeg2pass*
ls -la "$OUT"
