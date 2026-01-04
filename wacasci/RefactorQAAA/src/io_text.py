# src/io_text.py
from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from document import AsciiDocument


def load_text(path: str, max_w: int = 500, max_h: int = 500) -> AsciiDocument:
    with open(path, "r", encoding="ascii", errors="ignore") as f:
        lines = f.read().splitlines()
    return AsciiDocument.from_lines(lines, max_w=max_w, max_h=max_h)


def default_save_name(prefix: str = "ascii_", suffix: str = ".txt") -> str:
    return f"{prefix}{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"


def save_text(doc: AsciiDocument, path: Optional[str] = None) -> str:
    if not path:
        path = default_save_name()

    lines = doc.to_lines(rstrip=True)
    with open(path, "w", encoding="ascii") as f:
        for line in lines:
            f.write(line + "\n")

    return os.path.abspath(path)
