# src/glyphs/glyphs.py
from __future__ import annotations

from typing import List, Tuple

from document import AsciiDocument, Change


def glyph_to_lines(glyph: str) -> List[str]:
    # Keep all spaces; only split on newline.
    return glyph.split("\n")


def stamp(doc: AsciiDocument, glyph: str, x0: int, y0: int) -> list[Change]:
    """
    Stamp glyph into document at (x0, y0). Returns list of changes (for undo later).
    """
    changes: list[Change] = []
    lines = glyph_to_lines(glyph)
    for dy, line in enumerate(lines):
        y = y0 + dy
        if y < 0 or y >= doc.height:
            continue
        for dx, ch in enumerate(line):
            x = x0 + dx
            if not doc.in_bounds(x, y):
                continue
            c = doc.set(x, y, ch)
            if c is not None:
                changes.append(c)
    return changes
