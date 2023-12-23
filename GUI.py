import tkinter as tk
from tkinter import ttk

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game GUI")

        self.size_var = tk.DoubleVar(value=10)

        main_frame = ttk.Frame(self.root, padding=(50, 20))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Choose the size of the game board:").grid(row=0, column=0, pady=(0, 10))

        size_slider = ttk.Scale(main_frame, from_=8, to=12, variable=self.size_var, orient=tk.HORIZONTAL, length=200, command=self.updateSliderLabel)
        size_slider.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        positions = [6, 52, 99, 145, 192]
        for i, (size, annotation) in enumerate(sizes_and_annotations):
            size_slider.set(size)
            canvas = tk.Canvas(main_frame, width=1, height=10, bg="black")
            x_position = positions[i]
            canvas.place(x=x_position, y=50, anchor='center')

        self.size_label = ttk.Label(main_frame, text=f"Size: {int(self.size_var.get())}x{int(self.size_var.get())}")
        self.size_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

    def updateSliderLabel(self, event=None):
        selected_size = round(self.size_var.get())
        self.size_var.set(selected_size)
        self.size_label["text"] = f"Size: {selected_size}x{selected_size}"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    sizes_and_annotations = [(8, "8x8"), (9, "9x9"), (10, "10x10"), (11, "11x11"), (12, "12x12")]
    app = GameGUI()
    app.run()
