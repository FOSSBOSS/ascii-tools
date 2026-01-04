# src/ui/help.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


HELP_TEXT = (
    "QtAwesome ASCII Arts! - Key Bindings\n\n"
    "Drawing (brush select):\n"
    "  T  - Brush 0\n"
    "  Y  - Brush 1\n"
    "  U  - Brush 2\n"
    "  I  - Brush 3\n"
    "  J  - Brush 4\n"
    "  K  - Brush 5\n"
    "  L  - Brush 6\n"
    "  M  - Brush 7\n"
    "  N  - Brush 8\n"
    "  E  - Eraser\n\n"
    "Vector tool:\n"
    "  Shift + Mouse Drag  - Preview vector line\n"
    "  release click       - Commit vector line (default)\n"
    "  Enter               - Commit pinned vector\n"
    "  Esc                 - Clear vector\n\n"
    "Controls:\n"
    "  Mouse Drag   - Draw characters\n"
    "  WASD, Arrows - Move cursor and draw\n"
    "  R            - Reset canvas\n"
    "  P            - Populate entire area with text\n"
    "  B            - Toggle background\n"
    "  C            - Toggle Show Cursor\n"
    "  Ctrl+S       - Save\n"
    "  Ctrl+O       - Open\n"
    "  Ctrl+B       - Edit brushes\n"
    "  Ctrl+P       - Control panel\n\n"
    "Color Palette:\n"
    "  1-9          - Change color\n"
    "  0            - White\n\n"
    "Glyph tiles:\n"
    "  G,V,Z,X      - Example built-in stamps\n\n"
    "Help:\n"
    "  H            - Show this help window\n"
)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Key Bindings")
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()
        label = QLabel()
        label.setText(HELP_TEXT)
        label.setStyleSheet("font-family: Courier; font-size: 16px;")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(560, 680)

    def show_or_raise(self):
        if self.isVisible():
            self.raise_()
            self.activateWindow()
        else:
            self.show()
