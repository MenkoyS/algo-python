from tkinter import messagebox
from sys import exit
from lobbyGUI import LobbyGUI

class EndGameMessageBox:
    def __init__(self, winner, parentWindow):
        self.winner = winner
        self.parentWindow = parentWindow

    def run(self):
        message = f"Player {self.winner} wins!"
        detail = "Do you want to replay?"
        response = messagebox.askquestion(title="Game Over", message=message, detail=detail, icon="question", parent=self.parentWindow,)

        if response == "yes":
            self.parentWindow.destroy()
            LobbyGUI().run()

        elif response == "false" or not response:
            self.parentWindow.destroy()
            exit()
