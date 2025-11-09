#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import Canvas, font
from datetime import datetime

"""
ASCII-only version of the ASCII Art Generator.
Now draws characters from a defined string instead of random ones.

Got rid of prepopulated text area.. well sorta, its populated with spaces.

"""

# Change this string to whatever you want to "paint" with
draw_string = "FOSS IS BOSS"


class AsciiArtApp:
    def __init__(self, width=80, height=80):
        self.width = width
        self.height = height
        self.char_grid = [[' '] * width for _ in range(height)]
        self.canvas = None
        self.text_color = "black"

        # Brush source string
        self.draw_string = draw_string
        self.draw_index = 0

        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("ASCII Art Generator (ASCII Only)")
        self.root.attributes("-alpha", 1.3)

        self.canvas = Canvas(
            self.root,
            width=8 * self.width,
            height=14 * self.height,
            bg="white"
        )
        self.canvas.pack()


        self.font = font.Font(family="Courier", size=10)
        self.render_text()

        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.root.bind("<KeyPress-r>", self.reset_screen)
        self.root.bind("<KeyPress-s>", self.save_ascii_art)

        color_keys = {
            "1": "black", "2": "red", "3": "blue", "4": "green",
            "5": "purple", "6": "orange", "7": "yellow",
            "8": "cyan", "9": "magenta", "0": "white"
        }
        for key, color in color_keys.items():
            self.root.bind(f"<KeyPress-{key}>", lambda e, c=color: self.change_color(c))

        self.root.mainloop()

    def render_text(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                char = self.char_grid[y][x]
                color = self.text_color if char != '#' else "gray"
                self.canvas.create_text(
                    x * 8, y * 14, text=char, anchor="nw", fill=color, font=self.font
                )

    def on_drag(self, event):
        x, y = event.x // 8, event.y // 14
        if 0 <= x < self.width and 0 <= y < self.height:
            # Use the next character from draw_string
            char = self.draw_string[self.draw_index % len(self.draw_string)]
            self.char_grid[y][x] = char
            self.draw_index += 1
            self.render_text()

    def reset_screen(self, event=None):
        self.char_grid = [[' '] * self.width for _ in range(self.height)]
        self.draw_index = 0
        self.render_text()

    def change_color(self, color):
        self.text_color = color
        self.render_text()

    def save_ascii_art(self, event=None):
        filename = f"ascii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="ascii") as f:
            for row in self.char_grid:
                f.write("".join(row) + "\n")
        print(f"ASCII art saved to {filename}")


if __name__ == "__main__":
    width, height = 80, 80
    if len(sys.argv) > 1:
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
        except ValueError:
            print("Usage: python ascii_art_app.py [width height]")
            print("Invalid dimensions, using default 80x80")

    AsciiArtApp(width, height)
