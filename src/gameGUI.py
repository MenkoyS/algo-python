from src.game import Game
import tkinter as tk
from random import randint, choice
from os import remove
from tkinter import ttk
from pygame import mixer

class GameGUI:
    """
    A class representing the graphical user interface for the game.
    """

    def __init__(self, game) -> None:
        """
        Initializes the GameGUI object.
        :param game: The game object.
        """
        self.game = game
        self.initWindow()
        mixer.init()
        self.moveSound = mixer.Sound('assets/sounds/PawnMove.mp3')
        self.initVolumeBar()
        self.initializeAudio()
        self.updatePlayerTurn()
        self.updateRound()

    def initWindow(self) -> None:
        """
        Initializes the main window of the GUI.
        """
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.setupFullscreen()
        self.window.config(bg="black")

        self.boardFrame = self.createBoardFrame()
        self.canvases = self.createBoardCanvases()
        self.updateBoard()

        self.buttonFrame = self.createButtonFrame()
        self.setupButtons()

        self.turnLabel = tk.Label(self.buttonFrame, text="Turn: Player 1", font=(
            "Arial", 20), bg="black", fg="white")
        self.turnLabel.pack()

        self.roundLabel = tk.Label(self.buttonFrame, text="Round: 1", font=(
            "Arial", 20), bg="black", fg="white")
        self.roundLabel.pack(pady=40)

class GameGUI:
    """
    A class representing the graphical user interface for the game.
    """

    def __init__(self, game) -> None:
        """
        Initializes the GameGUI object.
        :param game: The game object.
        """
        self.game = game
        self.initWindow()
        mixer.init()
        self.moveSound = mixer.Sound('assets/sounds/PawnMove.mp3')
        self.initVolumeBar()
        self.initializeAudio()
        self.updatePlayerTurn()
        self.updateRound()

    def initWindow(self) -> None:
        """
        Initializes the main window of the GUI.
        """
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.setupFullscreen()
        self.window.config(bg="black")

        self.boardFrame = self.createBoardFrame()
        self.canvases = self.createBoardCanvases()
        self.updateBoard()

        self.buttonFrame = self.createButtonFrame()
        self.setupButtons()

        self.turnLabel = tk.Label(self.buttonFrame, text="Turn: Player 1", font=(
            "Arial", 20), bg="black", fg="white")
        self.turnLabel.pack()

        self.roundLabel = tk.Label(self.buttonFrame, text="Round: 1", font=("Arial", 20), bg="black", fg="white")
        self.roundLabel.pack(pady=40)

