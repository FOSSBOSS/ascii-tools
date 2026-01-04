# src/glyphs/transforms.py
from __future__ import annotations

from typing import Dict

# Mirrors need a swap map so glyphs look correct.
MIRROR_H: Dict[str, str] = {
    "/": "\\",
    "\\": "/",
    "(": ")",
    ")": "(",
    "[": "]",
    "]": "[",
    "{": "}",
    "}": "{",
    "<": ">",
    ">": "<",
}

MIRROR_V: Dict[str, str] = {
    "/": "\\",
    "\\": "/",
    "^": "v",
    "v": "^",
}


def mirror_horizontal(glyph: str) -> str:
    lines = glyph.split("\n")
    out = []
    for line in lines:
        rev = line[::-1]
        rev = "".join(MIRROR_H.get(ch, ch) for ch in rev)
        out.append(rev)
    return "\n".join(out)


def mirror_vertical(glyph: str) -> str:
    lines = glyph.split("\n")[::-1]
    out = []
    for line in lines:
        line2 = "".join(MIRROR_V.get(ch, ch) for ch in line)
        out.append(line2)
    return "\n".join(out)
