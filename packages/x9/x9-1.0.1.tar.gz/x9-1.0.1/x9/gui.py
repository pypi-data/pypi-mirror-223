import tkinter as tk
from tkinter import PhotoImage

class ResizableEntry(tk.Entry):
    def resize(self, width):
        self.config(width=width)

class GUIPlus:
    def __init__(self):
        self.window = tk.Tk()
        self.elements = []

    def bg(self, color):
        self.window.configure(bg=color)

    def title(self, title):
        self.window.title(title)

    def favicon(self, path):
        favicon = PhotoImage(file=path)
        self.window.iconphoto(True, favicon)

    def resize(self, dimensions):
        self.window.geometry(dimensions)

    def textbox(self, placeholder='', width=20, height=1):  # height added for Text widget
        textbox = ResizableEntry(self.window)
        textbox.insert(0, placeholder)
        textbox.config(width=width)
        textbox.pack(pady=5)
        self.elements.append(textbox)
        return textbox

    def button(self, value='Button', command=None):
        button = tk.Button(self.window, text=value, command=command)
        button.pack(pady=5)
        return button

    def run(self):
        self.window.mainloop()

def new():
    return GUIPlus()

def label(text):
    label = tk.Label(text=text)
    return label

def font(label, font_name, font_size, is_bold=False):
    font_style = "bold" if is_bold else "normal"
    label.config(font=(font_name, font_size, font_style))
