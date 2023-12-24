# gameGUI.py

import tkinter as tk
from tkinter import ttk

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game GUI")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        main_frame = ttk.Frame(self.root, padding=(50, 20))
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_font_size = int(24 * screen_width / 1920)

        ttk.Label(main_frame, text="Hello", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=0, column=0, pady=(0, 10))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GameGUI()
    app.run()
