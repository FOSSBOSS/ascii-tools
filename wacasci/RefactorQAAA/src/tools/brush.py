# src/tools/brush.py
from __future__ import annotations

from dataclasses import dataclass

from document import AsciiDocument, Change


@dataclass
class BrushTool:
    pattern: str
    index: int = 0

    def next_char(self) -> str:
        if not self.pattern:
            return " "
        ch = self.pattern[self.index % len(self.pattern)]
        self.index += 1
        return ch

    def apply_point(self, doc: AsciiDocument, x: int, y: int) -> Change | None:
        ch = self.next_char()
        return doc.set(x, y, ch)
