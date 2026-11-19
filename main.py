#!/usr/bin/env python3
"""news-image-20261118 v2 entrypoint.

Places the pre-rendered v2 broadsheet (48 stories, Wednesday 18 November
2026) at /output/entry.png, after checking the file is a well-formed
PNG of the right size. The check walks the PNG chunk structure and
verifies each chunk's CRC, so a truncated or corrupted copy is refused
instead of submitted. Standard library only, no network, no clock, no
randomness: the same bytes come out on every run.
"""
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEST = "/output/entry.png"
WANT_SIZE = (1024, 1024)
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_chunks(blob):
    """Yield (kind, payload) for each chunk in a PNG byte string."""
    if blob[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    pos = 8
    while pos + 8 <= len(blob):
        size, kind = struct.unpack(">I4s", blob[pos:pos + 8])
        payload = blob[pos + 8:pos + 8 + size]
        stored_crc, = struct.unpack(">I", blob[pos + 8 + size:pos + 12 + size])
        actual_crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError("chunk %r has a bad CRC" % kind.decode("latin-1"))
        yield kind, payload
        pos += 12 + size
        if kind == b"IEND":
            break


def verify_png(path):
    """Return (width, height) if path is a well-formed PNG of WANT_SIZE."""
    with open(path, "rb") as handle:
        blob = handle.read()
    kinds = []
    dims = None
    for kind, payload in read_chunks(blob):
        kinds.append(kind)
        if kind == b"IHDR":
            dims = struct.unpack(">II", payload[:8])
    if b"IHDR" not in kinds or b"IEND" not in kinds:
        raise ValueError("PNG is missing IHDR or IEND")
    if dims != WANT_SIZE:
        raise ValueError("expected %dx%d, got %dx%d" % (WANT_SIZE + dims))
    if len(blob) < 100000 or len(blob) > 1000000:
        raise ValueError("unexpected file size: %d bytes" % len(blob))
    return dims, len(blob)


def main():
    dims, size = verify_png(SRC)
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(SRC, "rb") as handle:
        data = handle.read()
    if len(data) != size:
        raise ValueError("entry.png changed size while reading")
    with open(DEST, "wb") as handle:
        handle.write(data)
    width, height = verify_png(DEST)[0]
    print("placed %s (%d bytes, %dx%d PNG)" % (DEST, size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
