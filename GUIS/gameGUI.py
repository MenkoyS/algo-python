import tkinter as tk

class JeuDeGrille:
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
        self.label_joueur.pack(side=tk.BOTTOM, pady=10)

        self.dessiner_quadrillage()

        self.canevas.bind("<Button-1>", self.selectionner_case)

    def calculer_taille_case(self):
        self.cote_case = min(self.root.winfo_screenwidth(), self.root.winfo_screenheight() - 50) / (2 * self.taille_plateau)

    def dessiner_quadrillage(self):
        for i in range(self.taille_plateau + 1):
            x = i * 2 * self.cote_case
            self.canevas.create_line(x, 0, x, 2 * self.cote_case * self.taille_plateau, fill="white")

        for i in range(self.taille_plateau + 1):
            y = i * 2 * self.cote_case
            self.canevas.create_line(0, y, 2 * self.cote_case * self.taille_plateau, y, fill="white")

    def selectionner_case(self, event):
        if 0 <= event.x < 2 * self.cote_case * self.taille_plateau and 0 <= event.y < 2 * self.cote_case * self.taille_plateau:
            col = int(event.x / (2 * self.cote_case))
            row = int(event.y / (2 * self.cote_case))

            taille_boule = 0.7
            couleur = "blue" if self.joueur_actuel == 1 else "red"
            self.canevas.create_oval(col * 2 * self.cote_case + (1-taille_boule)*self.cote_case,
                                     row * 2 * self.cote_case + (1-taille_boule)*self.cote_case,
                                     (col + 1) * 2 * self.cote_case - (1-taille_boule)*self.cote_case,
                                     (row + 1) * 2 * self.cote_case - (1-taille_boule)*self.cote_case,
                                     fill=couleur, outline="white")

            self.joueur_actuel = 3 - self.joueur_actuel
            self.label_joueur.config(text=f"Tour du Joueur {self.joueur_actuel}")

if __name__ == "__main__":
    taille_plateau = 8
    root = tk.Tk()
    root.attributes('-fullscreen', True)

    jeu = JeuDeGrille(root, taille_plateau)

    root.mainloop()
