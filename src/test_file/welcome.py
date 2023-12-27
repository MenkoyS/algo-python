import tkinter as tk

class WelcomeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test")
        self.root.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.text = "ceci est un texte ..."
        self.x_position = root.winfo_screenwidth() // 2
        self.y_position = root.winfo_screenheight() // 2
        self.speed = 100  # ~~~> time

        self.text_already_written = ""
        self.text_to_write = self.text

        self.animateText()

    def animateText(self):
        self.canvas.delete("all")

        if self.text_to_write:
            current_letter = self.text_to_write[:1]
            self.text_already_written += current_letter
            self.text_to_write = self.text_to_write[1:]

        self.canvas.create_text(self.x_position, self.y_position, text=self.text_already_written, anchor=tk.CENTER, fill="white", font=("Helvetica", 24))

        if self.text_to_write:
            self.root.after(self.speed, self.animateText)

if __name__ == "__main__":
    root = tk.Tk()
    welcome_gui = WelcomeGUI(root)
    root.mainloop()
