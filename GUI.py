import tkinter as tk
from tkinter import ttk

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game GUI")

        self.size_var = tk.DoubleVar(value=10)
        self.pawn_var = tk.DoubleVar(value=4)

        main_frame = ttk.Frame(self.root, padding=(50, 20))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Choose the size of the game board:").grid(row=0, column=0, pady=(0, 10))

        size_slider = ttk.Scale(main_frame, from_=8, to=12, variable=self.size_var, orient=tk.HORIZONTAL, length=200, command=self.updateSizeSliderLabel)
        size_slider.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        positions_size = [6, 52, 99, 145, 192] 
        for i, (size, annotation) in enumerate(sizes_and_annotations):
            size_slider.set(size)
            canvas_size = tk.Canvas(main_frame, width=1, height=10, bg="black")
            x_position_size = positions_size[i]
            canvas_size.place(x=x_position_size, y=50, anchor='center')

        self.size_label = ttk.Label(main_frame, text=f"Size: {int(self.size_var.get())}x{int(self.size_var.get())}")
        self.size_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(main_frame, text="Choose pawn:").grid(row=4, column=0, pady=(10, 10))

        pawn_slider = ttk.Scale(main_frame, from_=4, to=6, variable=self.pawn_var, orient=tk.HORIZONTAL, length=100, command=self.updatePawnSliderLabel)
        pawn_slider.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        positions_pawn = [56, 99, 142] 
        for i, pawn in enumerate([4, 5, 6]):
            pawn_slider.set(pawn)
            canvas_pawn = tk.Canvas(main_frame, width=1, height=10, bg="black")
            x_position_pawn = positions_pawn[i]
            canvas_pawn.place(x=x_position_pawn, y=155, anchor='center')

        self.pawn_label = ttk.Label(main_frame, text=f"Chosen Pawn: {int(self.pawn_var.get())}")
        self.pawn_label.grid(row=6, column=0, columnspan=2, pady=(0, 10))

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
    sizes_and_annotations = [(8, "8x8"), (9, "9x9"), (10, "10x10"), (11, "11x11"), (12, "12x12")]
    app = GameGUI()
    app.run()
