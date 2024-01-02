import tkinter as tk
from tkinter import messagebox
from sys import exit
from game import Game
import pygame

class GameGUI:
    def __init__(self, game) -> None:
        self.game = game
        self.init_window()

        # ~~> pygame mixer for sound ( line 126 )
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound('assets/sounds/PawnMove.mp3') # ~> line 126

        self.round = -1
        self.playerToPlay = self.game.getPlayer1()

    def init_window(self) -> None:
        self.window = tk.Tk()
        self.window.title("GameGUI")
        self.setup_fullscreen()

        self.board_frame = self.create_board_frame()
        self.canvases = self.create_board_canvases()
        self.update_board()

        self.button_frame = self.create_button_frame()
        self.setup_buttons()
        
        self.turn_label = tk.Label(self.button_frame, text="Turn: Player 1", font=("Arial", 12), bg="black", fg="white")
        self.turn_label.pack(pady=15, padx=20)
        
    def setup_fullscreen(self) -> None:
        self.window.attributes('-fullscreen', True)
        self.window.resizable(False, False)
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()-40}")

    def create_board_frame(self) -> tk.Frame:
        board_frame = tk.Frame(self.window)
        board_frame.pack(side=tk.LEFT)

        for i in range(self.game.getRows()):
            board_frame.rowconfigure(i, weight=1)
        for j in range(self.game.getColumns()):
            board_frame.columnconfigure(j, weight=1)

        return board_frame

    def create_board_canvases(self) -> list:
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
        button_frame = tk.Frame(self.window)
        button_frame.config(width=self.window.winfo_screenwidth()-self.window.winfo_screenheight(), bg="black")
        button_frame.pack(side=tk.RIGHT, padx=100)
        return button_frame

    def setup_buttons(self) -> None:
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
        if self.round == -1:
            self.place_pawn(self.game.getPlayer1(), row, col)
            self.round += 1
        elif self.round == 0:
            self.place_pawn(self.game.getPlayer2(), row, col)
            self.round += 1
        else:
            self.handle_players_moves(row, col)
        
        self.numberCounter()

    def place_pawn(self, player, row, col) -> None:
        player.setCoordX(col)
        player.setCoordY(row)
        self.game.setCell(row, col, player)

        self.canvases[row][col].config(state=tk.DISABLED)
        self.canvases[row][col].unbind("<Button-1>")
        self.update_board()

    def handle_players_moves(self, row, col) -> None:
        if (col, row) in self.game.possibleCell(self.playerToPlay):
            self.game.movePawn(self.playerToPlay, (col, row))
            self.canvases[row][col].config(state=tk.DISABLED)
            self.canvases[row][col].unbind("<Button-1>")
            self.update_board()
            self.play_sound_effect()  # ~~> play the sound effect
            self.round += 1

            if self.game.checkWin(self.playerToPlay, self.game.pawnsToAlign):
                winner = self.playerToPlay.getPlayer()
                messagebox.showinfo(title="Game Over", message=f"Player {winner} wins!", detail="Thank you for playing our game.")
                self.quit()

            self.playerToPlay = self.game.getPlayer2() if self.playerToPlay == self.game.getPlayer1() else self.game.getPlayer1()

            self.numberCounter()
    
    def numberCounter(self) -> None:
        player_turn = "Player 1" if self.round == -1 or self.round % 2 != 0 else "Player 2"
        self.turn_label.config(text="Turn: {}".format(player_turn))

    def play_sound_effect(self) -> None:
        self.move_sound.play() # ~~> play the sound effect

    def update_board(self) -> None:
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

    def restart_game(self) -> None:
        gameSize = self.game.getColumns()
        pawnsToAlign = self.game.pawnsToAlign
        self.game = Game(rows=gameSize, columns=gameSize, pawnsToAlign=pawnsToAlign)
        self.round = -1
        self.playerToPlay = self.game.getPlayer1()
        self.update_board()

        messagebox.showinfo(title="Restart Successfull", message="Game restarted successfully !", detail="You can now play your new game.")

    def save(self) -> None:
        self.game.saveGame()
        messagebox.showinfo(title="Save Successfull", message="Game saved successfully !", detail="You can quit and load your game later.")

    def toggle_fullscreen(self) -> None:
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))

    def quit(self) -> None:
        if messagebox.askquestion(title="Quit", message="Would you really like to quit ?") == "yes":
            if messagebox.askquestion(title="Save before quitting", message="Would you like to save before quitting ?") == "yes":
                self.save()

            self.window.destroy()
            exit()

    def run(self) -> None:
        self.window.mainloop()

settings = Game(rows=10, columns=10, pawnsToAlign=3)
app = GameGUI(settings)
app.run()
