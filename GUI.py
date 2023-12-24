import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class GameGUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Game GUI")

        self.root.attributes('-fullscreen', True)

        self.size_var = tk.DoubleVar(value=10)
        self.pawn_var = tk.DoubleVar(value=5)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        main_frame = ttk.Frame(self.root, padding=(50, 20))
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        label_font_size = int(24 * screen_width / 1920)

        ttk.Label(main_frame, text="Choose the size of the game board:", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=0, column=0, pady=(0, 10), padx=(140, 0))

        # Changer la couleur du slider en blanc
        ttk.Style().configure("TScale", troughcolor="white")

        size_slider = ttk.Scale(main_frame, from_=8, to=12, variable=self.size_var, orient=tk.HORIZONTAL, length=screen_width // 2, command=self.updateSizeSliderLabel, style="TScale")
        size_slider.grid(row=1, column=0, columnspan=2, pady=(20, 0))

        positions_size = [
            screen_width // 6 - 250,
            screen_width // 6 - 62,
            screen_width // 6 + 127,
            screen_width // 6 + 315,
            screen_width // 6 + 504
        ]
        size_canvases = []
        for i, size in enumerate([8, 9, 10, 11, 12]):
            if i < len(positions_size):
                canvas_size = tk.Canvas(main_frame, width=1, height=10, bg="black")
                x_position_size = positions_size[i]
                canvas_size.place(x=x_position_size, y=85, anchor='center')
                size_canvases.append(canvas_size)

        self.size_label = ttk.Label(main_frame, text=f"Size: {int(self.size_var.get())}x{int(self.size_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.size_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        ttk.Label(main_frame, text="Choose pawn:", anchor='center', font=("TkDefaultFont", label_font_size)).grid(row=4, column=0, pady=(10, 10), padx=(140, 0))

        pawn_slider = ttk.Scale(main_frame, from_=4, to=6, variable=self.pawn_var, orient=tk.HORIZONTAL, length=screen_width // 4, command=self.updatePawnSliderLabel, style="TScale")
        pawn_slider.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        positions_pawn = [
            screen_width // 6 - 58,
            screen_width // 6 + 127,
            screen_width // 6 + 312
        ]
        pawn_canvases = []
        for i, pawn in enumerate([4, 5, 6]):
            if i < len(positions_pawn):
                canvas_pawn = tk.Canvas(main_frame, width=1, height=10, bg="black")
                x_position_pawn = positions_pawn[i]
                canvas_pawn.place(x=x_position_pawn, y=200, anchor='center')
                pawn_canvases.append(canvas_pawn)

        self.pawn_label = ttk.Label(main_frame, text=f"Chosen Pawn: {int(self.pawn_var.get())}", anchor='center', font=("TkDefaultFont", label_font_size))
        self.pawn_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))

        quit_button = ttk.Button(main_frame, text="Quit", command=self.root.destroy)
        quit_button.grid(row=7, column=0, columnspan=2, pady=(10, 10))

    def updateSizeSliderLabel(self, event=None):
        selected_size = round(self.size_var.get())
        self.size_var.set(selected_size)
        self.size_label["text"] = f"Size: {selected_size}x{selected_size}"

    def updatePawnSliderLabel(self, event=None):
        selected_pawn = round(self.pawn_var.get())
        self.pawn_var.set(selected_pawn)
        self.pawn_label["text"] = f"Chosen Pawn: {selected_pawn}"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GameGUI()
    app.run()
