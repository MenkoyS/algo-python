from src.game import Game
from src.gameGUI import GameGUI

import tkinter as tk
from tkinter import ttk, messagebox

from ttkthemes import ThemedTk
from pygame import mixer

class WelcomeTextAnimator:
    def __init__(self, root, label):
        self.root = root
        self.label = label

        self.text = "Welcome to L-Knight-Battle "
        self.xPosition = root.winfo_screenwidth() // 2
        self.speed = 300

        self.textAlreadyWritten = ""
        self.textToWrite = self.text

    def animateText(self):
        self.label.config(text=self.textAlreadyWritten)

        if self.textToWrite:
            currentLetter = self.textToWrite[:1]
            self.textAlreadyWritten += currentLetter
            self.textToWrite = self.textToWrite[1:]

        if self.textToWrite:
            self.root.after(self.speed, self.animateText)

class LobbyGUI:
    def __init__(self):
        self.initializeWindow()
        self.initializeAudio()
        self.initializeVariables()

        mainFrame = ttk.Frame(self.root, padding=500)
        mainFrame.place(relx=0.5, rely=0.5, anchor='center')

        welcomeLabel = ttk.Label(mainFrame, text="Welcome to the Game Lobby", font=("Helvetica", 40))
        welcomeLabel.grid(row=0, column=0, columnspan=2, pady=(0, 100))

        self.welcomeTextAnimator = WelcomeTextAnimator(self.root, welcomeLabel)

        labelFontSize = int(self.root.winfo_width() / 1920)
        ttk.Label(mainFrame, text="Choose the size of the game board", anchor='center', font=("TkDefaultFont", labelFontSize)).grid(columnspan=3, pady=(0, 100))
        sizeSlider = ttk.Scale(mainFrame, from_=8, to=12, variable=self.sizeVar, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 2, command=self.updateSizeSliderLabel, style="TScale")
        sizeSlider.grid(row=1, columnspan=2, pady=(20, 10))
        self.createPositionCanvases(mainFrame, [8, 9, 10, 11, 12], [0.5, 12.75, 25, 37.2, 49.5], 260, 'center', self.sizeCanvases)
        self.sizeLabel = ttk.Label(mainFrame, text=f"Size: {int(self.sizeVar.get())}x{int(self.sizeVar.get())}", anchor='center', font=("TkDefaultFont", labelFontSize))
        self.sizeLabel.grid(row=3, column=0, columnspan=2, pady=(10, 40))

        ttk.Label(mainFrame, text="Choose pawn", anchor='center', font=("TkDefaultFont", labelFontSize)).grid(row=4, column=0, columnspan=3, pady=(10, 10))
        pawnSlider = ttk.Scale(mainFrame, from_=4, to=6, variable=self.pawnVar, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 4, command=self.updatePawnSliderLabel, style="TScale")
        pawnSlider.grid(row=5, column=0, columnspan=2, pady=(20, 10))
        self.createPositionCanvases(mainFrame, [4, 5, 6], [13, 25, 37], 475, 'center', self.pawnCanvases)
        self.pawnLabel = ttk.Label(mainFrame, text=f"Chosen Pawn: {int(self.pawnVar.get())}", anchor='center', font=("TkDefaultFont", labelFontSize))
        self.pawnLabel.grid(row=6, column=0, columnspan=2, pady=(40, 40))

        self.switchButton = ttk.Button(mainFrame, text="Go windowed", command=self.toggleFullscreen)
        self.switchButton.grid(row=10, column=0, pady=(10, 10), columnspan=2)

        newWindowButton = ttk.Button(mainFrame, text="Play vs Friend", command=self.openNewWindow)
        newWindowButton.grid(row=8, column=0, pady=(10, 10), columnspan=2)
        
        playervsbotButton = ttk.Button(mainFrame, text="Play vs AI") # - command=self.commandebot
        playervsbotButton.grid(row=9, column=0, pady=(10, 10), columnspan=2)

        quitButton = ttk.Button(mainFrame, text="Quit", command=self.confirmQuit)
        quitButton.grid(row=11, column=0, pady=(10, 10), columnspan=2)

        volumeIconLabel = ttk.Label(mainFrame, text="🔊", font=("Segoe UI Emoji", 12))  # Utilisez la police qui prend en charge les emojis
        volumeIconLabel.grid(row=12, column=0, pady=(30, 0), padx=(10, 5), sticky='e')

        volumeSlider = ttk.Scale(mainFrame, from_=0, to=100, variable=self.volumeVar, orient=tk.HORIZONTAL, length=self.root.winfo_screenwidth() // 4, command=self.updateVolume, style="TScale")
        volumeSlider.grid(row=12, column=1, columnspan=2, pady=(30, 0), padx=(0, 10), sticky='w')

        self.welcomeTextAnimator.animateText()

    def initializeWindow(self):
        self.root = ThemedTk(theme="black")
        self.root.title("Game Lobby")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.resizable(False, False)
        self.root.attributes('-fullscreen', True)

    def initializeAudio(self):
        mixer.init()
        mixer.music.load('./assets/sounds/AmbientGuitarLobby.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    def initializeVariables(self):
        self.sizeVar = tk.DoubleVar(value=10)
        self.pawnVar = tk.DoubleVar(value=5)
        self.volumeVar = tk.DoubleVar(value=50)
        self.sizeCanvases = []
        self.pawnCanvases = []

    def createPositionCanvases(self, frame, values, positions, yPosition, anchor, canvases):
        screenWidth = self.root.winfo_screenwidth()
        for i, value in enumerate(values):
            if i < len(positions):
                xPosition = (positions[i] / 100) * screenWidth
                canvas = tk.Canvas(frame, width=1, height=15, bg="black", highlightthickness=0)
                canvas.place(x=xPosition, y=yPosition, anchor=anchor)
                canvases.append(canvas)

    def updateSizeSliderLabel(self, event=None):
        selectedSize = round(self.sizeVar.get())
        self.sizeVar.set(selectedSize)
        self.sizeLabel["text"] = f"Size: {selectedSize}x{selectedSize}"

    def updatePawnSliderLabel(self, event=None):
        selectedPawn = round(self.pawnVar.get())
        self.pawnVar.set(selectedPawn)
        self.pawnLabel["text"] = f"Chosen Pawn: {selectedPawn}"

    def updateVolume(self, event=None):
        volumeLevel = self.volumeVar.get() / 100
        mixer.music.set_volume(volumeLevel)

    def toggleFullscreen(self):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.switchButton["text"] = "Go fullscreen"
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        else:
            self.root.attributes('-fullscreen', True)
            self.switchButton["text"] = "Go windowed"

    def confirmQuit(self):
        result = messagebox.askquestion("Confirmation", "Do you really want to leave?")
        if result == 'yes':
            self.root.destroy()

    def openNewWindow(self):
        self.root.destroy()
        mixer.music.stop()
        game = Game(rows=int(self.sizeVar.get()), columns=int(self.sizeVar.get()), pawnsToAlign=int(self.pawnVar.get()))
        newWindow = GameGUI(game)
        newWindow.run()

    def run(self):
        self.root.mainloop()