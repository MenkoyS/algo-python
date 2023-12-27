import tkinter as tk
from tkinter import ttk
from pygame import mixer
from ttkthemes import ThemedTk
from gameGUI import GameGUI

class LobbyGUI:
    def __init__(self):
        self.initialize_window()
        self.initialize_audio()
        self.initialize_variables()

        # Create the main frame we will place elements in
        main_frame = ttk.Frame(self.root, padding=500)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # self.create_welcome_label(main_frame)
        self.create_size_controls(main_frame)
        self.create_pawn_controls(main_frame)
        self.create_quit_button(main_frame)
        self.create_volume_control(main_frame)
        self.create_start_game_button(main_frame)

    def initialize_window(self):
        self.root = ThemedTk(theme="black")
        self.root.title("Game Lobby")
        self.root.geometry("843x480")
        self.root.resizable(False, False)
        self.root.attributes('-fullscreen', True)

    def initialize_audio(self):
        mixer.init()
        mixer.music.load('./assets/sounds/AmbientGuitarLobby.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    def initialize_variables(self):
        self.size_var = tk.DoubleVar(value=10)
        self.pawn_var = tk.DoubleVar(value=5)
        self.volume_var = tk.DoubleVar(value=50)
        self.size_canvases = []
        self.pawn_canvases = []

    def create_welcome_label(self, frame):
        welcome_label = tk.Label(frame, text="Welcome to the Game Lobby", font=("Helvetica", 16))
        welcome_label.grid(row=0, column=0, pady=(0, 100), padx=(100, 0))

    def create_size_controls(self, frame):
        label_font_size = int(24 * self.root.winfo_width() / 1920)
        ttk.Label(frame, text="Choose the size of the game board", anchor='center', font=("TkDefaultFont", label_font_size)).grid(columnspan=3, pady=(0, 10))

        size_slider = ttk.Scale(frame, from_=8, to=12, variable=self.size_var, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 2, command=self.update_size_slider_label, style="TScale")
        size_slider.grid(row=1, columnspan=2, pady=(20, 10))

        self.create_position_canvases(frame, [8, 9, 10, 11, 12], [0.5, 12.75, 25, 37.2, 49.5], 85, 'center', self.size_canvases)
        self.size_label = ttk.Label(frame, text=f"Size: {int(self.size_var.get())}x{int(self.size_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.size_label.grid(row=3, column=0, columnspan=2, pady=(40, 40))

    def create_pawn_controls(self, frame):
        label_font_size = int(24 * self.root.winfo_width() / 1920)
        ttk.Label(frame, text="Choose pawn", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=4, column=0, columnspan=3, pady=(10, 10))
        pawn_slider = ttk.Scale(frame, from_=4, to=6, variable=self.pawn_var, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 4, command=self.update_pawn_slider_label, style="TScale")
        pawn_slider.grid(row=5, column=0, columnspan=2, pady=(20, 10))

        self.create_position_canvases(frame, [4, 5, 6], [13, 25, 37], 290, 'center', self.pawn_canvases)
        self.pawn_label = ttk.Label(frame, text=f"Chosen Pawn: {int(self.pawn_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.pawn_label.grid(row=6, column=0, columnspan=2, pady=(40, 40))

    def create_quit_button(self, frame):
        quit_button_text = "Go windowed"
        self.quit_button = ttk.Button(frame, text=quit_button_text, command=self.toggle_fullscreen)
        self.quit_button.grid(row=7, column=0, columnspan=2, pady=(10, 10))
        
    def create_start_game_button(self, frame):
        new_window_button = ttk.Button(frame, text="Start Game", command=self.open_new_window)
        new_window_button.grid(row=8, column=0, columnspan=2, pady=(20, 0))

    def create_volume_control(self, frame):
        volume_slider = ttk.Scale(frame, from_=0, to=100, variable=self.volume_var, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 4, command=self.update_volume, style="TScale")
        volume_slider.grid(row=9, column=0, columnspan=2, pady=(20, 0), padx=(0, 20), sticky='se')

    def create_position_canvases(self, frame, values, positions, y_position, anchor, canvases):
        screen_width = self.root.winfo_screenwidth()
        for i, value in enumerate(values):
            if i < len(positions):
                x_position = (positions[i] / 100) * screen_width
                canvas = tk.Canvas(frame, width=1, height=15, bg="black", highlightthickness=0)
                canvas.place(x=x_position, y=y_position, anchor=anchor)
                canvases.append(canvas)

    def update_size_slider_label(self, event=None):
        selected_size = round(self.size_var.get())
        self.size_var.set(selected_size)
        self.size_label["text"] = f"Size: {selected_size}x{selected_size}"

    def update_pawn_slider_label(self, event=None):
        selected_pawn = round(self.pawn_var.get())
        self.pawn_var.set(selected_pawn)
        self.pawn_label["text"] = f"Chosen Pawn: {selected_pawn}"

    def update_volume(self, event=None):
        volume_level = self.volume_var.get() / 100
        mixer.music.set_volume(volume_level)

    def toggle_fullscreen(self):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.quit_button["text"] = "Go fullscreen"
        else:
            self.root.attributes('-fullscreen', True)
            self.quit_button["text"] = "Go windowed"

    def open_new_window(self):
        self.root.destroy()
        mixer.music.stop()
        new_window = GameGUI(size=int(self.size_var.get()))
        new_window.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LobbyGUI()
    app.run()
