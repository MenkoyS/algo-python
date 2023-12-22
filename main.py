import tkinter as tk
import random

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    def getCell(self, row, col):
        return self.board[row][col]

    def toggleCell(self, row, col):
        self.board[row][col] = 1 - self.board[row][col]

    def checkWin(self):
        pass

class GameGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.buttons = [[tk.Button(root, width=2, height=1, command=lambda r=row, c=col: self.onButtonClick(r, c))
                         for col in range(game.cols)] for row in range(game.rows)]

        self.setupGui()

    def setupGui(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                self.buttons[row][col].grid(row=row, column=col)

    def onButtonClick(self, row, col):
        self.game.toggleCell(row, col)
        self.updateGui()

    def updateGui(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                cell_value = self.game.getCell(row, col)
                if cell_value == 1:
                    self.buttons[row][col].config(bg="black")
                else:
                    self.buttons[row][col].config(bg="white")

if __name__ == "__main__":
    game = Game(rows=10, cols=10)

    root = tk.Tk()
    root.title("Game GUI")

    game_gui = GameGUI(root, game)

    root.mainloop()