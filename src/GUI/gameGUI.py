import tkinter as tk
from pygame import mixer

class GameGUI:
    def __init__(self, root, taillePlateau, fullscreen=False):
        self.root = root
        self.root.title("Jeu de Grille")
        
        mixer.init()
        mixer.music.load('./assets/sounds/AmbientPianoGame.mp3')
        mixer.music.set_volume(0)
        mixer.music.play(-1)
        
        self.taillePlateau = taillePlateau
        self.coteCase = 0
        self.joueurActuel = 1

        self.calculerTailleCase()

        self.canevas = tk.Canvas(self.root, bg="black", width=2 * self.coteCase * self.taillePlateau, height=2 * self.coteCase * self.taillePlateau)
        self.canevas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.labelJoueur = tk.Label(self.root, text="Tour du Joueur 1", font=("Helvetica", 16), fg="white", bg="black")
        self.labelJoueur.pack(side=tk.BOTTOM, pady=(10, 10))

        self.etatCases = [[False] * taillePlateau for _ in range(taillePlateau)] # etat false

        self.dessinerQuadrillage()

        self.canevas.bind("<Button-1>", self.selectionnerCase)
        
        if fullscreen:
            self.root.attributes('-fullscreen', True)

    def calculerTailleCase(self):
        self.coteCase = min(self.root.winfo_screenwidth(), self.root.winfo_screenheight() - 100) / (2 * self.taillePlateau)

    def dessinerQuadrillage(self):
        self.startX = (self.root.winfo_screenwidth() - 2 * self.coteCase * self.taillePlateau) / 2
        self.startY = (self.root.winfo_screenheight() - 2 * self.coteCase * self.taillePlateau) / 4

        for i in range(self.taillePlateau + 1):
            x = self.startX + i * 2 * self.coteCase
            self.canevas.create_line(x, self.startY, x, 2 * self.coteCase * self.taillePlateau + self.startY, fill="white")

        for i in range(self.taillePlateau + 1):
            y = self.startY + i * 2 * self.coteCase
            self.canevas.create_line(self.startX, y, 2 * self.coteCase * self.taillePlateau + self.startX, y, fill="white")

    def selectionnerCase(self, event):
        x = event.x
        y = event.y

        if self.startX <= x < self.startX + 2 * self.coteCase * self.taillePlateau and \
                self.startY <= y < self.startY + 2 * self.coteCase * self.taillePlateau:
            col = int((x - self.startX) / (2 * self.coteCase))
            row = int((y - self.startY) / (2 * self.coteCase))

            if 0 <= col < self.taillePlateau and 0 <= row < self.taillePlateau:
                if not self.etatCases[row][col]:
                    tailleBoule = 0.7
                    couleur = "blue" if self.joueurActuel == 1 else "red"
                    self.canevas.create_oval(self.startX + col * 2 * self.coteCase + (1 - tailleBoule) * self.coteCase,
                                             self.startY + row * 2 * self.coteCase + (1 - tailleBoule) * self.coteCase,
                                             self.startX + (col + 1) * 2 * self.coteCase - (1 - tailleBoule) * self.coteCase,
                                             self.startY + (row + 1) * 2 * self.coteCase - (1 - tailleBoule) * self.coteCase,
                                             fill=couleur, outline="white")

                    self.etatCases[row][col] = True
                    self.canevas.itemconfig(self.canevas.find_closest(x, y), state=tk.DISABLED)
                    self.joueurActuel = 3 - self.joueurActuel
                    self.labelJoueur.config(text=f"Tour du Joueur {self.joueurActuel}")

    def initializeAudio(self):
        mixer.music.load('./assets/sounds/AmbientGuitarLobby.mp3')
        mixer.music.set_volume(0)
        mixer.music.play(-1)
