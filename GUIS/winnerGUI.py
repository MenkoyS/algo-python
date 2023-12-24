import os
import tkinter as tk

# Nom de l'image
nom_image = 'test.png'

# Construire le chemin relatif depuis le répertoire courant
chemin_rel = os.path.join(os.getcwd(), 'assets', 'images', nom_image)

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Fenêtre en Plein Écran")

# Charger l'image de fond avec PhotoImage
image_tk = tk.PhotoImage(file=chemin_rel)

# Afficher l'image de fond en plein écran
fenetre.attributes('-fullscreen', True)

# Ajouter un label pour afficher l'image
label_image = tk.Label(fenetre, image=image_tk)
label_image.place(relwidth=1, relheight=1)

# Désactiver la gestion de la taille de la fenêtre
fenetre.resizable(False, False)

# Lancer la boucle principale
fenetre.mainloop()
