#!/usr/bin/env bash
# Full build:  narration -> timeline -> silent scenes (frame-exact) -> concat -> master audio + music -> final mp4 + QA.
#   ./build.sh            1080p60 final       QUALITY=l ./build.sh   480p15 draft       JOBS=4 parallel renders
# Output: ../<name>.mp4 (the video folder's top level, next to thumbnails/ and youtube.md; no copy in src/),
#         out/<name>.srt, out/<name>_720p_share.mp4, out/waveform_overview.png
set -euo pipefail
cd "$(dirname "$0")"
P="$(cd .. && pwd)"                                  # videos/<slug>
NAME="$(basename "$P" | tr '-' '_')"; FINAL="$P/$NAME.mp4"
Q="${QUALITY:-h}"; JOBS="${JOBS:-4}"
case "$Q" in l) RES=480p15;; m) RES=720p30;; h) RES=1080p60;; esac

tts/.venv/bin/python tools/timeline.py                          # cached per sentence
SCENES=$(python3 -c "import json;print(' '.join(s['id'] for s in json.load(open('script/script.json'))['scenes']))")

mkdir -p out/qa
# render scenes in parallel (each has its own media dir -> no shared text-cache races)
printf "%s\n" $SCENES | xargs -P "$JOBS" -I{} sh -c 'tools/render.sh {} '"$Q"' > out/qa/{}.build.log 2>&1 && echo "ok   {}" || echo "QA!  {} (see out/qa/{}.report.txt)"'

mkdir -p out/final
: > out/final/video.txt; : > out/final/audio.txt
for S in $SCENES; do
  F=$(grep -l "^class $S(" scenes/*.py | head -1)
  echo "file '$PWD/out/media/$S/videos/$(basename "$F" .py)/$RES/$S.mp4'" >> out/final/video.txt
  echo "file '$PWD/audio/scenes/$S.wav'" >> out/final/audio.txt
done
ffmpeg -loglevel error -y -f concat -safe 0 -i out/final/video.txt -c copy -an out/final/_video.mp4
ffmpeg -loglevel error -y -f concat -safe 0 -i out/final/audio.txt -c:a pcm_s16le out/final/_voice.wav
VLEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/final/_video.mp4)
ALEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/final/_voice.wav)
echo "video ${VLEN}s  voice ${ALEN}s"
tts/.venv/bin/python tts/music.py "$ALEN" >/dev/null

ffmpeg -loglevel error -y -i out/final/_video.mp4 -i out/final/_voice.wav -i audio/bed.wav -filter_complex "\
[1:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=9,asplit=2[v][vsc];\
[2:a]volume=0.07[b];\
[b][vsc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=600[bd];\
[v][bd]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$FINAL"
cp script/captions.srt "out/$NAME.srt"
.venv/bin/python tools/waveform_overview.py
[ "$Q" = h ] && tools/share.sh "$FINAL" "out/${NAME}_720p_share.mp4"
.venv/bin/python tools/final_qa.py "$FINAL"
