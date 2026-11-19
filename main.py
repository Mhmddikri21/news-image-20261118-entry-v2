#!/usr/bin/env python3
"""news-image-20261118 v2: one broadsheet of 18 November 2026 world news.

The v2 image is pre-rendered (entry.png, 1024x1024, 48 stories): black
masthead band, a "day in numbers" strip (141 drones, 126 downed, Dow
-561, EU 45bn loan proposed, 950,000 at flood risk in Gaza, Voyager 1
at 25.9bn km), four lead cards, a 12-card grid, a bigger world map and a
32-item also-list, plus the date-check box. It supersedes the v1 entry
(55 stories, UTC timeline, no numbers strip), which scored 98.50% dev
but ranked 228 of 12,068. This entrypoint only places
that image at /output/entry.png. No network, no clock, no randomness:
the same bytes come out on every run.
"""
from pathlib import Path
import shutil
import struct

SRC = Path(__file__).resolve().parent / "entry.png"
DEST = Path("/output/entry.png")
DIMS = (1024, 1024)


def validate_png(path):
    """Check path is a PNG of the expected size; return (width, height)."""
    head = path.read_bytes()[:33]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    dims = struct.unpack(">II", head[16:24])
    if dims != DIMS:
        raise ValueError(f"expected {DIMS[0]}x{DIMS[1]}, got {dims[0]}x{dims[1]}")
    return dims


def place_entry():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DEST)
    width, height = validate_png(DEST)
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes, {width}x{height} PNG)")


if __name__ == "__main__":
    place_entry()
