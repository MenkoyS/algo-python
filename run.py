from resources.game import Game
from GUIS.GUI import *

if __name__ == "__main__":
    game = Game(rows=10, columns=10, pawnsToAlign=5)

    root = tk.Tk()
    root.title("Game GUI")

    game_gui = GameGUI(root, game)

    root.mainloop()