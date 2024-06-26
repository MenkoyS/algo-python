import platform
import os

try:
    from PIL import Image, ImageTk
    from pygame import mixer
    from ttkthemes import ThemedTk

except ImportError as e:
            print(f"Import Error : {e}")
            print("Please verify if you have the dependencies required : pip install -r requirements.txt")

            # Ouvrir le fichier requirements.txt dans un éditeur de texte en fonction du système d'exploitation
            if platform.system() == "Windows":
                os.system("notepad dependenciesGuide.txt")
            elif platform.system() == "Linux":
                os.system("gedit dependenciesGuide.txt")
            elif platform.system() == "Darwin":  # macOS
                os.system("open -e dependenciesGuide.txt")
            else:
                print("Unsupported operating system.")
            exit(1) 

from src.game import Game
from src.gameGUI import GameGUI
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from pygame import mixer

class WelcomeTextAnimator:
    def __init__(self, root, label):
        """
        Initialise l'objet WelcomeTextAnimator
        :param root: Fenêtre racine
        :param label: Label à animer
        """
        self.root = root
        self.label = label

        self.text = "Welcome to L-Knight Battle "
        self.xPosition = root.winfo_screenwidth() // 2
        self.speed = 300

        self.textAlreadyWritten = ""
        self.textToWrite = self.text

    def animateText(self):
        """
        Anime le texte
        """
        self.label.config(text=self.textAlreadyWritten)

        if self.textToWrite:
            currentLetter = self.textToWrite[:1]
            self.textAlreadyWritten += currentLetter
            self.textToWrite = self.textToWrite[1:]

        if self.textToWrite:
            self.root.after(self.speed, self.animateText)

