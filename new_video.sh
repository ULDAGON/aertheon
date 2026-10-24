#!/usr/bin/env bash
# Scaffold a new video:  <engine>/new_video.sh <slug> "<Working title>"
# Creates <videos>/<slug>/ and links the shared Python environments:
#   <slug>/src/          everything the pipeline works in (copy of the engine's template/: script, audio, scenes, tools, out/)
#   <slug>/thumbnails/   the three thumbnail PNGs (written by src/thumbnails/make_thumbnails.py)
#   <slug>/youtube.md    three titles + the description (from template/youtube.md)
#   <slug>/<name>.mp4    the final video (written by src/build.sh; no copy inside src/)
# <videos> defaults to the "videos" folder next to the engine; override with AERTHEON_VIDEOS=/abs/path.
# Prints the new src folder ($V in PIPELINE.md). Nothing is written inside the engine.
set -euo pipefail
ENGINE="$(cd "$(dirname "$0")" && pwd)"
VIDEOS="${AERTHEON_VIDEOS:-$(dirname "$ENGINE")/videos}"
SLUG="${1:?usage: new_video.sh <slug> \"<title>\"}"; TITLE="${2:-$SLUG}"
[[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "slug must be kebab-case: $SLUG" >&2; exit 2; }
P="$VIDEOS/$SLUG"; V="$P/src"
[ -e "$P" ] && { echo "exists: $P" >&2; exit 2; }
"$ENGINE/setup.sh" >/dev/null 2>&1 || { echo "setup.sh failed; run it directly to see why" >&2; exit 3; }
mkdir -p "$V" "$P/thumbnails"
rsync -a --exclude __pycache__ --exclude .DS_Store "$ENGINE/template/" "$V/"   # no engine bytecode in the video
find "$V" -name .gitkeep -delete
mv "$V/youtube.md" "$P/youtube.md"
ln -s "$ENGINE/.venv" "$V/.venv"
ln -s "$ENGINE/tts/.venv" "$V/tts/.venv"
mkdir -p "$V"/{audio,timeline,out}
python3 - "$P" "$TITLE" "$ENGINE" <<'PY'
import sys, pathlib
v, title, engine = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
for p in v.rglob("*"):
    if p.is_file() and p.suffix in (".md", ".py", ".sh"):
        s = p.read_text()
        t = s.replace("{{TITLE}}", title).replace("{{VIDEO_DIR}}", str(v / "src")).replace("{{ENGINE_DIR}}", engine)
        if t != s:
            p.write_text(t)
PY
echo "$V"
