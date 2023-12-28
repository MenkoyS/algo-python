import os
import tkinter as tk
from tkinter import Canvas, Label
from PIL import Image, ImageTk
import imageio
from pygame import mixer

videoName = 'poulet.mp4'
relativePath = os.path.join(os.getcwd(), 'assets', 'images', videoName)

window = tk.Tk()
window.title("Window with Video")
window.attributes('-fullscreen', True)

mixer.init()

musicPath = './assets/sounds/VictorySound.mp3'
mixer.music.load(musicPath)
mixer.music.set_volume(0)

video = imageio.get_reader(relativePath)
videoWidth, videoHeight = video.get_meta_data()['size']

videoCanvas = Canvas(window, width=videoWidth, height=videoHeight)
videoCanvas.place(relwidth=1, relheight=1)

winner_text = Label(window, text="Il a gagné", font=("Helvetica", 30), fg="white", bg="black", padx=200)
winner_text.place(relx=0, rely=0.5, anchor='w')

def updateVideoFrame(frame):
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image=image)
    videoCanvas.create_image(0, 0, anchor=tk.NW, image=photo)
    videoCanvas.image = photo

def quitWindow(event):
    window.destroy()

window.bind('<Escape>', quitWindow)

def playVideo():
    mixer.music.play(0)

    for frame in video:
        updateVideoFrame(frame)
        window.update()

playVideo()

window.mainloop()
