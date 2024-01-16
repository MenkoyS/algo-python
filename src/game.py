from src.pawn import Pawn

class Game:
    """
    Initialize the game board class.
    :param rows: 8 <= int <= 12, The number of rows on the game board.
    :param columns: 8 <= int <= 12, The number of columns on the game board.
    :param pawnsToAlign: 4 <= int <= 6, The number of pawns needed to win the game.
    :param botMode: bool, Tell if the game is against a Bot
    """

    def __init__(self, rows=10, columns=10, pawnsToAlign=5, botMode=True) -> None:
        self.rows = rows
        self.columns = columns
        self.pawnsToAlign = pawnsToAlign
        self.botMode = botMode

        self.player1 = Pawn(1)
        self.player2 = Pawn(2)
        self.board = [[0 for _ in range(self.columns)]
                      for _ in range(self.rows)]
        
        self.round = 1
        self.playerToPlay = self.player1
        self.playerPlaced = 0
        
    def getRows(self) -> int:
        """
        Get the number of rows on the game board.
        :return: int, The number of rows.
        """
        return self.rows

    def getColumns(self) -> int:
        """
        Get the number of columns on the game board.
        :return: int, The number of columns.
        """
        return self.columns

    def getCell(self, row, column):
        """
        Get the value of a cell on the game board.
        :param row: int, The row index of the cell.
        :param column: int, The column index of the cell.
        :return: int, The value of the cell.
        """
        return self.board[row][column]

    def getPlayer1(self) -> object:
        """
        Get the player 1 object.
        :return: object<Pawn>, The player 1 object.
        """
        return self.player1

    def getPlayer2(self) -> object:
        """
        Get the player 2 object.
        :return: object<Pawn>, The player 2 object.
        """
        return self.player2
    
    def getRound(self) -> int:
        """
        Get the current round.
        :return: int, The current round.
        """
        return self.round
    
    def getPlayerToPlay(self) -> object:
        """
        Get the player to play.
        :return: object<Pawn>, The player to play.
        """
        return self.playerToPlay

    def setRows(self, numberRows) -> None:
        """
        Set the number of rows on the game board.
        :param numberRows: 8 <= int <= 12, The new number of rows.
        """
        self.rows = numberRows

    def setColumns(self, numberColumns) -> None:
        """
        Set the number of columns on the game board.
        :param numberColumns: 8 <= int <= 12, The new number of columns.
        """
        self.columns = numberColumns

    def setCell(self, row, column, value) -> None:
        """
        Set the value of a cell on the game board.
        :param row: int, The row index of the cell.
        :param column: int, The column index of the cell.
        :param value: int, The new value for the cell.
        """
        self.board[row][column] = value

    def incrementRound(self) -> None:
        """
        Increment the round counter.
        """
        self.round += 1

    def alternatePlayer(self) -> None:
        """
        Alternate the player to play.
        """
        self.playerToPlay = self.player1 if self.playerToPlay == self.player2 else self.player2

    def possibleCell(self, pawn) -> list:
        """
        Get a list of possible cells for the pawn to move to.
        :param pawn: object<Pawn>, The pawn for which to find possible cells.
        :return: list[tuple[int, int]], A list of possible cell coordinates.
        """
        pawnX, pawnY = pawn.getCoordX(), pawn.getCoordY()
        return [(pawnX+x, pawnY+y) for x, y in [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
                if 0 <= pawnX+x < self.columns and 0 <= pawnY+y < self.rows and self.getCell(pawnY+y, pawnX+x)==0]

    def movePawn(self, pawn, destination) -> None:
        """
        Move a pawn from the origin to the destination on the game board.
        :param pawn: object<Pawn>, The pawn to be moved.
        :param destination: tuple, The coordinates (x, y) of the pawn's new position.
        """
        originX, originY = pawn.getCoordX(), pawn.getCoordY()
        destinationX, destinationY = destination
        pawn.setCoordX(destinationX)
        pawn.setCoordY(destinationY)
        self.board[destinationY][destinationX] = pawn
        self.board[originY][originX] = pawn.getPlayer()

    def checkDiagonals(self, player, nbAligned, coordinates) -> bool:
        """
        Check if the player has aligned the required number of elements diagonally to win.
        :param player: object<Pawn>, The player for whom the win is being checked.
        :param nbAligned: int, The number of aligned elements required for a win.
        :param coordinates: tuple[int, int], The starting coordinates to check diagonals.
        :return: bool, True if the player has won diagonally, False otherwise.
        """
        x, y = coordinates
        diagonalsToCheck = []

        # Check what diagonals we need to check (left or right or both)
        if y + (nbAligned - 1) < self.columns and x + (nbAligned - 1) < self.columns:
            diagonalsToCheck.append(1)
        if y + (nbAligned - 1) < self.columns and x - (nbAligned - 1) >= 0:
            diagonalsToCheck.append(-1)

        # Check for each diagonal if there is 5 aligned elements of the player
        for increment in diagonalsToCheck:
            for k in range(nbAligned):
                if self.board[y + k][x + k * increment] != player.getPlayer():
                    break
                if k+1 == nbAligned:
                    return True
        return False

    def checkLines(self, player, nbAligned, coordinates) -> bool:
        """
        Check if the player has aligned the required number of elements horizontally or vertically to win.
        :param player: object<Pawn>, The player for whom the win is being checked.
        :param nbAligned: int, The number of aligned elements required for a win.
        :param coordinates: tuple[int, int], The starting coordinates to check lines.
        :return: bool, True if the player has won horizontally or vertically, False otherwise.
        """
        x, y = coordinates
        linesToCheck = []

        # Check what lines we need to check (horizontal or vertical or both)
        if x + nbAligned - 1 < self.columns:
            linesToCheck.append((1, 0))
        if y + nbAligned - 1 < self.rows:
            linesToCheck.append((0, 1))

        # Check for each lines if there is 5 aligned elements of the player
        for xMult, yMult in linesToCheck:
            for k in range(nbAligned):
                if self.board[y + k * yMult][x + k * xMult] != player.getPlayer():
                    break
                if k+1 == nbAligned:
                    return True
        return False

    def checkWin(self, player, nbAligned) -> bool:
        """
        Check if a player has won the game.
        :param player: object<Pawn>, The player for whom the win is being checked.
        :param nbAligned: int, The number of aligned elements required for a win.
        :return: bool, Indicating whether the player has won.
        """
        # If the enemy player can't move the player won
        enemyPlayer = self.player2 if player == self.player1 else self.player1
        if not self.possibleCell(enemyPlayer):
            return True

        # If the player has aligned the required number of elements he has won
        for yCoord in range(self.rows):
            for xCoord in range(self.columns):
                if self.checkLines(player, nbAligned, (xCoord, yCoord)) or self.checkDiagonals(player, nbAligned, (xCoord, yCoord)):
                    return True

        return False

    def saveGame(self, filename="save.txt") -> None:
        """
        Save the current state of the game to a file.
        :param filename: str, The name of the file to save the game to.
        """
        with open(f"./src/game_save/{filename}", 'w') as file:
            file.write(f"{self.rows}\n")
            file.write(f"{self.columns}\n")
            file.write(f"{self.pawnsToAlign}\n")
            file.write(f"{self.round}\n")
            file.write(f"{self.playerToPlay.getPlayer()}\n")
            file.write(f"{self.playerPlaced}\n")
            file.write(f"{self.botMode}\n")

            file.write(
                f"{self.player1.getCoordX()} {self.player1.getCoordY()}\n")
            file.write(
                f"{self.player2.getCoordX()} {self.player2.getCoordY()}\n")

            for row in self.board:
                line = []
                for cell in row:
                    if isinstance(cell, Pawn):
                        line.append(cell.getPlayer()+2)
                    else:
                        line.append(cell)
                file.write(" ".join(map(str, line)) + "\n")

    def loadGame(self, filename="save.txt") -> None:
        """
        Load the game state from a file.
        :param filename: str, The name of the file to load the game from.
        """
        try:
            with open(f"./src/game_save/{filename}", 'r') as file:
                self.rows = int(file.readline())
                self.columns = int(file.readline())
                self.pawnsToAlign = int(file.readline())
                self.round = int(file.readline())
                self.playerToPlay = self.player1 if int(file.readline()) == 1 else self.player2
                self.playerPlaced = int(file.readline())
                self.botMode = True if file.readline() == "True\n" else False

                player1_coords = tuple(map(int, file.readline().split()))
                player2_coords = tuple(map(int, file.readline().split()))

                self.player1.setCoordX(player1_coords[0])
                self.player1.setCoordY(player1_coords[1])

                self.player2.setCoordX(player2_coords[0])
                self.player2.setCoordY(player2_coords[1])

                self.board = [[self.player1 if cell == 3 else self.player2 if cell == 4 else cell for cell in map(int, line.split())] for line in file]

        except FileNotFoundError:
            print("Save file not found. Starting a new game.")
