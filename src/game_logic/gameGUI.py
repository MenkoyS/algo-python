import tkinter as tk
from game import Game

class GameGUI:
    """
    Initialize the graphical user interface for the game board.
    :param game: Game, An instance of the Game class representing the game logic.
    """

    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.round = -1
        self.playerToPlay = self.game.getPlayer1()

        # Create a 2D list to store references to the labels
        self.labels = [[None for _ in range(self.game.getColumns())] for _ in range(self.game.getRows())]

        # Create the game board labels
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                label = tk.Label(self.window, text="", width=5, height=2,
                                 relief=tk.RIDGE, borderwidth=1, bg="black", fg="white")
                label.grid(row=row, column=col)
                label.bind("<Button-1>", lambda event, r=row,
                           c=col: self.on_label_click(r, c))
                self.labels[row][col] = label

        # Update the board after creating clickable labels
        self.update_board()

    def on_label_click(self, row, col):
        """
        Handle the click event on a label.
        :param row: int, The row index of the clicked label.
        :param col: int, The column index of the clicked label.
        """
        # Handle clicks based on the game state
        if self.round == -1:
            # Place player 1 pawn
            self.game.getPlayer1().setCoordX(col)
            self.game.getPlayer1().setCoordY(row)
            self.game.setCell(row, col, self.game.getPlayer1())

            # Update the board GUI
            self.labels[row][col].config(state=tk.DISABLED)
            self.labels[row][col].unbind("<Button-1>")
            self.update_board()
            self.round += 1

        elif self.round == 0:
            # Place player 2 pawn
            self.game.getPlayer2().setCoordX(col)
            self.game.getPlayer2().setCoordY(row)
            self.game.setCell(row, col, self.game.getPlayer2())

            # Update the board GUI
            self.labels[row][col].config(state=tk.DISABLED)
            self.labels[row][col].unbind("<Button-1>")
            self.update_board()
            self.round += 1

        else:
            # Handle players' moves
            if (col, row) in self.game.possibleCell(self.playerToPlay):
                self.game.movePawn(self.playerToPlay, (col, row))
                self.labels[row][col].config(state=tk.DISABLED)  # Deactivate label
                self.labels[row][col].unbind("<Button-1>")
                self.update_board()
                self.round += 1

                # If the player has won
                if self.game.checkWin(self.playerToPlay, self.game.pawnsToAlign):
                    winner = self.playerToPlay.getPlayer()
                    print(f"Player {winner} won !")
                    return winner

                # Inverse player turn
                self.playerToPlay = self.game.getPlayer2() if self.playerToPlay == self.game.getPlayer1() else self.game.getPlayer1()

    def update_board(self):
        """
        Update the text on the labels based on the game state.
        """
        # Update the text on the labels based on the game state
        for row in range(self.game.rows):
            for col in range(self.game.columns):
                cell_value = self.game.getCell(row, col)
                text = "B" if cell_value == 1 else "R" if cell_value == 2 else "1" if cell_value == self.game.player1 else "2" if cell_value == self.game.player2 else ""
                self.labels[row][col].config(text=text)

    def run(self):
        """
        Run the Tkinter main loop to display the game GUI.
        """
        self.window.mainloop()

if __name__ == "__main__":
    game = Game()
    game_gui = GameGUI(game)
    game_gui.run()
