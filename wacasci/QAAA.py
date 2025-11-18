#!/usr/bin/env python3
import sys
import os
os.environ["QT_LOGGING_RULES"] = "*.warning=false"  # STFU Qt warnings

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QInputDialog,
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QScrollArea, QShortcut
)
from PyQt5.QtGui import QPainter, QFont, QColor, QKeySequence
from PyQt5.QtCore import Qt, QPoint
from datetime import datetime


draw_string0 = "...oooOOO000OOOooo..." # T
draw_string1 = "01010100 010"          # Y
draw_string2 = "[[[]]]|||///\\\\"      # U
draw_string3 = "HACKTHEMATRIX"         # I
draw_string4 = "//"                    # J
draw_string5 = "]]||"                  # K
draw_string6 = "\\\\"                  # L
draw_string7 = ">>><<<"                # M
draw_string8 = "-=+"                   # N
draw_string9 = "    "                  # E Erase


# Stamps: predefined text based tool tips


class AsciiArtWindow(QWidget):
    def __init__(self, width=80, height=80):
        super().__init__()

        # Ctrl+S Save
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save_file)
        # Ctrl+O Open 
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.open_file)
        # Ctrl+B Edit Brushes
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self.brush_editor)
        # Ctrl+G Control Panel
        #QShortcut(QKeySequence("Ctrl+G"), self, activated=self.control_panel)
        
        
        self.glyphs = {
        "Tile1": r"""
    \  \/  /
    /  /\  \
    """.lstrip("\n"),

        "Tile2": r"""
       __
     /    \
     \____/
    """.lstrip("\n"),
    }
        
        
        # Tile Conditionals
        # you need to update the event.pos() by h,w of the tile. .. however that might be done.
        # wasd, arrows work, and if you set the curror you can kinda guess where stuff is.
        self.active_tile = None
        self.tile_dragging = False

        
        
        # Brushes
        self.draw_string0 = draw_string0
        self.draw_string1 = draw_string1
        self.draw_string2 = draw_string2
        self.draw_string3 = draw_string3
        self.draw_string4 = draw_string4
        self.draw_string5 = draw_string5
        self.draw_string6 = draw_string6
        self.draw_string7 = draw_string7
        self.draw_string8 = draw_string8
        self.draw_string9 = draw_string9 # add more later

        # Current active brush
        self.draw_string = self.draw_string0

        # Canvas/grid setup
        self.width_chars = width
        self.height_chars = height
        self.char_grid = [[' '] * width for _ in range(height)]
        self.text_color = QColor("black")
        self.draw_index = 0
        self.char_width = 8
        self.char_height = 14
        self.current_filename = None
        self.scroll_parent = None

        # Cursor for WASD movement
        self.cursor_x = 0
        self.cursor_y = 0

        # Window setup
        self.setWindowTitle("QtAwesome ASCII Arts!")
        self.resize(self.width_chars * self.char_width,
                    self.height_chars * self.char_height)

        # Transparent background while keeping the frame
        self.BG_Flag = True
        self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
        self.setAutoFillBackground(False)
        
        # Show Cursor
        self.Show_Cursor = False
        
        
        # Monospace font
        self.font = QFont("Courier", 10)
        self.show()

        # Minimum size so manual resizing doesn't collapse it
        self.setMinimumSize(self.char_width * 10, self.char_height * 1)

    # Brush editor
    def brush_editor(self):
        # If already open
        if hasattr(self, "brush_window") and self.brush_window.isVisible():
            self.brush_window.raise_()
            return

        self.brush_window = QDialog(self)
        self.brush_window.setWindowTitle("Edit Brushes")
        self.brush_window.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()

        def make_row(label, getter, setter):
            row = QHBoxLayout()
            lbl = QLabel(label)
            edit = QLineEdit(getter())
            btn = QPushButton("Save")

            def save():
                new_value = edit.text()
                setter(new_value)
                print(f"{label} updated to: {new_value}")

                # If this brush is currently active, keep drawing with updated pattern
                if label.startswith("Brush T") and self.draw_string == self.draw_string0:
                    self.draw_string = self.draw_string0
                elif label.startswith("Brush Y") and self.draw_string == self.draw_string1:
                    self.draw_string = self.draw_string1
                elif label.startswith("Brush U") and self.draw_string == self.draw_string2:
                    self.draw_string = self.draw_string2
                elif label.startswith("Brush I") and self.draw_string == self.draw_string3:
                    self.draw_string = self.draw_string3
                elif label.startswith("Brush J") and self.draw_string == self.draw_string4:
                    self.draw_string = self.draw_string4
                elif label.startswith("Brush K") and self.draw_string == self.draw_string5:
                    self.draw_string = self.draw_string5
                elif label.startswith("Brush L") and self.draw_string == self.draw_string6:
                    self.draw_string = self.draw_string6
                elif label.startswith("Brush M") and self.draw_string == self.draw_string7:
                    self.draw_string = self.draw_string7
                elif label.startswith("Brush N") and self.draw_string == self.draw_string8:
                    self.draw_string = self.draw_string8
                elif label.startswith("Eraser") and self.draw_string == self.draw_string9:
                    self.draw_string = self.draw_string9

            btn.clicked.connect(save)

            row.addWidget(lbl)
            row.addWidget(edit)
            row.addWidget(btn)
            return row

        layout.addLayout(make_row("Brush T:", lambda: self.draw_string0, lambda v: setattr(self, "draw_string0", v)))
        layout.addLayout(make_row("Brush Y:", lambda: self.draw_string1, lambda v: setattr(self, "draw_string1", v)))
        layout.addLayout(make_row("Brush U:", lambda: self.draw_string2, lambda v: setattr(self, "draw_string2", v)))
        layout.addLayout(make_row("Brush I:", lambda: self.draw_string3, lambda v: setattr(self, "draw_string3", v)))
        layout.addLayout(make_row("Brush J:", lambda: self.draw_string4, lambda v: setattr(self, "draw_string4", v)))
        layout.addLayout(make_row("Brush K:", lambda: self.draw_string5, lambda v: setattr(self, "draw_string5", v)))
        layout.addLayout(make_row("Brush L:", lambda: self.draw_string6, lambda v: setattr(self, "draw_string6", v)))
        layout.addLayout(make_row("Brush M:", lambda: self.draw_string7, lambda v: setattr(self, "draw_string7", v)))
        layout.addLayout(make_row("Brush N:", lambda: self.draw_string8, lambda v: setattr(self, "draw_string8", v)))
        layout.addLayout(make_row("Eraser:",  lambda: self.draw_string9, lambda v: setattr(self, "draw_string9", v)))

        self.brush_window.setLayout(layout)
        self.brush_window.resize(600, 240)
        self.brush_window.show()

    # ---------- Drawing helpers ----------

    def draw_at_cursor(self):
        if 0 <= self.cursor_x < self.width_chars and 0 <= self.cursor_y < self.height_chars:
            char = self.draw_string[self.draw_index % len(self.draw_string)]
            self.char_grid[self.cursor_y][self.cursor_x] = char
            self.draw_index += 1
            self.update()

    # Track mouse position only (no drawing on move by default)
    def mouseMoveEvent(self, event):
        self.cursor_x = event.x() // self.char_width
        self.cursor_y = event.y() // self.char_height
        if event.buttons() & Qt.LeftButton:
            self.draw_char(event.pos())
        self.update()

    def mousePressEvent(self, event):
        # Update cursor first
        self.cursor_x = event.x() // self.char_width
        self.cursor_y = event.y() // self.char_height

        # Draw a point
        if event.button() == Qt.LeftButton:
            self.draw_char(event.pos())

        self.update()


    def draw_char(self, pos: QPoint):
        x = pos.x() // self.char_width
        y = pos.y() // self.char_height
        if 0 <= x < self.width_chars and 0 <= y < self.height_chars:
            char = self.draw_string[self.draw_index % len(self.draw_string)]
            self.char_grid[y][x] = char
            self.draw_index += 1

    # ---------- Help & file I/O ----------

    def show_help(self):
        if hasattr(self, "help_window") and self.help_window.isVisible():
            self.help_window.raise_()
            self.help_window.activateWindow()
            return

        self.help_window = QDialog(self)
        self.help_window.setWindowTitle("Key Bindings")
        self.help_window.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()
        label = QLabel()
        label.setText(
            "Awesome ASCII Art Generator - Key Bindings\n\n"
            "Drawing:\n"
            "  T  - Brush 0\n"
            "  Y  - Brush 1\n"
            "  U  - Brush 2\n"
            "  I  - Brush 3\n"
            "  J  - Brush 4\n"
            "  K  - Brush 5\n"
            "  L  - Brush 6\n"
            "  M  - Brush 7\n"
            "  N  - Brush 8\n"
            "  E  - Eraser\n"
            "\n"
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
            "\n"
            "Color Palette:\n"
            "  1-9          - Change color\n"
            "  0            - White\n"
            "\n"
            "Help:\n"
            "  H            - Show this help window\n"
        )

        label.setStyleSheet("font-family: Courier; font-size: 16px;")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(label)
        self.help_window.setLayout(layout)
        self.help_window.resize(450, 500)
        self.help_window.show()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open ASCII Text File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return

        max_w = 500
        max_h = 500

        with open(path, "r", encoding="ascii", errors="ignore") as f:
            lines = f.read().splitlines()

        if not lines:
            return

        max_width = max(len(line) for line in lines)
        height = len(lines)

        capped_width = min(max_width, max_w)
        capped_height = min(height, max_h)

        self.width_chars = capped_width
        self.height_chars = capped_height

        self.char_grid = [[' ' for _ in range(self.width_chars)]
                          for _ in range(self.height_chars)]

        for y in range(self.height_chars):
            line = lines[y]
            for x in range(min(len(line), self.width_chars)):
                self.char_grid[y][x] = line[x]

        self.update()
        print(f"Loaded file: {path}")

    def save_file(self):
        filename = f"ascii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="ascii") as f:
            for row in self.char_grid:
                line = "".join(row)
                if any(c != ' ' for c in line):
                    out = line.rstrip()
                else:
                    out = " "
                f.write(out + "\n")
        print(f"ASCII art saved to: {filename}")

    # ---------- Layout / grid management ----------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        if not self.BG_Flag:
            painter.fillRect(self.rect(), QColor("white"))
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.text_color)

        for y in range(self.height_chars):
            for x in range(self.width_chars):
                char = self.char_grid[y][x]
                if char.strip():
                    painter.drawText( x * self.char_width, (y + 1) * self.char_height, char)

        if self.Show_Cursor:
            # Optional: draw cursor rectangle
            painter.setPen(QColor("red"))
            painter.drawRect(
                self.cursor_x * self.char_width,
                self.cursor_y * self.char_height,
                self.char_width,
                self.char_height
            )
        

    def resizeEvent(self, event):
        self.update_grid()
        self.update()

    def update_grid(self):
        new_w = max(1, self.width() // self.char_width)
        new_h = max(1, self.height() // self.char_height)

        if new_w != self.width_chars or new_h != self.height_chars:
            old_grid = self.char_grid
            old_h = len(old_grid)
            old_w = len(old_grid[0]) if old_grid else 0

            self.width_chars = new_w
            self.height_chars = new_h

            new_grid = [[' '] * new_w for _ in range(new_h)]
            for y in range(min(new_h, old_h)):
                for x in range(min(new_w, old_w)):
                    new_grid[y][x] = old_grid[y][x]

            self.char_grid = new_grid

    def populate(self, s):
        if not s:
            return
        length = len(s)
        index = 0
        for y in range(self.height_chars):
            for x in range(self.width_chars):
                self.char_grid[y][x] = s[index % length]
                index += 1
    
    # ---------- Draw Glpyphs  ----------
    # triple quotes have trailing newline. 
    # r raw string / tripple quotes to presurve white space, and special chars dont need escapes                                       
    def draw_tile(self, name):
        if name not in self.glyphs:
            return

        lines = self.glyphs[name].split("\n")
        for dy, line in enumerate(lines):
            for dx, ch in enumerate(line):
                x = self.cursor_x + dx
                y = self.cursor_y + dy
                if 0 <= x < self.width_chars and 0 <= y < self.height_chars:
                    self.char_grid[y][x] = ch
        self.update()
                                  
                                      
    # ---------- Key handling ----------

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_R:
            self.char_grid = [[' '] * self.width_chars for _ in range(self.height_chars)]
            self.draw_index = 0
            self.update()

        # Color keys
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

        # Brush selection
        elif key == Qt.Key_T:
            self.draw_string = self.draw_string0
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_Y:
            self.draw_string = self.draw_string1
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_U:
            self.draw_string = self.draw_string2
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_I:
            self.draw_string = self.draw_string3
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_J:
            self.draw_string = self.draw_string4
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_K:
            self.draw_string = self.draw_string5
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_L:
            self.draw_string = self.draw_string6
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_M:
            self.draw_string = self.draw_string7
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_N:
            self.draw_string = self.draw_string8
            self.setWindowTitle(f"Awesome ASCII Art {self.draw_string}")
        elif key == Qt.Key_E:
            self.draw_string = self.draw_string9
            self.setWindowTitle("Awesome ASCII Art Eraser")

        # WASD / arrow drawing
        elif key in (Qt.Key_W, Qt.Key_Up):
            self.cursor_y = max(0, self.cursor_y - 1)
            self.draw_at_cursor()
        elif key in (Qt.Key_S, Qt.Key_Down):
            self.cursor_y = min(self.height_chars - 1, self.cursor_y + 1)
            self.draw_at_cursor()
        elif key in (Qt.Key_A, Qt.Key_Left):
            self.cursor_x = max(0, self.cursor_x - 1)
            self.draw_at_cursor()
        elif key in (Qt.Key_D, Qt.Key_Right):
            self.cursor_x = min(self.width_chars - 1, self.cursor_x + 1)
            self.draw_at_cursor()

        # Novel functions
        elif key == Qt.Key_H:
            self.show_help()

        elif key == Qt.Key_P:
            string, ok = QInputDialog.getText(
                self, "Populate Text area",
                "Type the characters to fill area:"
            )
            if ok and string:
                self.populate(string)
                self.update()

        elif key == Qt.Key_B:
            self.BG_Flag = not self.BG_Flag
            self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
        
        elif key == Qt.Key_C:
            self.Show_Cursor = not self.Show_Cursor
        
        elif key == Qt.Key_G:
            self.setWindowTitle(f"Tile 1")
            self.draw_tile("Tile1")
        elif key == Qt.Key_V:
            self.setWindowTitle(f"Tile 1")
            self.draw_tile("Tile2")
        
          
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) < 2:
        window = AsciiArtWindow(80, 80)
        print("Optional")
        print(f"Usage: {sys.argv[0]} [width height]")
    elif len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [width height]")
        sys.exit(1)
    else:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        if x < 1:
            x = 1
        if y < 1:
            y = 10
        window = AsciiArtWindow(x, y)

    sys.exit(app.exec_())

'''
ok gotta think about what a whole as control panel might include, 
and how it might work. Im tempted to just build it into the brush-editor
*print 
change font
change font size
other tools?
import brush
import stamps
enable the cursor. 
zoom +/-
import images as a background.


'''
