import os
import tkinter as tk

nom_image = 'test.png'
chemin_rel = os.path.join(os.getcwd(), 'assets', 'images', nom_image)

fenetre = tk.Tk()
fenetre.title("Fenêtre en Plein Écran")

image_tk = tk.PhotoImage(file=chemin_rel)

fenetre.attributes('-fullscreen', True)

label_image = tk.Label(fenetre, image=image_tk)
label_image.place(relwidth=1, relheight=1)

fenetre.resizable(False, False)

fenetre.mainloop()
