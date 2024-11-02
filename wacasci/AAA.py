#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import Canvas, font
from datetime import datetime
from PIL import Image, ImageDraw
import random
"""
Gist:
Its like pixel art, but with ascii.
"""


"""
ToDo:

I looked at this ascii table, but this is not what renders.
https://www.asciitable.com/

So, Ill have to write a test to figure out what characters render
as intended... or something. 

Saved file is not read able! 
it is, but you need an app that can render extended ascii characters. 
or i need to modify this to not use extended ascii characters... IDK, 
Tests will tell me that. 

Render size differs.... shouldnt 80x80 be square? lol no. characters, 
are rectangles, and so is 80x80. you want squares, use 2xwidth, or 1/2 height 
or something like that. 

Opening very large frames both takes a long time to render, and may hang the program
"""

class AsciiArtApp:
    def __init__(self, width=80, height=80):
        self.width = width
        self.height = height
        self.char_grid = [[chr(219)] * width for _ in range(height)]
        self.canvas = None
        self.pressure = 0  # Placeholder for pressure detection
        self.text_color = "black"  # Default color
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("ASCII Art Generator")
        
        # Canvas to display the text box with fixed-width font
        self.canvas = Canvas(self.root, width=8 * self.width, height=14 * self.height, bg="white")
        self.canvas.pack()
        
        # Set up a fixed-width font for consistent alignment
        self.font = font.Font(family="Courier", size=10)
        
        self.render_text()

        # Bind tablet events here (use pen/mouse events for now)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Key bindings
        self.root.bind("<KeyPress-r>", self.reset_screen)  # Press 'r' to reset
        self.root.bind("<KeyPress-s>", self.save_ascii_art)  # Press 's' to save
        self.root.bind("<KeyPress-1>", lambda e: self.change_color("black"))
        self.root.bind("<KeyPress-2>", lambda e: self.change_color("red"))
        self.root.bind("<KeyPress-3>", lambda e: self.change_color("blue"))
        self.root.bind("<KeyPress-4>", lambda e: self.change_color("green"))
        self.root.bind("<KeyPress-5>", lambda e: self.change_color("purple"))
        self.root.bind("<KeyPress-6>", lambda e: self.change_color("orange"))
        self.root.bind("<KeyPress-7>", lambda e: self.change_color("yellow"))
        self.root.bind("<KeyPress-8>", lambda e: self.change_color("cyan"))
        self.root.bind("<KeyPress-9>", lambda e: self.change_color("magenta"))
        self.root.bind("<KeyPress-0>", lambda e: self.change_color("white"))
        
        
        self.root.mainloop()

    def render_text(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                color = self.text_color if self.char_grid[y][x] != chr(219) else "red"
                self.canvas.create_text(x * 8, y * 14, text=self.char_grid[y][x], anchor="nw", fill=color, font=self.font)

    def on_drag(self, event):
        x, y = event.x // 8, event.y // 14

        # Simulate pressure-based character changes
        self.pressure = random.choice([0, 1, 2, 3])  # Placeholder for real pressure values
        char_map = {0: chr(0), 1: chr(178), 2: chr(177), 3: chr(176)}
        if 0 <= x < self.width and 0 <= y < self.height:
            self.char_grid[y][x] = char_map[self.pressure]
            self.render_text()

    def reset_screen(self, event=None):
        # Reset the screen by filling it with the initial character
        self.char_grid = [[chr(219)] * self.width for _ in range(self.height)]
        self.render_text()

    def change_color(self, color):
        # Change the drawing color
        self.text_color = color
        self.render_text()

    def save_ascii_art(self, event=None):
        filename = f"ascii_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
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

    app = AsciiArtApp(width, height)
