#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QPoint
from datetime import datetime
"""
The limit of tkinter is transparency. So you have to use QT.
This app is the same functionaly as AAA.py, but offers transparency.
So you can trace out ascii arts. 

Dont do any diabolical stuff with this app pls.

"""

draw_string = ".oO0Oo."

class AsciiArtWindow(QWidget):
    def __init__(self, width=80, height=80):
        super().__init__()
        self.width_chars = width
        self.height_chars = height
        self.char_grid = [[' '] * width for _ in range(height)]
        self.text_color = QColor("black")
        self.draw_string = draw_string
        self.draw_index = 0
        self.char_width = 8
        self.char_height = 14

        # Window setup
        self.setWindowTitle("ASCII Art Generator (Qt Transparent)")
        self.resize(self.width_chars * self.char_width, self.height_chars * self.char_height)

        # Transparent background while keeping the frame
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        # Monospace font
        self.font = QFont("Courier", 10)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)

        # Transparent background — don't fill rect
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.text_color)

        for y in range(self.height_chars):
            for x in range(self.width_chars):
                char = self.char_grid[y][x]
                if char.strip():
                    painter.drawText(
                        x * self.char_width,
                        (y + 1) * self.char_height,
                        char
                    )

    def mouseMoveEvent(self, event):
        self.draw_char(event.pos())
        self.update()

    def mousePressEvent(self, event):
        self.draw_char(event.pos())
        self.update()

    def draw_char(self, pos: QPoint):
        x = pos.x() // self.char_width
        y = pos.y() // self.char_height
        if 0 <= x < self.width_chars and 0 <= y < self.height_chars:
            char = self.draw_string[self.draw_index % len(self.draw_string)]
            self.char_grid[y][x] = char
            self.draw_index += 1

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_R:
            self.char_grid = [[' '] * self.width_chars for _ in range(self.height_chars)]
            self.draw_index = 0
            self.update()
        elif key == Qt.Key_S:
            filename = f"ascii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="ascii") as f:
                for row in self.char_grid:
                    f.write("".join(row) + "\n")
            print(f"ASCII art saved to {filename}")
        elif key == Qt.Key_1:
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
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AsciiArtWindow(80, 80)
    sys.exit(app.exec_())
