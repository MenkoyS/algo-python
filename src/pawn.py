class Pawn:
    """
    Represents a pawn in the game.
    :param player: int, The player to whom the pawn belongs (1 or 2).
    :param coordX: int, The X-coordinate of the pawn on the game board.
    :param coordY: int, The Y-coordinate of the pawn on the game board.
    """
    
    def __init__(self, player=1, coordX=0, coordY=0) -> None:
        self.player = player
        self.coordX = coordX
        self.coordY = coordY

    def getCoordX(self) -> int:
        """
        Get the X-coordinate of the pawn.
        :return: int, The X-coordinate of the pawn.
        """
        return self.coordX

    def getCoordY(self) -> int:
        """
        Get the Y-coordinate of the pawn.
        :return: int, The Y-coordinate of the pawn.
        """
        return self.coordY

    def getPlayer(self) -> int:
        """
        Get the player to whom the pawn belongs.
        :return int: The player number (1 or 2).
        """
        return self.player

    def setCoordX(self, newCoordX) -> None:
        """
        Set the X-coordinate of the pawn.
        :param newCoordX: int, The new X-coordinate for the pawn.
        """
        self.coordX = newCoordX

    def setCoordY(self, newCoordY) -> None:
        """
        Set the Y-coordinate of the pawn.
        :param newCoordY: int, The new Y-coordinate for the pawn.
        """
        self.coordY = newCoordY