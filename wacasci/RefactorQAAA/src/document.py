# src/document.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


Coord = Tuple[int, int]
Change = Tuple[int, int, str, str]  # x, y, old, new


@dataclass
class AsciiDocument:
    width: int
    height: int
    grid: List[List[str]]

    @classmethod
    def blank(cls, width: int, height: int, fill: str = " ") -> "AsciiDocument":
        width = max(1, int(width))
        height = max(1, int(height))
        grid = [[fill] * width for _ in range(height)]
        return cls(width=width, height=height, grid=grid)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y):
            return " "
        return self.grid[y][x]

    def set(self, x: int, y: int, ch: str) -> Change | None:
        """Set a single cell. Returns a Change tuple for undo, or None if no-op/out-of-bounds."""
        if not self.in_bounds(x, y):
            return None
        if ch is None or ch == "":
            ch = " "
        ch = ch[0]

        old = self.grid[y][x]
        if old == ch:
            return None

        self.grid[y][x] = ch
        return (x, y, old, ch)

    def set_many(self, coords: Iterable[Coord], ch: str) -> List[Change]:
        changes: List[Change] = []
        for (x, y) in coords:
            c = self.set(x, y, ch)
            if c is not None:
                changes.append(c)
        return changes

    def clear(self, fill: str = " ") -> None:
        for y in range(self.height):
            row = self.grid[y]
            for x in range(self.width):
                row[x] = fill

    def resize_preserve(self, new_w: int, new_h: int, fill: str = " ") -> None:
        """Resize while preserving the upper-left region of content."""
        new_w = max(1, int(new_w))
        new_h = max(1, int(new_h))

        old_grid = self.grid
        old_w = self.width
        old_h = self.height

        new_grid = [[fill] * new_w for _ in range(new_h)]

        for y in range(min(new_h, old_h)):
            for x in range(min(new_w, old_w)):
                new_grid[y][x] = old_grid[y][x]

        self.width = new_w
        self.height = new_h
        self.grid = new_grid

    def populate(self, s: str) -> None:
        if not s:
            return
        idx = 0
        n = len(s)
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = s[idx % n]
                idx += 1

    def to_lines(self, rstrip: bool = True) -> List[str]:
        lines: List[str] = []
        for row in self.grid:
            line = "".join(row)
            if rstrip:
                # Keep at least one character so empty rows survive
                line = line.rstrip() or " "
            lines.append(line)
        return lines

    @classmethod
    def from_lines(cls, lines: List[str], max_w: int = 500, max_h: int = 500) -> "AsciiDocument":
        if not lines:
            return cls.blank(1, 1)

        height = min(len(lines), max_h)
        width = min(max((len(l) for l in lines[:height]), default=1), max_w)

        doc = cls.blank(width, height)
        for y in range(height):
            line = lines[y]
            for x in range(min(len(line), width)):
                doc.grid[y][x] = line[x]
        return doc
