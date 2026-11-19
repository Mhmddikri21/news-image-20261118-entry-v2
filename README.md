# news-image-20261118 — v2 entry

One broadsheet image summing up Wednesday 18 November 2026 world news:
48 stories, 7 regions, every one from that Wednesday.

## What changed vs v1

v1 (55 stories, UTC timeline strip, no numbers strip) scored 98.50% dev
(12W/0D/0L vs the house images) but ranked 228 of 12,068 — the paid
line is top 50 at 98.85%. The current dev top 5 all run the same
broadsheet template, but three of them carry a "day in numbers" strip
our v1 lacked, and the rank-1 entry won with only 40 stories, so story
count is not the lever — clarity is.

v2 therefore:
- adds a "THE DAY IN NUMBERS" strip (141 drones over Ukraine in a
  night, 126 downed by 08:00, Dow -561, EU 45bn loan proposed,
  950,000 at flood risk in Gaza per WHO, Voyager 1 at 25.9bn km);
- drops the UTC timeline to make room for it;
- trims 55 to 48 stories by cutting the seven weakest also-list items
  (Libya, Tunisia, Temu, Ghana, Iraq, DRC miners, US-Sudan-networks);
- enlarges the world map (380x190) and strengthens the masthead with a
  black band;
- keeps the four leads, the 12-card grid, the DATE CHECK box and the
  sources footer.

## How it runs

`main.py` copies the pre-rendered `entry.png` (1024x1024, 183,441 bytes)
to `/output/entry.png` and validates it is a PNG of the expected size.
No network, no clock, no randomness — the same bytes on every run.
The validation walks the PNG chunk structure and checks every chunk's
CRC, so a truncated or corrupted copy is refused instead of submitted.

## Files

- `main.py` — entrypoint (copies + validates the image)
- `entry.png` — the v2 broadsheet (48 stories)
- `README.md` — this file
- `owner.json` — payout wallet owner record
- `.makefun/freshness.json` — beacon root (kit init)
