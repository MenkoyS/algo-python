import tkinter as tk
from tkinter import messagebox
from sys import exit

from pygame import mixer

from game import Game

class GameGUI:
    def __init__(self, game) -> None:
        """
        Initializes the Game GUI.
        :param game: object<Game>, The instance of the game.
        """
        self.game = game
        self.round = 1
        self.player_placed = 0
        self.playerToPlay = self.game.getPlayer1()

        # Initialize main window
        self.init_window()

        # Initialize pygame mixer for sound
        mixer.init()
        self.move_sound = mixer.Sound('assets/sounds/PawnMove.mp3')

    def init_window(self) -> None:
        """
        Initializes the main window.
        """
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.setup_fullscreen()

        # Create board frame and canvases
        self.board_frame = self.create_board_frame()
        self.canvases = self.create_board_canvases()
        self.update_board()

        # Create button frame and buttons
        self.button_frame = self.create_button_frame()
        self.setup_buttons()

        # Labels for turn and round
        self.turn_label = tk.Label(self.button_frame, text="Turn: Player 1", font=("Arial", 12), bg="black", fg="white")
        self.turn_label.pack()

        self.round_label = tk.Label(self.button_frame, text="Round: 1", font=("Arial", 12), bg="black", fg="white")
        self.round_label.pack(pady=15)

    def setup_fullscreen(self) -> None:
        """
        Sets up the window to fullscreen mode.
        """
        self.window.attributes('-fullscreen', True)
        self.window.resizable(False, False)
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()-40}")

    def create_board_frame(self) -> tk.Frame:
        """
        Creates the frame for the game board.
        :return: object<Frame>, The frame for the game board.
        """
        board_frame = tk.Frame(self.window)
        board_frame.pack(side=tk.LEFT)

        for i in range(self.game.getRows()):
            board_frame.rowconfigure(i, weight=1)
        for j in range(self.game.getColumns()):
            board_frame.columnconfigure(j, weight=1)

        return board_frame

    def create_board_canvases(self) -> list[list[tk.Canvas]]:
        """
        Creates the canvases for the cells of the game board.
        :return: list<list<Canvas>>, The canvases for the cells of the game board.
        """
        cell_size = self.window.winfo_screenheight() // self.game.getRows() - 2
        canvases = [[None for _ in range(self.game.getColumns())] for _ in range(self.game.getRows())]

        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                canvas = tk.Canvas(self.board_frame, width=cell_size, height=cell_size, bg="black", highlightthickness=0)
                canvas.grid(row=row, column=col, padx=1, pady=1, ipadx=1, ipady=1)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.on_label_click(r, c))
                canvases[row][col] = canvas

        return canvases

    def create_button_frame(self) -> tk.Frame:
        """
        Creates the frame for the buttons.
        :return: object<Frame>, The frame for the buttons.
        """
        button_frame = tk.Frame(self.window)
        button_frame.config(width=self.window.winfo_screenwidth()-self.window.winfo_screenheight(), bg="black")
        button_frame.pack(side=tk.RIGHT, padx=100)
        return button_frame

    def setup_buttons(self) -> None:
        """
        Sets up the buttons.
        """
        button_width = self.window.winfo_screenwidth() // 40
        button_height = self.window.winfo_screenheight() // 300

        buttons = [
            ("Restart", "#4CAF50", self.restart_game),
            ("Save", "#1565C0", self.save),
            ("Windowed", "#FFC107", self.toggle_fullscreen),
            ("Quit", "#D32F2F", self.quit)
        ]

        for text, bg_color, command_func in buttons:
            button = tk.Button(self.button_frame, text=text, width=button_width, height=button_height,
                               font=("Arial", 12), bg=bg_color, fg="white", padx=10, pady=5, bd=2, command=command_func)
            button.pack(pady=15, padx=20)

    def on_label_click(self, row, col) -> None:
        """
        Handles the click event on a cell.
        """
        if self.player_placed < 2:
            self.place_pawn(self.game.getPlayer1() if self.player_placed == 0 else self.game.getPlayer2(), row, col)
            self.player_placed += 1
        else:
            self.handle_players_moves(row, col)

        self.update_board()

    def place_pawn(self, player, row, col) -> None:
        """
        Places a pawn on the game board.
        :param player: object<Pawn>, Player object
        :param row: int, Row index
        :param col: int, Column index
        """
        player.setCoordX(col)
        player.setCoordY(row)
        self.game.setCell(row, col, player)

        self.canvases[row][col].config(state=tk.DISABLED)
        self.canvases[row][col].unbind("<Button-1>")

    def handle_players_moves(self, row, col) -> None:
        """
        Handles the moves of the players.
        :param row: int, Row index
        :param col: int, Column index
        """
        if (col, row) in self.game.possibleCell(self.playerToPlay):
            self.game.movePawn(self.playerToPlay, (col, row))
            self.canvases[row][col].config(state=tk.DISABLED)
            self.canvases[row][col].unbind("<Button-1>")
            self.update_board()
            self.play_sound_effect()

            if self.game.checkWin(self.playerToPlay, self.game.pawnsToAlign):
                winner = self.playerToPlay.getPlayer()
                messagebox.showinfo(title="Game Over", message=f"Player {winner} wins!",
                                    detail="Thank you for playing our game.")
                self.window.destroy()
                exit()

            self.round += 1
            self.playerToPlay = self.game.getPlayer2() if self.playerToPlay == self.game.getPlayer1() else self.game.getPlayer1()
            self.updatePlayerTurn()
            self.updateRound()

    def updatePlayerTurn(self) -> None:
        """
        Updates the label displaying the current player's turn.
        """
        self.turn_label.config(text="Turn: Player {}".format(self.playerToPlay.getPlayer()))

    def updateRound(self) -> None:
        """
        Updates the label displaying the current round number.
        """
        self.round_label.config(text="Round: {}".format(self.round))

    def play_sound_effect(self) -> None:
        """
        Plays the sound effect for pawn movement.
        """
        self.move_sound.play()

    def update_board(self) -> None:
        """
        Updates the game board display.
        """
        cell_size = self.window.winfo_screenheight() // self.game.getRows() - 2
        for row in range(self.game.getRows()):
            for col in range(self.game.getColumns()):
                cell_value = self.game.getCell(row, col)
                canvas = self.canvases[row][col]

                canvas.delete("all")

                if cell_value == self.game.player1:
                    canvas.create_oval(10, 10, cell_size-10, cell_size-10, fill="red", outline="black")
                elif cell_value == self.game.player2:
                    canvas.create_oval(10, 10, cell_size-10, cell_size-10, fill="blue", outline="black")
                elif cell_value == 1:
                    canvas.create_line(10, 10, cell_size-10, cell_size-10, fill="red", width=10)
                    canvas.create_line(10, cell_size-10, cell_size-10, 10, fill="red", width=10)
                elif cell_value == 2:
                    canvas.create_line(10, 10, cell_size-10, cell_size-10, fill="blue", width=10)
                    canvas.create_line(10, cell_size-10, cell_size-10, 10, fill="blue", width=10)
                elif self.player_placed == 2 and (col, row) in self.game.possibleCell(self.playerToPlay):
                    canvas.create_oval(20, 20, cell_size-20, cell_size-20, fill="gray", outline="gray")

    def restart_game(self) -> None:
        """
        Restarts the game using the same parameters and makes a confirmation message box.
        """
        game_size = self.game.getColumns()
        pawns_to_align = self.game.pawnsToAlign
        self.game = Game(rows=game_size, columns=game_size, pawnsToAlign=pawns_to_align)
        self.player_placed = 0
        self.round = 1
        self.playerToPlay = self.game.getPlayer1()

        # Reset canvases
        self.canvases = self.create_board_canvases()
        self.update_board()
        self.updatePlayerTurn()
        self.updateRound()

        messagebox.showinfo(title="Restart Successful", message="Game restarted successfully!",
                            detail="You can now play your new game.")

    def save(self) -> None:
        """
        Saves the game and makes a confirmation message box.
        """
        self.game.saveGame()
        messagebox.showinfo(title="Save Successful", message="Game saved successfully!",
                            detail="You can quit and load your game later.")

    def toggle_fullscreen(self) -> None:
        """
        Toggles fullscreen mode.
        """
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))

    def quit(self) -> None:
        """
        Use a message box to get a confirmation to quit the game.
        """
        if messagebox.askquestion(title="Quit", message="Would you really like to quit?") == "yes":
            if messagebox.askquestion(title="Save before quitting", message="Would you like to save before quitting?") == "yes":
                self.save()

            self.window.destroy()
            exit()

    def run(self) -> None:
        """
        Runs the GUI.
        """
        self.window.mainloop()
