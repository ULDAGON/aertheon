"""YouTube chapter timestamps from the frozen timeline:  python3 tools/chapters.py

Prints one line per scene, "M:SS <scene title from script.json>", starting at 0:00 (YouTube needs the first chapter at
0:00, at least three chapters, each at least 10 s). Times are floored to the second, so a chapter never starts after its
scene. Rewrite the titles for viewers (short, concrete, no scene ids) when pasting them into ../youtube.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    script = json.loads((ROOT / "script" / "script.json").read_text())
    t = 0.0
    for sc in script["scenes"]:
        dur = json.loads((ROOT / "timeline" / f"{sc['id']}.json").read_text())["duration"]
        assert dur >= 10, f"{sc['id']} is shorter than YouTube's 10 s chapter minimum"
        s = int(t)
        print(f"{s // 60}:{s % 60:02d} {sc.get('title') or sc['id']}")
        t += dur
    assert len(script["scenes"]) >= 3, "YouTube shows chapters only for three or more"


if __name__ == "__main__":
    main()
