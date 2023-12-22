import tkinter as tk

class GameGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.buttons = [[tk.Button(root, width=2, height=1, command=lambda r=row, c=col: self.onButtonClick(r, c))
                         for col in range(game.columns)] for row in range(game.rows)]

        self.setupGui()

    def setupGui(self):
        for row in range(self.game.rows):
            for col in range(self.game.columns):
                self.buttons[row][col].grid(row=row, column=col)

    def onButtonClick(self, row, column):
        self.game.setCell(row, column, 1)
        self.updateGui()

    def updateGui(self):
        for row in range(self.game.rows):
            for col in range(self.game.columns):
                cell_value = self.game.getCell(row, col)
                if cell_value == 1:
                    self.buttons[row][col].config(bg="black")
                else:
                    self.buttons[row][col].config(bg="white")