from src.game_logic.game import Game
from src.GUI.lobbyGUI import *

if __name__ == "__main__":
    game = Game(rows=10, columns=10, pawnsToAlign=5)

    root = tk.Tk()
    root.title("Game GUI")

    game_gui = LobbyGUI(root, game)

    root.mainloop()