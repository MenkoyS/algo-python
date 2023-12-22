import tkinter as tk

class Pawn:
    def __init__(self, player=1, coordX=0, coordY=0) -> None:
        self.player = 0
        self.coordX = 0
        self.coordY = 0
    
    def getCoordX(self):
        return self.coordX
    
    def getCoordY(self):
        return self.coordY
    
    def getPlayer(self):
        return self.coordX
    
    def setCoordX(self, newCoordX):
        self.coordX = newCoordX

    def setCoordY(self, newCoordY):
        self.coordY = newCoordY

class Game:
    def __init__(self, rows=10, cols=10, pawnsToAlign=5):
        self.rows = rows
        self.cols = cols
        self.pawnsToAlign = pawnsToAlign

        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.player1 = Pawn(1)
        self.player2 = Pawn(2)
    
    def setRows(self, numberRows):
        self.rows = numberRows
    
    def setCols(self, numberCols):
        self.cols = numberCols

    def getCell(self, row, col):
        return self.board[row][col]

    def setCell(self, row, col, value):
        self.board[row][col] = value

    def possibleCell(self, pawn):
        pass

    def checkWin(self):
        pass

    def gameLoop(self):
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