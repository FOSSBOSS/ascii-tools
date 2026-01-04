# src/glyphs/registry.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple


def normalize_glyph(g: str) -> str:
    """
    Normalize only outer newlines that often come from triple-quoted strings.
    Do NOT dedent; your glyphs rely on leading spaces.
    """
    if g.startswith("\n"):
        g = g[1:]
    if g.endswith("\n"):
        g = g[:-1]
    return g


@dataclass
class GlyphRegistry:
    _glyphs: Dict[str, str] = field(default_factory=dict)

    def register(self, name: str, glyph: str) -> None:
        self._glyphs[name] = normalize_glyph(glyph)

    def register_many(self, items: Iterable[Tuple[str, str]]) -> None:
        for name, glyph in items:
            self.register(name, glyph)

    def has(self, name: str) -> bool:
        return name in self._glyphs

    def names(self) -> list[str]:
        return sorted(self._glyphs.keys())

    def get(self, name: str) -> str:
        return self._glyphs[name]