class LobbyGUI:
    def __init__(self):
        """
        Initialise l'objet LobbyGUI
        """
        self.initializeWindow()
        self.initializeAudio()
        self.initializeVariables()

        mainFrame = ttk.Frame(self.root, padding=500)
        mainFrame.place(relx=0.5, rely=0.5, anchor='center')

        welcomeLabel = ttk.Label(mainFrame, text="Welcome to the Game Lobby", font=("Helvetica", 40))
        welcomeLabel.grid(row=0, column=0, columnspan=2, pady=(0, 100))

        self.welcomeTextAnimator = WelcomeTextAnimator(self.root, welcomeLabel)

        labelFontSize = int(self.root.winfo_width() / 1920)
        
        ttk.Label(mainFrame, text="Choose the size of the game board", anchor='center', 
                  font=("TkDefaultFont", labelFontSize)).grid(columnspan=3, pady=(0, 100))
        
        sizeSlider = ttk.Scale(mainFrame, from_=8, to=12, variable=self.sizeVar, orient=tk.HORIZONTAL, 
                               length=self.root.winfo_screenwidth() // 2, command=self.updateSizeSliderLabel, style="TScale")
        sizeSlider.grid(row=1, columnspan=2, pady=(20, 10))
        
        self.createPositionCanvases(mainFrame, [8, 9, 10, 11, 12], [0.5, 12.75, 25, 37.2, 49.5], 260, 'center', self.sizeCanvases)
        
        self.sizeLabel = ttk.Label(mainFrame, text=f"Size: {int(self.sizeVar.get())}x{int(self.sizeVar.get())}", 
                                   anchor='center', font=("TkDefaultFont", labelFontSize))
        self.sizeLabel.grid(row=3, column=0, columnspan=2, pady=(10, 40))

        ttk.Label(mainFrame, text="Choose pawn", anchor='center', font=("TkDefaultFont", 
                                                                labelFontSize)).grid(row=4, column=0, columnspan=3, pady=(10, 10))
        
        pawnSlider = ttk.Scale(mainFrame, from_=4, to=6, variable=self.pawnVar, orient=tk.HORIZONTAL, 
                               length=self.root.winfo_screenwidth() // 4, command=self.updatePawnSliderLabel, style="TScale")
        pawnSlider.grid(row=5, column=0, columnspan=2, pady=(20, 10))
        
        self.createPositionCanvases(mainFrame, [4, 5, 6], [13, 25, 37], 475, 'center', self.pawnCanvases)
        
        self.pawnLabel = ttk.Label(mainFrame, text=f"Chosen Pawn: {int(self.pawnVar.get())}", anchor='center', 
                                   font=("TkDefaultFont", labelFontSize))
        self.pawnLabel.grid(row=6, column=0, columnspan=2, pady=(40, 40))

        self.switchButton = ttk.Button(mainFrame, text="Go windowed", command=self.toggleFullscreen)
        self.switchButton.grid(row=10, column=0, pady=(10, 10), columnspan=2)

        newWindowButton = ttk.Button(mainFrame, text="Play vs Friend", command=self.openNewWindow)
        newWindowButton.grid(row=8, column=0, pady=(10, 10), columnspan=2)
        
        playervsbotButton = ttk.Button(mainFrame, text="Play vs AI", command=self.commandeBot)
        playervsbotButton.grid(row=9, column=0, pady=(10, 10), columnspan=2)

        quitButton = ttk.Button(mainFrame, text="Quit", command=self.confirmQuit)
        quitButton.grid(row=11, column=0, pady=(10, 10), columnspan=2)

        volumeIconLabel = ttk.Label(mainFrame, text="🔊", font=("Segoe UI Emoji", 12))
        volumeIconLabel.grid(row=12, column=0, pady=(30, 0), padx=(10, 5), sticky='e')

        volumeSlider = ttk.Scale(mainFrame, from_=0, to=100, variable=self.volumeVar, orient=tk.HORIZONTAL, 
                                 length=self.root.winfo_screenwidth() // 4, command=self.updateVolume, style="TScale")
        volumeSlider.grid(row=12, column=1, columnspan=2, pady=(30, 0), padx=(0, 10), sticky='w')

        self.welcomeTextAnimator.animateText()

    def initializeWindow(self):
        """
        Initialise la fenêtre
        """
        self.root = ThemedTk(theme="black")
        self.root.title("Game Lobby")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.resizable(False, False)
        self.root.attributes('-fullscreen', True)

    def initializeAudio(self):
        """
        Initialise l'audio
        """
        mixer.init()
        mixer.music.load('./assets/sounds/AmbientGuitarLobby.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    def initializeVariables(self):
        """
        Initialise les variables
        """
        self.sizeVar = tk.DoubleVar(value=10)
        self.pawnVar = tk.DoubleVar(value=5)
        self.volumeVar = tk.DoubleVar(value=50)
        self.sizeCanvases = []
        self.pawnCanvases = []

    def createPositionCanvases(self, frame, values, positions, yPosition, anchor, canvases):
        """
        Crée des canvas pour afficher les positions des sliders
        :param frame: Frame dans laquelle les canvas seront placés
        :param values: Valeurs des sliders
        :param positions: Positions des canvas
        :param yPosition: Position Y des canvas
        :param anchor: Ancrage des canvas
        :param canvases: Liste dans laquelle les canvas seront ajoutés
        """
        screenWidth = self.root.winfo_screenwidth()
        for i, value in enumerate(values):
            if i < len(positions):
                xPosition = (positions[i] / 100) * screenWidth
                canvas = tk.Canvas(frame, width=1, height=15, bg="black", highlightthickness=0)
                canvas.place(x=xPosition, y=yPosition, anchor=anchor)
                canvases.append(canvas)

    def updateSizeSliderLabel(self, event=None):
        """
        Met à jour le label du slider de taille
        :param event: Événement
        """
        selectedSize = round(self.sizeVar.get())
        self.sizeVar.set(selectedSize)
        self.sizeLabel["text"] = f"Size: {selectedSize}x{selectedSize}"

    def updatePawnSliderLabel(self, event=None):
        """
        Met à jour le label du slider de pion
        :param event: Événement
        """
        selectedPawn = round(self.pawnVar.get())
        self.pawnVar.set(selectedPawn)
        self.pawnLabel["text"] = f"Chosen Pawn: {selectedPawn}"

    def updateVolume(self, event=None):
        """
        Met à jour le volume
        :param event: Événement
        """
        volumeLevel = self.volumeVar.get() / 100
        mixer.music.set_volume(volumeLevel)

    def toggleFullscreen(self):
        """
        Bascule le mode plein écran
        """
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.switchButton["text"] = "Go fullscreen"
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        else:
            self.root.attributes('-fullscreen', True)
            self.switchButton["text"] = "Go windowed"

    def confirmQuit(self):
        """
        Demande une confirmation avant de quitter
        """
        result = messagebox.askquestion("Confirmation", "Do you really want to leave?")
        if result == 'yes':
            self.root.destroy()

    def openNewWindow(self):
        """
        Ouvre une nouvelle fenêtre
        """
        self.root.destroy()
        mixer.music.stop()
        game = Game(rows=int(self.sizeVar.get()), columns=int(self.sizeVar.get()), pawnsToAlign=int(self.pawnVar.get()), botMode=False)
        newWindow = GameGUI(game)
        newWindow.run()

    def commandeBot(self):
        """
        Ouvre une nouvelle fenêtre
        """
        self.root.destroy()
        mixer.music.stop()
        game = Game(rows=int(self.sizeVar.get()), columns=int(self.sizeVar.get()), pawnsToAlign=int(self.pawnVar.get()), botMode=True)
        newWindow = GameGUI(game)
        newWindow.run()

    def run(self):
        try:
            import tkinter as tk
            import os
            from PIL import Image, ImageTk
            from pygame import mixer
            from tkinter import ttk, messagebox
            from ttkthemes import ThemedTk

        except ImportError as e:
            print(f"Erreur d'importation : {e}")
            print("Veuillez vérifier les dépendances en exécutant : pip install -r requirements.txt")
            print("Le fichier requirements.txt doit contenir les modules suivants :")
            print("tkinter, Pillow, pygame, ttkthemes")

            # Ouvrir le fichier requirements.txt dans un éditeur de texte en fonction du système d'exploitation
            if platform.system() == "Windows":
                os.system("notepad requirements.txt")
            elif platform.system() == "Linux":
                os.system("gedit requirements.txt")
            elif platform.system() == "Darwin":  # macOS
                os.system("open -e requirements.txt")
            else:
                print("Système d'exploitation non pris en charge. Veuillez ouvrir requirements.txt manuellement.")
            exit(1) 
        self.root.mainloop()
        