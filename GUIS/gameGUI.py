import tkinter as tk

class GameGUI:
    def __init__(self, root, taille_plateau):
        self.root = root
        self.root.title("Jeu de Grille")
        
        self.taille_plateau = taille_plateau
        self.cote_case = 0
        self.joueur_actuel = 1

        self.calculer_taille_case()

        self.canevas = tk.Canvas(self.root, bg="black", width=2*self.cote_case*self.taille_plateau, height=2*self.cote_case*self.taille_plateau)
        self.canevas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_joueur = tk.Label(self.root, text="Tour du Joueur 1", font=("Helvetica", 16), fg="white", bg="black")
        self.label_joueur.pack(side=tk.BOTTOM, pady=(10,10))

        self.dessiner_quadrillage()

        self.canevas.bind("<Button-1>", self.selectionner_case)

    def calculer_taille_case(self):
        self.cote_case = min(self.root.winfo_screenwidth(), self.root.winfo_screenheight() - 100) / (2 * self.taille_plateau)

    def dessiner_quadrillage(self):
        # Calculer la position de départ pour centrer le quadrillage
        self.start_x = (self.root.winfo_screenwidth() - 2 * self.cote_case * self.taille_plateau) / 2
        self.start_y = (self.root.winfo_screenheight() - 2 * self.cote_case * self.taille_plateau) / 4  # ajuster le 3 à votre convenance

        for i in range(self.taille_plateau + 1):
            x = self.start_x + i * 2 * self.cote_case
            self.canevas.create_line(x, self.start_y, x, 2 * self.cote_case * self.taille_plateau + self.start_y, fill="white")

        for i in range(self.taille_plateau + 1):
            y = self.start_y + i * 2 * self.cote_case
            self.canevas.create_line(self.start_x, y, 2 * self.cote_case * self.taille_plateau + self.start_x, y, fill="white")

    def selectionner_case(self, event):
        x = event.x
        y = event.y

        # Vérifier que les coordonnées du clic sont à l'intérieur du quadrillage
        if self.start_x <= x < self.start_x + 2 * self.cote_case * self.taille_plateau and \
        self.start_y <= y < self.start_y + 2 * self.cote_case * self.taille_plateau:
        
            col = int((x - self.start_x) / (2 * self.cote_case))
            row = int((y - self.start_y) / (2 * self.cote_case))

            # Vérifier que la colonne et la ligne sont dans les limites du quadrillage
            if 0 <= col < self.taille_plateau and 0 <= row < self.taille_plateau:
                taille_boule = 0.7
                couleur = "blue" if self.joueur_actuel == 1 else "red"
                self.canevas.create_oval(self.start_x + col * 2 * self.cote_case + (1-taille_boule)*self.cote_case,
                                        self.start_y + row * 2 * self.cote_case + (1-taille_boule)*self.cote_case,
                                        self.start_x + (col + 1) * 2 * self.cote_case - (1-taille_boule)*self.cote_case,
                                        self.start_y + (row + 1) * 2 * self.cote_case - (1-taille_boule)*self.cote_case,
                                        fill=couleur, outline="white")

                self.joueur_actuel = 3 - self.joueur_actuel
                self.label_joueur.config(text=f"Tour du Joueur {self.joueur_actuel}")


if __name__ == "__main__":
    taille_plateau = 12
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    jeu = GameGUI(root, taille_plateau)

    root.mainloop()