class GameGUI:
    def __init__(self, game) -> None:
        """
        Initializes the GameGUI object.
        :param game: The game object.
        """
        self.game = game
        self.initWindow()
        mixer.init()
        self.moveSound = mixer.Sound('assets/sounds/PawnMove.mp3')
        self.initVolumeBar()
        self.initializeAudio()
        self.updatePlayerTurn()
        self.updateRound()

    def initWindow(self) -> None:
        """
        Initializes the main window of the GUI.
        """
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.setupFullscreen()
        self.window.config(bg="black")

        self.boardFrame = self.createBoardFrame()
        self.canvases = self.createBoardCanvases()
        self.updateBoard()

        self.buttonFrame = self.createButtonFrame()
        self.setupButtons()

        self.turnLabel = tk.Label(self.buttonFrame, text="Turn: Player 1", font=("Arial", 20), bg="black", fg="white")
        self.turnLabel.pack()

        self.roundLabel = tk.Label(self.buttonFrame, text="Round: 1", font=("Arial", 20), bg="black", fg="white")
        self.roundLabel.pack(pady=40)

    def setupFullscreen(self) -> None:
        """
        Sets up the fullscreen mode for the window.
        """
        self.window.attributes('-fullscreen', True)
        self.window.resizable(False, False)
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()-40}")

    def createBoardFrame(self) -> tk.Frame:
        """
        Creates the frame containing the board.
        :return: The frame containing the board.
        """
        boardFrame = tk.Frame(self.window)
        boardFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        for i in range(self.game.getRows()):
            boardFrame.rowconfigure(i, weight=1)
        for j in range(self.game.getColumns()):
            boardFrame.columnconfigure(j, weight=1)

        return boardFrame

    def createBoardCanvases(self) -> list[list[tk.Canvas]]:
        """
        Creates the canvases representing the board.
        :return: The list of canvases representing the board.
        """
        cellSize = self.window.winfo_screenheight() // self.game.getRows() - 2
        canvases = [[None for _ in range(self.game.getColumns())] for _ in range(self.game.getRows())]
    
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                canvas = tk.Canvas(self.boardFrame, width=cellSize, height=cellSize, bg="black", highlightthickness=0)
                canvas.grid(row=row, column=col, padx=1, pady=1, ipadx=1, ipady=1)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.onLabelClick(r, c))
                canvases[row][col] = canvas

        return canvases

    def createButtonFrame(self) -> tk.Frame:
        """
        Creates the frame containing the buttons.
        :return: The frame containing the buttons.
        """
        buttonFrame = tk.Frame(self.window)
        buttonFrame.config(width=self.window.winfo_screenwidth(), bg="black")
        buttonFrame.pack(side=tk.RIGHT, padx=100)

        return buttonFrame

    def setupButtons(self) -> None:
        """
        Sets up the buttons.
        """
        buttonWidth = self.window.winfo_screenwidth() // 40
        buttonHeight = self.window.winfo_screenheight() // 300

        buttons = [
            ("Restart", "#FFFFFF", "black", self.restartGame),
            ("Save", "#FFFFFF", "black", self.save),
            ("Windowed", "#FFFFFF", "black", self.toggleFullscreen),
            ("Quit", "#FFFFFF", "black", self.quit),
        ]

        for text, bgColor, fgColor, commandFunc in buttons:
            button = tk.Button(self.buttonFrame, text=text, width=buttonWidth, height=buttonHeight, 
                               font=("Arial", 12), bg=bgColor, fg=fgColor, padx=10, pady=5, bd=2, command=commandFunc)
            button.pack(pady=15, padx=20)
            
        tk.Label(self.buttonFrame, text="", bg="black").pack(expand=True)

        rulesButton = tk.Button(self.buttonFrame, text="Rules", width=buttonWidth, height=buttonHeight,
                                font=("Arial", 12), bg="#FFFFFF", fg="black", padx=10, pady=5, bd=2, command=self.showRules)
        rulesButton.pack(side=tk.BOTTOM, anchor=tk.SE, padx=20)


    def initVolumeBar(self):
        """
        Initializes the volume bar.
        """
        self.volumeVar = tk.DoubleVar(value=50)
        volumeSlider = ttk.Scale(self.buttonFrame, from_=0, to=100, variable=self.volumeVar, 
                        orient=tk.HORIZONTAL, length=self.window.winfo_screenwidth() // 4, command=self.updateVolume, style="TScale")
        volumeSlider.pack(side=tk.RIGHT, padx=20, pady=30)

    def initializeAudio(self):
        """
        Initializes the audio.
        """
        mixer.init()
        mixer.music.load('./assets/sounds/AmbientPianoGame.mp3')
        mixer.music.set_volume(self.volumeVar.get() / 100)
        mixer.music.play(-1)

    def updateVolume(self, event=None):
        """
        Updates the volume.
        """
        volumeLevel = self.volumeVar.get() / 100
        mixer.music.set_volume(volumeLevel)

    def showRules(self) -> None:
        """
        Shows the rules of the game.
        """
        rulesText = """To win the game, a player must satisfy one of the following two conditions:
        
→ Align the number of marks of its color you choose in the lobby (horizontally, vertically or in one of the two diagonals). 
Note that a pawn does not count as a mark.

→ Block the opponent in the sense that he can no longer move his pawn.
        """
        
        tk.messagebox.showinfo(title="Game Rules", message=rulesText, detail="Copyright, Mog Studios, all rights deserved.")

    def onLabelClick(self, row, col) -> None:
        if self.game.playerPlaced < 2:
            self.placePawn(self.game.getPlayer1() if self.game.playerPlaced == 0 else self.game.getPlayer2(), row, col)
            self.game.playerPlaced += 1
            self.turnLabel.config(text="Turn: Player {}".format("2" if self.game.playerPlaced == 1 else "1"))
            self.updateBoard()
        else:
            self.handlePlayersMoves(row, col)

    def placePawn(self, player, row, col) -> None:
        """
        Places a pawn on the board.
        :param player: The player to place the pawn for.
        :param row: The row to place the pawn on.
        :param col: The column to place the pawn on.
        """
        player.setCoordX(col)
        player.setCoordY(row)
        self.game.setCell(row, col, player)

        self.canvases[row][col].config(state=tk.DISABLED)
        self.canvases[row][col].unbind("<Button-1>")

        if self.game.botMode:
            x, y = col, row
            player2 = self.game.getPlayer2()

            while (x, y) == (col, row):

                x = randint(0, self.game.getColumns()-1)
                y = randint(0, self.game.getRows()-1)
            player2.setCoordX(x)
            player2.setCoordY(y)
            self.game.setCell(y, x, player2)

            self.canvases[y][x].config(state=tk.DISABLED)
            self.canvases[y][x].unbind("<Button-1>")
            self.game.playerPlaced = 1
        self.updateBoard()

    def handlePlayersMoves(self, row, col) -> None:
        """
        Handles the players' moves.
        :param row: The row to place the pawn on.
        :param col: The column to place the pawn on.
        """
        if (col, row) in self.game.possibleCell(self.game.getPlayerToPlay()):
            self.game.movePawn(self.game.getPlayerToPlay(), (col, row))
            self.canvases[row][col].config(state=tk.DISABLED)
            self.canvases[row][col].unbind("<Button-1>")
            self.updateBoard()
            self.playSoundEffect()

            if self.game.checkWin(self.game.getPlayerToPlay(), self.game.pawnsToAlign):
                try:
                    remove('./src/game_save/save.txt')
                except:
                    print("No save file found")
                winner = self.game.getPlayerToPlay().getPlayer()
                mixer.music.stop()
                victorySound = mixer.Sound('./assets/sounds/VictorySound.mp3')
                victorySound.play()
                tk.messagebox.showinfo(title="Game Over", message=f"Player {winner} wins!", detail="Thank you for playing!")
                REPLAY = True if tk.messagebox.askquestion(title="Replay", message="Would you like to replay ?") == "yes" else False
                if REPLAY == True:
                    self.restartGame()
                else:
                    self.window.destroy()
                    exit()

            else:

                if self.game.botMode:
                    x, y = choice(self.game.possibleCell(self.game.getPlayer2()))
                    self.game.movePawn(self.game.getPlayer2(), (x, y))
                    self.canvases[y][x].config(state=tk.DISABLED)
                    self.canvases[y][x].unbind("<Button-1>")

                    self.game.incrementRound()
                    self.game.incrementRound()
                else:
                    self.game.incrementRound()
                    self.game.alternatePlayer()
        self.updatePlayerTurn()
        self.updateRound()            
        self.updateBoard()

    def updatePlayerTurn(self) -> None:
        """
        Updates the player turn label.
        """
        self.turnLabel.config(text="Turn: Player {}".format(
            self.game.getPlayerToPlay().getPlayer()))

    def updateRound(self) -> None:
        """
        Updates the round label.
        """
        self.roundLabel.config(text="Round: {}".format(self.game.getRound()))

    def playSoundEffect(self) -> None:
        """
        Plays a sound effect.
        """
        self.moveSound.play()

    def updateBoard(self) -> None:
        """
        Updates the board.
        """
        cellSize = self.window.winfo_screenheight() // self.game.getRows() - 2
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                cellValue = self.game.getCell(row, col)
                canvas = self.canvases[row][col]

                canvas.delete("all")

                if cellValue == self.game.player1:
                    canvas.create_oval(10, 10, cellSize-10, cellSize-10, fill="red", outline="black")
                    
                elif cellValue == self.game.player2:
                    canvas.create_oval(10, 10, cellSize-10, cellSize-10, fill="blue", outline="black")
                    
                elif cellValue == 1:
                    canvas.create_line(10, 10, cellSize-10, cellSize-10, fill="red", width=10)
                    canvas.create_line(10, cellSize-10, cellSize-10, 10, fill="red", width=10)
                    
                elif cellValue == 2:
                    canvas.create_line(10, 10, cellSize-10, cellSize-10, fill="blue", width=10)
                    canvas.create_line(10, cellSize-10, cellSize-10, 10, fill="blue", width=10)
                    
                elif self.game.playerPlaced == 2 and (col, row) in self.game.possibleCell(self.game.getPlayerToPlay()):
                    canvas.create_oval(20, 20, cellSize-20, cellSize-20, fill="gray", outline="gray")

    def restartGame(self) -> None:
        """
        Restarts the game.
        """
        gameSize = self.game.getColumns()
        pawnsToAlign = self.game.pawnsToAlign
        botMode = self.game.botMode
        self.game = Game(rows=gameSize, columns=gameSize, pawnsToAlign=pawnsToAlign, botMode=botMode)
        self.game.playerPlaced = 0
        self.game.round = 1
        self.game.playerToPlay = self.game.getPlayer1()

        self.canvases = self.createBoardCanvases()
        self.updateBoard()
        self.updatePlayerTurn()
        self.updateRound()

        tk.messagebox.showinfo(title="Restart Successful", message="Game restarted successfully!",detail="You can now play your new game.")

    def save(self) -> None:
        """
        Saves the game.
        """
        self.game.saveGame()
        tk.messagebox.showinfo(title="Save Successful", message="Game saved successfully!",detail="You can quit and load your game later.")

    def toggleFullscreen(self) -> None:
        """
        Toggles the fullscreen mode.
        """
        self.window.attributes(
            '-fullscreen', not self.window.attributes('-fullscreen'))

    def quit(self) -> None:
        """
        Quits the game.
        """
        if tk.messagebox.askquestion(title="Quit", message="Would you really like to quit?") == "yes":
            if tk.messagebox.askquestion(title="Save before quitting", message="Would you like to save before quitting?") == "yes":
                self.save()

            self.window.destroy()
            exit()

    def run(self) -> None:
        """
        Runs the GUI.
        """
        self.window.mainloop()
