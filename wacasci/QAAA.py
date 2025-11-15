#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QPoint
from datetime import datetime

# the repeat characters effectively lowers sensitivity, making it easer to draw
draw_string = "...oooOOO000OOOooo..." # H
draw_string1 = "...,,,---'''"         # J
draw_string2 = "[[[]]]|||///\\\\"     # K
#draw_string3 = "XXXLLLLJJJJKKK####"   # L
draw_string3 = "HACKTHEMATRIX"        # L
draw_string4 = "    "                 # Erase lol
# Expriament with unicode chars
draw_string5 = "•••→→→———≥≥≥✔✔✔"   # U-nicode
draw_string6 = "▀▀▀▄▄▄▐▐▐▌"        # U-nicode2
draw_string7 = "┌┌┐└┘├┤┬┬┴┼"       # U-nicode3
draw_string8 = "╔╔╔╗╗╚╚╚╝╝╝"       # U-nicode4

# other features to add:
# press T for text typing. escape to drawing by pressing any pallet key including E.
# how that migth work: get last known cordinate, start typing there.



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
        self.current_filename = None

        # Window setup
        self.setWindowTitle("ASCII Art Generator (Qt Transparent)")
        self.resize(self.width_chars * self.char_width, self.height_chars * self.char_height)

        # Transparent background while keeping the frame
        self.BG_Flag = True       # background flag
        self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
        self.setAutoFillBackground(False)

        # Monospace font
        self.font = QFont("Courier", 10)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        if not self.BG_Flag:
            painter.fillRect(self.rect(), QColor("white"))
        # Transparent background don't fill rect
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
            # delete trailing whitespace
            filename = f"ascii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="ascii") as f:
                for row in self.char_grid:
                    line = "".join(row)
                    # If a line contains any non-space character, trim trailing whitespace
                    if any(c != ' ' for c in line):
                        out = line.rstrip()
                    else:
                        # Completely empty line --> preserve ONE single space
                        out = " "
                    f.write(out + "\n")
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
        elif key == Qt.Key_H:
            self.draw_string = draw_string
            self.setWindowTitle(f"draw_string")
            self.setWindowTitle(f"ASCII Art Generator {draw_string}")
        elif key == Qt.Key_J:
            self.draw_string = draw_string1
            self.setWindowTitle(f"ASCII Art Generator {draw_string1}")
        elif key == Qt.Key_K:
            self.draw_string = draw_string2
            self.setWindowTitle(f"ASCII Art Generator {draw_string2}")
        elif key == Qt.Key_L:
            self.draw_string = draw_string3
            self.setWindowTitle(f"ASCII Art Generator {draw_string3}")
        elif key == Qt.Key_E:
            self.draw_string = draw_string4
            self.setWindowTitle("ASCII Art Generator ERRASING")
        #elif key == Qt.Key_T:
            # allow typing text until escape key is pressed.
            #Qt.Key_Escape:
        elif key == Qt.Key_B:
            if self.BG_Flag == False:
                self.BG_Flag = True
                self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
                
            else:
                self.BG_Flag = False
                self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
                
                
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if len(sys.argv) < 2:
        window = AsciiArtWindow(80, 80)
    elif len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [width height]")
        sys.exit(1)
    else:
        x = int(sys.argv[1]) # type cast
        y = int(sys.argv[2]) # type cast
        window = AsciiArtWindow(x, y)   
        
    sys.exit(app.exec_())
