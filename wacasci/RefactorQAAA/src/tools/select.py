# src/tools/select.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from document import AsciiDocument


Coord = Tuple[int, int]
Rect = Tuple[int, int, int, int]  # x0,y0,x1,y1 inclusive


@dataclass
class SelectionTool:
    active: bool = False
    start: Optional[Coord] = None
    end: Optional[Coord] = None

    def clear(self) -> None:
        self.active = False
        self.start = None
        self.end = None

    def begin(self, x: int, y: int) -> None:
        self.active = True
        self.start = (x, y)
        self.end = (x, y)

    def update(self, x: int, y: int) -> None:
        if not self.active:
            return
        self.end = (x, y)

    def rect(self) -> Optional[Rect]:
        if not self.start or not self.end:
            return None
        x0, y0 = self.start
        x1, y1 = self.end
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        return (x0, y0, x1, y1)

    def copy_as_text(self, doc: AsciiDocument) -> str:
        r = self.rect()
        if not r:
            return ""
        x0, y0, x1, y1 = r
        lines = []
        for y in range(y0, y1 + 1):
            line = "".join(doc.get(x, y) for x in range(x0, x1 + 1))
            lines.append(line.rstrip() or " ")
        return "\n".join(lines)
