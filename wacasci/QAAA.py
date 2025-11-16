#!/usr/bin/env python3
import sys
import os
os.environ["QT_LOGGING_RULES"] = "*.warning=false" # STFU Qt warnings

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QInputDialog
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from datetime import datetime

# the repeat characters effectively lowers sensitivity, making it easer to draw
draw_string = "...oooOOO000OOOooo..." # T
draw_string1 = "...,,,---'''"         # Y
draw_string2 = "[[[]]]|||///\\\\"     # U
draw_string3 = "HACKTHEMATRIX"        # I
draw_string4 = "    "                 # Erase lol
# other features to add:
# press T for text typing. escape to drawing by pressing any pallet key including E.
# how that migth work: get last known cordinate, start typing there.

# wasd and arrow keys added. tried to get mouse cursor to give current poisition, 
# but thats not working yet. 

# Added file open, but text will not reize window so easily



class AsciiArtWindow(QWidget):
    def __init__(self, width=80, height=80):
        super().__init__()
        # Ctrl+S function
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save_file)
        # Ctrl+O function
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.open_file)
        
        
        self.width_chars = width
        self.height_chars = height
        self.char_grid = [[' '] * width for _ in range(height)]
        self.text_color = QColor("black")
        self.draw_string = draw_string
        self.draw_index = 0
        self.char_width = 8
        self.char_height = 14
        self.current_filename = None
        self.scroll_parent = None
        
        # Stored positionals
        self.cursor_x = 0
        self.cursor_y = 0
        
        
                 
        # Window setup
        self.setWindowTitle("Qt Awesome ASCII Arts!")
        self.resize(self.width_chars * self.char_width, self.height_chars * self.char_height)

        # Transparent background while keeping the frame
        self.BG_Flag = True       # background flag
        self.setAttribute(Qt.WA_TranslucentBackground, self.BG_Flag)
        self.setAutoFillBackground(False)

        # Monospace font
        self.font = QFont("Courier", 10)
        self.show()
        
        # Set minimum window size: manual resizing. 
        self.setMinimumSize(self.char_width * 10, self.char_height * 1)


    def draw_at_cursor(self):
        if 0 <= self.cursor_x < self.width_chars and 0 <= self.cursor_y < self.height_chars:
            char = self.draw_string[self.draw_index % len(self.draw_string)]
            self.char_grid[self.cursor_y][self.cursor_x] = char
            self.draw_index += 1
            self.update()        

    def mouseMoveEvent(self, event):
        self.cursor_x = event.x() // self.char_width
        self.cursor_y = event.y() // self.char_height
        self.update()

    def show_help(self):
        # If already open, bring it to front
        if hasattr(self, "help_window") and self.help_window.isVisible():
            self.help_window.raise_()
            self.help_window.activateWindow()
            return

        self.help_window = QDialog(self)
        self.help_window.setWindowTitle("Key Bindings")
        self.help_window.setWindowFlags(Qt.Window)   # <-- Makes it a real independent window

        layout = QVBoxLayout()
        label = QLabel()
        label.setText(      
            "ASCII Art Generator — Key Bindings\n\n"
            "Drawing:\n"
            "  T  - Brush 1 (oooOOO...)\n"
            "  Y  - Brush 2 (,,,---''')\n"
            "  U  - Brush 3 ([[[]]]|||///\\\\)\n"
            "  I  - Brush 4 (HACKTHEMATRIX)\n"
            "  E  - Eraser\n"
            "\n"
            "Controls:\n"
            "  Mouse Drag   - Draw characters\n"
            "  R            - Reset canvas\n"
            "  P            - Populate entire area with text\n"
            "  B            - Toggle background\n"
            "  Ctrl+S       - Save\n"
            #"  Ctrl+O       - Open\n"
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
        # you can init larger area, when trying to init scroll bars if over 500 char stuff broke. its unrealted, you can init larger, just not by opening a file. fix later
        # you can resize manualy for now.
        max_w = 500
        max_h = 500
        
        if not path:
            return

        # Read the file
        with open(path, "r", encoding="ascii", errors="ignore") as f:
            lines = f.read().splitlines()

        if not lines:
            return

        # Determine size
        max_width = max(len(line) for line in lines)
        height = len(lines)

        # Hard caps
        capped_width = min(max_width, max_w)
        capped_height = min(height, max_h)

        # Build new character grid (truncate if needed)
        self.width_chars = capped_width
        self.height_chars = capped_height

        self.char_grid = [[' ' for _ in range(self.width_chars)]
                           for _ in range(self.height_chars)]

        for y in range(self.height_chars):
            line = lines[y]
            for x in range(min(len(line), self.width_chars)):
                self.char_grid[y][x] = line[x]

        # Resize window or apply scrolling ... breaks app so bad. 
        #self.apply_resize(max_width, height)

        self.update()
        print(f"Loaded file: {path}")
   
        
        
    def save_file(self):
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

        print(f"ASCII art saved to: {filename}")

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

    def resizeEvent(self, event):
        self.update_grid()
        self.update()

    def update_grid(self):
        new_w = max(1, self.width() // self.char_width)
        new_h = max(1, self.height() // self.char_height)

        # Only rebuild if the size changed
        if new_w != self.width_chars or new_h != self.height_chars:
            self.width_chars = new_w
            self.height_chars = new_h

            # Resize char grid while retaining old content if possible
            new_grid = [[' '] * new_w for _ in range(new_h)]
            for y in range(min(new_h, len(self.char_grid))):
                for x in range(min(new_w, len(self.char_grid[0]))):
                    new_grid[y][x] = self.char_grid[y][x]

            self.char_grid = new_grid

    
    def populate(self, s):
        # Fill the entire area with repeating text
        if not s:
            return
        length = len(s)
        index = 0
        for y in range(self.height_chars):
            for x in range(self.width_chars):
                self.char_grid[y][x] = s[index % length]
                index += 1



    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_R:
            self.char_grid = [[' '] * self.width_chars for _ in range(self.height_chars)]
            self.draw_index = 0
            self.update()
        # Onscreen colors
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
        
        # Drawing characters     
        elif key == Qt.Key_T:
            self.draw_string = draw_string
            self.setWindowTitle(f"draw_string")
            self.setWindowTitle(f"Awesome ASCII Art {draw_string}")
        elif key == Qt.Key_Y:
            self.draw_string = draw_string1
            self.setWindowTitle(f"Awesome ASCII Art {draw_string1}")
        elif key == Qt.Key_U:
            self.draw_string = draw_string2
            self.setWindowTitle(f"Awesome ASCII Art {draw_string2}")
        elif key == Qt.Key_I:
            self.draw_string = draw_string3
            self.setWindowTitle(f"Awesome ASCII Art {draw_string3}")
        elif key == Qt.Key_E:
            self.draw_string = draw_string4
            self.setWindowTitle("Awesome ASCII Art ERRASING")
                  
        # Drawing Keys
        elif key == Qt.Key_W or key == Qt.Key_Up:
            self.cursor_y = max(0, self.cursor_y - 1)
            self.draw_at_cursor()     
        elif key == Qt.Key_S or key == Qt.Key_Down:
            self.cursor_y = min(self.height_chars - 1, self.cursor_y + 1)
            self.draw_at_cursor()                           
        elif key == Qt.Key_A or key == Qt.Key_Left:
            self.cursor_x = max(0, self.cursor_x - 1)
            self.draw_at_cursor()                
        elif key == Qt.Key_D or key == Qt.Key_Right:
            self.cursor_x = min(self.width_chars - 1, self.cursor_x + 1)
            self.draw_at_cursor()
        
        # Novel functions
        elif key == Qt.Key_H:
            self.show_help()
            
        elif key == Qt.Key_P:
            # Populate the screen with text. window,lable
            # let populate get the current window size and populate it. 
            string, ok = QInputDialog.getText(self, "Populate Text area", "type the Characters to fill area: ")
            if ok and string:
                self.populate(string)
                self.update()
            
        elif key == Qt.Key_B:
            # set or unset background
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
        if x < 1:
            x = 1
        if y < 1:
            y = 10 
        window = AsciiArtWindow(x, y)   
        
    sys.exit(app.exec_())
