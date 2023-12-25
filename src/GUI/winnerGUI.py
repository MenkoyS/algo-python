import os
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import imageio

nom_video = 'poulet.mp4'
chemin_rel = os.path.join(os.getcwd(), 'assets', 'images', nom_video)

fenetre = tk.Tk()
fenetre.title("Fenêtre avec Vidéo")
fenetre.attributes('-fullscreen', True)

video = imageio.get_reader(chemin_rel)
video_width, video_height = video.get_meta_data()['size']

fenetre_video = Canvas(fenetre, width=video_width, height=video_height)
fenetre_video.place(relwidth=1, relheight=1)

def update_video_frame(frame):
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image=image)
    fenetre_video.create_image(0, 0, anchor=tk.NW, image=photo)
    fenetre_video.image = photo

def quitter_fenetre(event):
    fenetre.destroy()

fenetre.bind('<Escape>', quitter_fenetre)

def lire_video():
    for frame in video:
        update_video_frame(frame)
        fenetre.update()

lire_video()

fenetre.mainloop()
