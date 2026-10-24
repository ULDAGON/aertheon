"""Verified, topic-specific data and shared motifs for all scenes of this video.

Put here everything more than one scene uses and that must be *right*: coordinates, constructions, datasets,
counts (numpy/mpmath, heavy results cached in data/), plus the recurring motif's class and any fixed layouts that several
scenes share, so parallel scene builders cannot drift apart. Every constructor asserts its own claims, and
`.venv/bin/python topic.py` runs a self-check. The module docstring is the API list scene builders read.
References: {{ENGINE_DIR}}/reference/riemann-hypothesis/topic.py (numerics + ErrorDial + strip layouts), {{ENGINE_DIR}}/reference/hadwiger-nelson/geom.py (geometry).
"""
import numpy as np  # noqa: F401

from common import *  # noqa: E402,F401,F403   (motif classes use the style tokens)


if __name__ == "__main__":
    print("topic.py self-check: nothing defined yet")
