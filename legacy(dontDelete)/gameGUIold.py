import tkinter as tk
from game import Game

class GameGUI:
    def __init__(self, game):
        """
        Initialize the GameGUI.

        Parameters:
        - game: An instance of the Game class.
        """
        self.game = game
        self.window = tk.Tk()
        self.window.title("GameGUI")

        # Set fullscreen
        self.window.attributes('-fullscreen', True)

        # Create a frame for the game board
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=0, column=0, sticky="nsew")

        # Create a frame for the buttons, centered vertically
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=0, column=1, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)  # Ensure center alignment

        # Create a spacer frame to center the buttons vertically
        spacer_frame = tk.Frame(self.button_frame)
        spacer_frame.pack(expand=True, fill=tk.Y)

        # Configure rows and columns to expand for both frames
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        # Configure rows and columns to expand for the game board frame
        for i in range(self.game.getRows()):
            self.board_frame.rowconfigure(i, weight=1)
        for j in range(self.game.getColumns()):
            self.board_frame.columnconfigure(j, weight=1)

        self.round = -1
        self.playerToPlay = self.game.getPlayer1()

        # Create a 2D list to store references to the labels
        self.labels = [[None for _ in range(self.game.getColumns())] for _ in range(self.game.getRows())]

        # Create the game board labels with spacing
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                label = tk.Label(self.board_frame, text="", width=5, height=2,
                                 relief=tk.RIDGE, borderwidth=1, bg="black", fg="white", font=("Helvetica", 16),
                                 padx=5, pady=5)  # Add padx and pady for spacing
                label.grid(row=row, column=col, sticky="nsew")
                label.bind("<Button-1>", lambda event, r=row,
                           c=col: self.on_label_click(r, c))
                self.labels[row][col] = label

        outer_frame = tk.Frame(self.button_frame, bg="#F0F0F0", bd=5, relief=tk.RAISED)  # Light gray background, 5-pixel border, raised relief
        outer_frame.pack(expand=True, fill=tk.BOTH)

        # Create buttons in the outer frame for vertical and horizontal centering
        btn_restart = tk.Button(outer_frame, text="Restart", command=self.restart_game, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5, bd=2)  # Green button
        btn_restart.grid(row=0, pady=10)

        btn_quit = tk.Button(outer_frame, text="Quit", command=self.window.destroy, font=("Arial", 12), bg="#D32F2F", fg="white", padx=10, pady=5, bd=2)  # Red button
        btn_quit.grid(row=1, pady=10)

        btn_save = tk.Button(outer_frame, text="Save", command=self.save, font=("Arial", 12), bg="#1565C0", fg="white", padx=10, pady=5, bd=2)  # Blue button
        btn_save.grid(row=2, pady=10)

        btn_go_window = tk.Button(outer_frame, text="Go window", command=self.window, font=("Arial", 12), bg="#FFC107", fg="black", padx=10, pady=5, bd=2)  # Yellow button
        btn_go_window.grid(row=3, pady=10)

        # Center the outer frame within its parent
        outer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Update the board after creating clickable labels
        self.update_board()

    def on_label_click(self, row, col):
        """
        Handle clicks on the game board labels.

        Parameters:
        - row: Row index of the clicked label.
        - col: Column index of the clicked label.
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
                    print(f"Player {winner} won!")
                    return winner

                # Inverse player turn
                self.playerToPlay = self.game.getPlayer2() if self.playerToPlay == self.game.getPlayer1() else self.game.getPlayer1()

    def update_board(self):
        """
        Update the game board GUI based on the current state of the game.
        """
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                cell_value = self.game.getCell(row, col)
                if cell_value == self.game.player1:
                    self.labels[row][col].config(text="", bg="red")
                elif cell_value == self.game.player2:
                    self.labels[row][col].config(text="", bg="blue")
                else:
                    self.labels[row][col].config(text="")

    def restart_game(self):
        """
        Restart the game.
        """
        # Implement the logic to restart the game
        pass

    def save(self):
        """
        Save the current state of the game.
        """
        # Implement the logic to save the game state
        pass

    def window(self):
        """
        Open a new window.
        """
        # Implement the logic to open a new window
        pass

    def run(self):
        """
        Run the main event loop of the GUI.
        """
        self.window.mainloop()

if __name__ == "__main__":
    game = Game()
    game_gui = GameGUI(game)
    game_gui.run()
