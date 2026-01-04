# src/ui/window.py
from __future__ import annotations

import os
import sys
from dataclasses import asdict

os.environ["QT_LOGGING_RULES"] = "*.warning=false"  # quiet Qt warnings

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QFont, QColor, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QInputDialog, QShortcut
)

from document import AsciiDocument
import io_text

from glyphs.registry import GlyphRegistry
from glyphs.builtins import BUILTIN_GLYPHS
from glyphs.glyphs import stamp as stamp_glyph

from tools.brush import BrushTool
from tools.vector import VectorTool
from tools.select import SelectionTool  # scaffold, not fully wired yet

from ui.help import HelpDialog
from ui.brush_editor import BrushEditorDialog
from ui.control_panel import ControlPanelDialog, ControlState


class AsciiArtWindow(QWidget):
    def __init__(self, width=80, height=80):
        super().__init__()

        # document + tools
        self.doc = AsciiDocument.blank(width, height)
        self.brush_patterns = {
            "Brush T": "...oooOOO000OOOooo...",
            "Brush Y": "H E L P  M Y   T E X T  E D I T O R  I S  B U S T E D",
            "Brush U": "[[[]]]|||///\\\\",
            "Brush I": "HACKTHEMATRIX",
            "Brush J": "//",
            "Brush K": "]]||",
            "Brush L": "\\\\",
            "Brush M": ">>><<<",
            "Brush N": "-=+",
            "Eraser": "    ",
        }
        self.active_brush_name = "Brush T"
        self.brush = BrushTool(self.brush_patterns[self.active_brush_name])

        self.vector = VectorTool()
        self.vector_commit_on_release = True

        self.select = SelectionTool()  # placeholder

        # glyphs
        self.glyphs = GlyphRegistry()
        self.glyphs.register_many(BUILTIN_GLYPHS.items())

        # display settings
        self.text_color = QColor("black")
        self.char_width = 8
        self.char_height = 24

        self.cursor_x = 0
        self.cursor_y = 0
        self.show_cursor = False

        self.bg_transparent = True
        self.setAttribute(Qt.WA_TranslucentBackground, self.bg_transparent)
        self.setAutoFillBackground(False)

        self.font = QFont("Courier", 14)
        self.setMouseTracking(True)
        self.setMinimumSize(self.char_width * 10, self.char_height * 1)

        self.base_title = "QtAwesome ASCII Arts!"
        self.update_title()

        # shortcuts
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save_file)
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.open_file)
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self.open_brush_editor)
        QShortcut(QKeySequence("Ctrl+P"), self, activated=self.open_control_panel)

        self.resize(self.doc.width * self.char_width, self.doc.height * self.char_height)
        self.show()

    # ---------------- coordinate helpers ----------------

    def grid_pos_from_pixel(self, pos: QPoint) -> tuple[int, int]:
        x = pos.x() // self.char_width
        y = pos.y() // self.char_height
        x = max(0, min(self.doc.width - 1, x))
        y = max(0, min(self.doc.height - 1, y))
        return x, y

    # ---------------- title ----------------

    def update_title(self):
        if self.vector.points and (self.vector.active or self.vector.pinned):
            self.setWindowTitle(
                f"{self.base_title}  [vector len={self.vector.length} char='{self.vector.char}']"
            )
        else:
            self.setWindowTitle(self.base_title)

    # ---------------- dialogs ----------------

    def open_help(self):
        if not hasattr(self, "_help"):
            self._help = HelpDialog(self)
        self._help.show_or_raise()

    def open_brush_editor(self):
        if not hasattr(self, "_brush_editor"):
            self._brush_editor = BrushEditorDialog(
                self,
                get_brushes=lambda: dict(self.brush_patterns),
                set_brush=self.set_brush_pattern,
            )
        self._brush_editor.show_or_raise()

    def open_control_panel(self):
        if not hasattr(self, "_control_panel"):
            self._control_panel = ControlPanelDialog(
                self,
                get_state=self.get_control_state,
                apply_state=self.apply_control_state,
            )
        self._control_panel.show_or_raise()

    def get_control_state(self) -> ControlState:
        return ControlState(
            char_width=self.char_width,
            char_height=self.char_height,
            show_cursor=self.show_cursor,
            bg_transparent=self.bg_transparent,
            vector_commit_on_release=self.vector_commit_on_release,
        )

    def apply_control_state(self, st: ControlState) -> None:
        self.char_width = max(2, int(st.char_width))
        self.char_height = max(4, int(st.char_height))
        self.show_cursor = bool(st.show_cursor)
        self.bg_transparent = bool(st.bg_transparent)
        self.vector_commit_on_release = bool(st.vector_commit_on_release)

        self.setAttribute(Qt.WA_TranslucentBackground, self.bg_transparent)
        self.update_grid_from_window()
        self.update()

    # ---------------- brush management ----------------

    def set_brush_pattern(self, name: str, pattern: str) -> None:
        self.brush_patterns[name] = pattern
        if self.active_brush_name == name:
            self.brush.pattern = pattern
        self.update()

    def set_active_brush(self, name: str) -> None:
        if name not in self.brush_patterns:
            return
        self.active_brush_name = name
        self.brush.pattern = self.brush_patterns[name]
        self.base_title = f"QtAwesome ASCII Arts!  [{name}]"
        self.update_title()

    # ---------------- file I/O ----------------

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open ASCII Text File", "", "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        self.doc = io_text.load_text(path, max_w=500, max_h=500)
        self.vector.clear()
        self.resize(self.doc.width * self.char_width, self.doc.height * self.char_height)
        self.base_title = f"QtAwesome ASCII Arts!  [loaded: {os.path.basename(path)}]"
        self.update_title()
        self.update()

    def save_file(self):
        out_path = io_text.save_text(self.doc)
        self.base_title = f"QtAwesome ASCII Arts!  [saved: {os.path.basename(out_path)}]"
        self.update_title()

    # ---------------- grid resize ----------------

    def update_grid_from_window(self):
        new_w = max(1, self.width() // self.char_width)
        new_h = max(1, self.height() // self.char_height)
        if new_w != self.doc.width or new_h != self.doc.height:
            self.doc.resize_preserve(new_w, new_h)
            # clamp vector endpoints if needed
            if self.vector.start:
                x, y = self.vector.start
                self.vector.start = (max(0, min(self.doc.width - 1, x)),
                                     max(0, min(self.doc.height - 1, y)))
            if self.vector.end:
                x, y = self.vector.end
                self.vector.end = (max(0, min(self.doc.width - 1, x)),
                                   max(0, min(self.doc.height - 1, y)))
            if self.vector.start and self.vector.end:
                self.vector._recompute()

    def resizeEvent(self, event):
        self.update_grid_from_window()
        self.update()

    # ---------------- drawing ----------------

    def draw_at(self, x: int, y: int):
        self.brush.apply_point(self.doc, x, y)
        self.update()

    # ---------------- paint ----------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        painter.setRenderHint(QPainter.TextAntialiasing)

        if not self.bg_transparent:
            painter.fillRect(self.rect(), QColor("white"))

        # permanent grid
        painter.setPen(self.text_color)
        for y in range(self.doc.height):
            row = self.doc.grid[y]
            for x in range(self.doc.width):
                ch = row[x]
                if ch.strip():
                    painter.drawText(x * self.char_width, (y + 1) * self.char_height, ch)

        # vector overlay (non-permanent unless committed)
        if self.vector.points and (self.vector.active or self.vector.pinned):
            painter.save()
            painter.setPen(QColor("darkGray"))
            for x, y in self.vector.points:
                if self.doc.in_bounds(x, y):
                    painter.drawText(x * self.char_width, (y + 1) * self.char_height, self.vector.char)
            painter.restore()

        # cursor
        if self.show_cursor:
            painter.setPen(QColor("red"))
            painter.drawRect(
                self.cursor_x * self.char_width,
                self.cursor_y * self.char_height,
                self.char_width,
                self.char_height,
            )

    # ---------------- mouse ----------------

    def mouseMoveEvent(self, event):
        self.cursor_x = event.x() // self.char_width
        self.cursor_y = event.y() // self.char_height

        if event.buttons() & Qt.LeftButton:
            if self.vector.active:
                x, y = self.grid_pos_from_pixel(event.pos())
                self.vector.update(x, y)
                self.update_title()
            else:
                x, y = self.grid_pos_from_pixel(event.pos())
                self.brush.apply_point(self.doc, x, y)

        self.update()

    def mousePressEvent(self, event):
        self.cursor_x = event.x() // self.char_width
        self.cursor_y = event.y() // self.char_height

        if event.button() == Qt.LeftButton:
            x, y = self.grid_pos_from_pixel(event.pos())

            if event.modifiers() & Qt.ShiftModifier:
                self.vector.begin(x, y)
                self.update_title()
            else:
                self.brush.apply_point(self.doc, x, y)

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.vector.active:
            x, y = self.grid_pos_from_pixel(event.pos())
            self.vector.finish(x, y)

            if self.vector_commit_on_release:
                self.vector.commit(self.doc)
            else:
                # leave it pinned until Enter commits
                pass

            self.update_title()
            self.update()

    # ---------------- glyph tiles ----------------

    def stamp_glyph(self, name: str):
        if not self.glyphs.has(name):
            return
        glyph = self.glyphs.get(name)
        stamp_glyph(self.doc, glyph, self.cursor_x, self.cursor_y)
        self.base_title = f"QtAwesome ASCII Arts!  [stamp: {name}]"
        self.update_title()
        self.update()

    # ---------------- keys ----------------

    def keyPressEvent(self, event):
        key = event.key()

        # clear vector
        if key == Qt.Key_Escape:
            self.vector.clear()
            self.update_title()
            self.update()
            return

        # commit vector
        if key in (Qt.Key_Return, Qt.Key_Enter):
            if self.vector.points and (self.vector.active or self.vector.pinned):
                self.vector.commit(self.doc)
                self.update_title()
                self.update()
                return

        # reset
        if key == Qt.Key_R:
            self.doc.clear()
            self.brush.index = 0
            self.vector.clear()
            self.base_title = "QtAwesome ASCII Arts!  [reset]"
            self.update_title()
            self.update()
            return

        # colors
        if key == Qt.Key_1:
            self.text_color = QColor("black")
        elif key == Qt.Key_2:
            self.text_color = QColor("red")
        elif key == Qt.Key_3:
            self.text_color = QColor("blue")
        elif key == Qt.Key_4:
            self.text_color = QColor("green")
        elif key == Qt.Key_5:
            self.text_color = QColor("purple")
        elif key == Qt.Key_6:
            self.text_color = QColor("orange")
        elif key == Qt.Key_7:
            self.text_color = QColor("yellow")
        elif key == Qt.Key_8:
            self.text_color = QColor("cyan")
        elif key == Qt.Key_9:
            self.text_color = QColor("magenta")
        elif key == Qt.Key_0:
            self.text_color = QColor("white")

        # brush selection
        elif key == Qt.Key_T:
            self.set_active_brush("Brush T")
        elif key == Qt.Key_Y:
            self.set_active_brush("Brush Y")
        elif key == Qt.Key_U:
            self.set_active_brush("Brush U")
        elif key == Qt.Key_I:
            self.set_active_brush("Brush I")
        elif key == Qt.Key_J:
            self.set_active_brush("Brush J")
        elif key == Qt.Key_K:
            self.set_active_brush("Brush K")
        elif key == Qt.Key_L:
            self.set_active_brush("Brush L")
        elif key == Qt.Key_M:
            self.set_active_brush("Brush M")
        elif key == Qt.Key_N:
            self.set_active_brush("Brush N")
        elif key == Qt.Key_E:
            self.set_active_brush("Eraser")

        # WASD / arrows draw
        elif key in (Qt.Key_W, Qt.Key_Up):
            self.cursor_y = max(0, self.cursor_y - 1)
            self.draw_at(self.cursor_x, self.cursor_y)
            return
        elif key in (Qt.Key_S, Qt.Key_Down):
            self.cursor_y = min(self.doc.height - 1, self.cursor_y + 1)
            self.draw_at(self.cursor_x, self.cursor_y)
            return
        elif key in (Qt.Key_A, Qt.Key_Left):
            self.cursor_x = max(0, self.cursor_x - 1)
            self.draw_at(self.cursor_x, self.cursor_y)
            return
        elif key in (Qt.Key_D, Qt.Key_Right):
            self.cursor_x = min(self.doc.width - 1, self.cursor_x + 1)
            self.draw_at(self.cursor_x, self.cursor_y)
            return

        # help
        elif key == Qt.Key_H:
            self.open_help()

        # populate
        elif key == Qt.Key_P:
            string, ok = QInputDialog.getText(self, "Populate Text area", "Type the characters to fill area:")
            if ok and string:
                self.doc.populate(string)
                self.update()

        # background toggle
        elif key == Qt.Key_B:
            self.bg_transparent = not self.bg_transparent
            self.setAttribute(Qt.WA_TranslucentBackground, self.bg_transparent)
            self.update()

        # cursor toggle
        elif key == Qt.Key_C:
            self.show_cursor = not self.show_cursor
            self.update()

        # glyph tiles (demo)
        elif key == Qt.Key_G:
            self.stamp_glyph("Tile1")
        elif key == Qt.Key_V:
            self.stamp_glyph("Tile2")
        elif key == Qt.Key_Z:
            self.stamp_glyph("Tile3")
        elif key == Qt.Key_X:
            self.stamp_glyph("Tile4")

        self.update()


def main(argv: list[str]) -> int:
    app = QApplication(argv)

    if len(argv) < 2:
        win = AsciiArtWindow(80, 80)
        print("Optional")
        print(f"Usage: {argv[0]} [width height]")
    elif len(argv) != 3:
        print(f"Usage: {argv[0]} [width height]")
        return 1
    else:
        w = max(1, int(argv[1]))
        h = max(1, int(argv[2]))
        win = AsciiArtWindow(w, h)

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
