import tkinter as tk
from PIL import Image, ImageTk


class Winner1Wins:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.image = Image.open("./assets/images/winner-1.png")


class Winner2Wins:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.image = Image.open("./assets/images/winner-2.png")

