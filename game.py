from pawn import Pawn

class Game:
    """
    Initialize the game board class.
    :param rows: 8 <= int <= 12, The number of rows on the game board.
    :param columns: 8 <= int <= 12, The number of columns on the game board.
    :param pawnsToAlign: 4 <= int <= 6, The number of pawns needed to win the game.
    """

    def __init__(self, rows=10, columns=10, pawnsToAlign=5):
        self.rows = rows
        self.columns = columns
        self.pawnsToAlign = pawnsToAlign

        self.player1 = Pawn(1)
        self.player2 = Pawn(2)
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def setRows(self, numberRows):
        """
        Set the number of rows on the game board.
        :param numberRows: 8 <= int <= 12, The new number of rows.
        """
        self.rows = numberRows

    def setColumns(self, numberColumns):
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

    def setCell(self, row, column, value):
        """
        Set the value of a cell on the game board.
        :param row: int, The row index of the cell.
        :param column: int, The column index of the cell.
        :param value: int, The new value for the cell.
        """
        self.board[row][column] = value

    def possibleCell(self, pawn):
        """
        Get a list of possible cells for the pawn to move to.
        :param pawn: object, The pawn for which to find possible cells.
        :return: list<tuple>, A list of possible cell coordinates.
        """
        pawnX = pawn.getCoordX()
        pawnY = pawn.getCoordY()
        return [(x, y) for x, y in [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
                if 0 <= pawnX+x < self.columns and 0 <= pawnY+y < self.rows]
    
    def movePawn(self, origin, destination, pawn):
        """
        Move a pawn from the origin to the destination on the game board.
        :param origin: tuple, The coordinates (x, y) of the pawn's current position.
        :param destination: tuple, The coordinates (x, y) of the pawn's new position.
        :param pawn: object, The pawn to be moved.
        """
        originX, originY = origin
        destinationX, destinationY = destination
        self.board[destinationY][destinationX] = pawn
        self.board[originY][originX] = pawn.getPlayer

    def checkWin(self):
        """
        Check if a player has won the game.
        :return: bool, True if a player has won, False otherwise.
        """

    def gameLoop(self):
        """
        Main game loop to handle game logic.
        """
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]