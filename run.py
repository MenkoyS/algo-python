from src.lobbyGUI import LobbyGUI
from src.gameGUI import GameGUI
from src.game import Game

import tkinter as tk
import os

from PIL import Image, ImageTk
from pygame import mixer
import platform


class WelcomeApp:
    def __init__(self):
        """
        ~~~> Initializes the WelcomeApp class.

        ~~> Args:
            ~> root (tk.Tk): The main Tkinter window.
        """
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # ~~> sound effect __init__
        mixer.init()

        self.image = Image.open("./assets/images/moglogo.png")

        # ~~> getScreenDims
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # ~> img sizing
        self.new_width = int(self.screen_width * 0.5)
        self.new_height = int(self.screen_height * 0.5)
        self.image = self.image.resize((self.new_width, self.new_height), Image.ANTIALIAS if 'ANTIALIAS' in dir(Image) else Image.BICUBIC)

        # ~> tkinter photoimageformat
        self.tk_image = ImageTk.PhotoImage(self.image)

        # ~> centering
        self.x = (self.screen_width - self.new_width) // 2
        self.y = (self.screen_height - self.new_height) // 2

        # ~~> widget to display the image
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg='black')
        self.canvas.pack()

        # ~~> next label
        self.next_label = tk.Label(self.root, text="↳ Suivant", font=("Helvetica", 48), fg='white', bg='black')
        self.next_label.bind("<Button-1>", lambda event=None: self.showNextWindow())  # ~> bind left click
        self.next_label.place_forget()  # ~> hide initially 

        # ~~> display fadeIN effect
        self.canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.tk_image)

        self.fadeIn()

    def fadeIn(self):
        """
        ~~> FadeIN effect (opacity increasing)
        """
        alpha = 0
        while alpha < 1.0:
            alpha += 0.01
            tk_image = self.applyTransparency(self.tk_image, alpha)
            self.canvas.itemconfig(self.canvas.find_all()[0], image=tk_image)
            self.root.update()
            self.root.after(3)

        self.fadeOut()

    def fadeOut(self):
        """
        ~~> FadeOUT effect (opacity decreasing)
        """
        alpha = 1.0
        while alpha > 0.0:
            alpha -= 0.01
            tk_image = self.applyTransparency(self.tk_image, alpha)
            self.canvas.itemconfig(self.canvas.find_all()[0], image=tk_image)
            self.root.update()
            self.root.after(3)

        # ~~> delete img | sound effect
        self.canvas.delete("all")
        mixer.music.set_volume(0.1)
        mixer.music.load("./assets/sounds/writing.mp3")
        mixer.music.play(0, 0.0)

        self.showWelcomeTextDynamic("Bienvenue sur L-Knight Battle, amusez-vous bien.")

    def applyTransparency(self, tk_image, alpha):
        """
        ~~~> Apply transparency to the image.

        ~~> Args:
            ~> tk_image (ImageTk.PhotoImage): Tkinter PhotoImage.
            ~> alpha (float): Transparency value.
        """
        image = ImageTk.getimage(tk_image).convert("RGBA")
        image.putalpha(int(alpha * 255))
        return ImageTk.PhotoImage(image)

    def showWelcomeTextDynamic(self, text):
        """
        ~~~> Dynamic writing

        ~~> Args:
            ~> text (str): Text to be displayed
        """
        index = 0
        while index < len(text):
            self.canvas.delete("text")  # ~~> delete existing text
            self.canvas.create_text(self.canvas.winfo_reqwidth() // 2, self.canvas.winfo_reqheight() // 2,
                                    text=text[:index + 1], font=("Helvetica", 24), fill="white", anchor=tk.CENTER, tags="text")
            self.root.update()
            self.root.after(100)
            index += 1

        mixer.music.stop()
        self.blinkNextLabel()

    def blinkNextLabel(self):
        """
        Make "Next" label blink using :after
        """
        self.next_label.place(relx=1.0, rely=1.0, anchor=tk.SE)
        self.root.after(500, self.toggleNextLabel)

    def toggleNextLabel(self):
        """
        Toggle visibility of "Next" label and schedule the next toggle
        """
        current_state = self.next_label.winfo_ismapped()
        self.next_label.place_forget() if current_state else self.next_label.place(relx=1.0, rely=1.0, anchor=tk.SE)
        self.root.after(500, self.toggleNextLabel)

    def showNextWindow(self):
        if self.isSaved():
            if tk.messagebox.askquestion(title="Load Save", message="Would you like to load your previously saved game ?") == "yes":
                game = Game()
                game.loadGame()
                self.root.destroy()
                GameGUI(game).run()
            else:
                self.root.destroy()
                LobbyGUI().run()
        else:
            self.root.destroy()
            LobbyGUI().run()

    def isSaved(self, filename="save.txt"):
        """
        ~~~> Check if the game has been saved.
        ~~> Args:
            ~> filename (str): The name of the file to check.
        ~~> Returns:
            ~> bool: True if the game has been saved, False otherwise.
        """
        return os.path.isfile(f"./src/game_save/{filename}")

    def run(self):
        """
        ~~~> Run the WelcomeApp.
        """       
        self.root.mainloop()

if __name__ == "__main__":
    WelcomeApp().run()
