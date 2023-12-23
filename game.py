from pawn import Pawn
from random import randint

class Game:
    """
    Initialize the game board class.
    :param rows: 8 <= int <= 12, The number of rows on the game board.
    :param columns: 8 <= int <= 12, The number of columns on the game board.
    :param pawnsToAlign: 4 <= int <= 6, The number of pawns needed to win the game.
    """

    def __init__(self, rows=10, columns=10, pawnsToAlign=5) -> None:
        self.rows = rows
        self.columns = columns
        self.pawnsToAlign = pawnsToAlign

        self.player1 = Pawn(1)
        self.player2 = Pawn(2)
        self.board = [[randint(0, 1) for _ in range(self.columns)] for _ in range(self.rows)]

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

    def getCell(self, row, column):
        """
        Get the value of a cell on the game board.
        :param row: int, The row index of the cell.
        :param column: int, The column index of the cell.
        :return: int, The value of the cell.
        """
        return self.board[row][column]

    def setCell(self, row, column, value) -> None:
        """
        Set the value of a cell on the game board.
        :param row: int, The row index of the cell.
        :param column: int, The column index of the cell.
        :param value: int, The new value for the cell.
        """
        self.board[row][column] = value

    def possibleCell(self, pawn) -> list:
        """
        Get a list of possible cells for the pawn to move to.
        :param pawn: object<Pawn>, The pawn for which to find possible cells.
        :return: list[tuple[int, int]], A list of possible cell coordinates.
        """
        pawnX, pawnY = pawn.getCoordX(), pawn.getCoordY()
        return [(x, y) for x, y in [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
                if 0 <= pawnX+x < self.columns and 0 <= pawnY+y < self.rows]
    
    def movePawn(self, pawn, destination) -> None:
        """
        Move a pawn from the origin to the destination on the game board.
        :param pawn: object<Pawn>, The pawn to be moved.
        :param destination: tuple, The coordinates (x, y) of the pawn's new position.
        """
        originX, originY = pawn.getCoordX, pawn.getCoordY
        destinationX, destinationY = destination
        self.board[destinationY][destinationX] = pawn
        self.board[originY][originX] = pawn.getPlayer

    def checkDiagonals(self, player, nbAligned, coordinates):
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
        if x + nbAligned < self.columns:
            diagonalsToCheck.append(1)
        if x - nbAligned >= 0:
            diagonalsToCheck.append(-1)

        # Check for each diagonal if there is 5 aligned elements of the player
        for increment in diagonalsToCheck:
            for k in range(nbAligned):
                if self.board[y + k][x + k * increment] != player.getPlayer():
                    break
                if k+1 == nbAligned:
                    return True
        return False

    def checkLines(self, player, nbAligned, coordinates):
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
        if x + nbAligned < self.columns:
            linesToCheck.append((1, 0))
        if y + nbAligned < self.rows:
            linesToCheck.append((0, 1))

        # Check for each lines if there is 5 aligned elements of the player
        for xMult, yMult in linesToCheck:
            for k in range(nbAligned):
                if self.board[y + k * yMult][x + k * xMult] != player.getPlayer():
                    break
                if k+1 == nbAligned:
                    return True
        return False


    def checkWin(self, player, nbAligned):
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

    def gameLoop(self):
        """
        Main game loop to handle game logic.
        """
        hasPlayerWon = False
        round = 1
        playerToPlay = self.player1

        # Replace getting coords by clicking in GUI
        player1xCoord = int(input("Choose x coordinate to place your pawn : ")) # Horizontal
        player1yCoord = int(input("Choose y coordinate to place your pawn : ")) # Vertical
        
        player2xCoord = int(input("Choose x coordinate to place your pawn : ")) # Horizontal
        player2yCoord = int(input("Choose y coordinate to place your pawn : ")) # Vertical

        # Setting players to their chosen coordinates
        self.player1.setCoordX = player1xCoord
        self.player1.setCoordY = player1yCoord

        self.player2.setCoordX = player2xCoord
        self.player2.setCoordY = player2yCoord

        while not hasPlayerWon:
            
            # Player choose where to move
            xMove, yMove = -1, -1
            while not (xMove, yMove) in self.possibleCell(playerToPlay):
                # Replace by click on case in GUI
                xMove = int(input("Choose x coordinate to move your pawn : ")) # Horizontal
                yMove = int(input("Choose  coordinate to move your pawn : ")) # Vertical

            # We move the player to its chosen move
            self.movePawn(playerToPlay, (xMove, yMove))

            # We check if the player has won with this move
            hasPlayerWon = self.checkWin(playerToPlay, self.pawnsToAlign)
            if hasPlayerWon:
                break

            playerToPlay = self.player2 if playerToPlay == self.player1 else self.player1
            round += 1