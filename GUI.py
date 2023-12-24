# GUI.py

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from pygame import mixer
import os
from gameGUI import GameGUI

class LobbyGUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Game GUI")
        self.fullscreen_var = tk.BooleanVar(value=True)
        self.root.attributes('-fullscreen', self.fullscreen_var.get())
        mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_file_path = os.path.join(script_dir, "assets", "sounds", "AmbientGuitarLobby.mp3")
        mixer.music.load(music_file_path)
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        self.size_var = tk.DoubleVar(value=10)
        self.pawn_var = tk.DoubleVar(value=5)
        self.volume_var = tk.DoubleVar(value=50)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        main_frame = ttk.Frame(self.root, padding=(50, 20))
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        label_font_size = int(24 * screen_width / 1920)
        ttk.Label(main_frame, text="Choose the size of the game board:", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=0, column=0, pady=(0, 10), padx=(140, 0))
        ttk.Style().configure("TScale", troughcolor="white")
        size_slider = ttk.Scale(main_frame, from_=8, to=12, variable=self.size_var, orient=tk.HORIZONTAL, length=screen_width // 2, command=self.updateSizeSliderLabel, style="TScale")
        size_slider.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        positions_size = [0.5, 12.75, 25, 37.2, 49.5]
        size_canvases = []
        for i, size in enumerate([8, 9, 10, 11, 12]):
            if i < len(positions_size):
                x_position_size = (positions_size[i] / 100) * screen_width
                canvas_size = tk.Canvas(main_frame, width=1, height=10, bg="black")
                canvas_size.place(x=x_position_size, y=85, anchor='center')
                size_canvases.append(canvas_size)
        self.size_label = ttk.Label(main_frame, text=f"Size: {int(self.size_var.get())}x{int(self.size_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.size_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        ttk.Label(main_frame, text="Choose pawn:", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=4, column=0, pady=(10, 10), padx=(140, 0))
        pawn_slider = ttk.Scale(main_frame, from_=4, to=6, variable=self.pawn_var, orient=tk.HORIZONTAL, length=screen_width // 4, command=self.updatePawnSliderLabel, style="TScale")
        pawn_slider.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        positions_pawn = [13, 25, 37]
        pawn_canvases = []
        for i, pawn in enumerate([4, 5, 6]):
            if i < len(positions_pawn):
                x_position_pawn = (positions_pawn[i] / 100) * screen_width
                canvas_pawn = tk.Canvas(main_frame, width=1, height=10, bg="black")
                canvas_pawn.place(x=x_position_pawn, y=200, anchor='center')
                pawn_canvases.append(canvas_pawn)
        self.pawn_label = ttk.Label(main_frame, text=f"Chosen Pawn: {int(self.pawn_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.pawn_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        quit_button_text = "Go windowed"
        self.quit_button = ttk.Button(main_frame, text=quit_button_text, command=self.toggleFullscreen)
        self.quit_button.grid(row=7, column=0, columnspan=2, pady=(10, 10))
        volume_slider = ttk.Scale(main_frame, from_=0, to=100, variable=self.volume_var, orient=tk.HORIZONTAL, length=screen_width // 4, command=self.updateVolume, style="TScale")
        volume_slider.grid(row=8, column=0, columnspan=2, pady=(20, 0), padx=(0, 20), sticky='se')
        new_window_button = ttk.Button(main_frame, text="New Window", command=self.openNewWindow)
        new_window_button.grid(row=9, column=0, columnspan=2, pady=(20, 0))

    def updateSizeSliderLabel(self, event=None):
        selected_size = round(self.size_var.get())
        self.size_var.set(selected_size)
        self.size_label["text"] = f"Size: {selected_size}x{selected_size}"

    def updatePawnSliderLabel(self, event=None):
        selected_pawn = round(self.pawn_var.get())
        self.pawn_var.set(selected_pawn)
        self.pawn_label["text"] = f"Chosen Pawn: {selected_pawn}"

    def updateVolume(self, event=None):
        volume_level = self.volume_var.get() / 100
        mixer.music.set_volume(volume_level)

    def toggleFullscreen(self):
        self.fullscreen_var.set(not self.fullscreen_var.get())
        self.root.attributes('-fullscreen', self.fullscreen_var.get())
        quit_button_text = "Go windowed" if self.fullscreen_var.get() else "Go fullscreen"
        self.quit_button["text"] = quit_button_text

    def openNewWindow(self):
        self.root.destroy()
        mixer.music.stop()
        new_window = GameGUI(size=int(self.size_var.get()))
        new_window.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LobbyGUI()
    app.run()
