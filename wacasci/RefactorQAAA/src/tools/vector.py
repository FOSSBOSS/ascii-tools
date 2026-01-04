# src/tools/vector.py
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

from document import AsciiDocument, Change


Coord = Tuple[int, int]


def bresenham(x0: int, y0: int, x1: int, y1: int) -> List[Coord]:
    points: List[Coord] = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy
    return points


def vector_char_for_angle(dx: int, dy: int) -> str:
    """
    Orientation rules:
      '_'  near horizontal
      '|'  near vertical
      '/'  up-right (positive math angle)
      '\\' down-right (negative math angle)

    Screen coords: +y is downward, so use atan2(-dy, dx).
    """
    if dx == 0 and dy == 0:
        return "_"

    ang = math.degrees(math.atan2(-dy, dx))
    abs_ang = abs(ang)

    if abs_ang <= 15 or abs_ang >= 165:
        return "_"
    if abs(abs_ang - 90) <= 15:
        return "|"
    return "\\" if ang < 0 else "/"


@dataclass
class VectorTool:
    active: bool = False
    pinned: bool = False
    start: Optional[Coord] = None
    end: Optional[Coord] = None
    points: List[Coord] = None
    char: str = "_"

    def __post_init__(self):
        if self.points is None:
            self.points = []

    def clear(self) -> None:
        self.active = False
        self.pinned = False
        self.start = None
        self.end = None
        self.points = []
        self.char = "_"

    def begin(self, x: int, y: int) -> None:
        self.active = True
        self.pinned = False
        self.start = (x, y)
        self.end = (x, y)
        self._recompute()

    def update(self, x: int, y: int) -> None:
        if not self.active:
            return
        self.end = (x, y)
        self._recompute()

    def finish(self, x: int, y: int) -> None:
        # finishing makes it not-active but still visible (pinned) until committed/cleared
        if not (self.start and (self.active or self.pinned)):
            return
        self.active = False
        self.pinned = True
        self.end = (x, y)
        self._recompute()

    def _recompute(self) -> None:
        if not self.start or not self.end:
            self.points = []
            return
        x0, y0 = self.start
        x1, y1 = self.end
        dx = x1 - x0
        dy = y1 - y0
        self.char = vector_char_for_angle(dx, dy)
        self.points = bresenham(x0, y0, x1, y1)

    def commit(self, doc: AsciiDocument) -> List[Change]:
        if not self.points:
            return []
        changes = doc.set_many(self.points, self.char)
        self.clear()
        return changes

    @property
    def length(self) -> int:
        return len(self.points)
