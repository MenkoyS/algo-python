import unittest
from game import Game
from pawn import Pawn

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game(rows=5, columns=5, pawnsToAlign=3)

    def test_initialization(self):
        self.assertEqual(self.game.rows, 5)
        self.assertEqual(self.game.columns, 5)
        self.assertEqual(self.game.pawnsToAlign, 3)

    def test_setRows(self):
        self.game.setRows(8)
        self.assertEqual(self.game.rows, 8)

    def test_setColumns(self):
        self.game.setColumns(8)
        self.assertEqual(self.game.columns, 8)

    def test_getCell(self):
        self.assertEqual(self.game.getCell(0, 0), 0)

    def test_setCell(self):
        self.game.setCell(0, 0, 1)
        self.assertEqual(self.game.getCell(0, 0), 1)

    def test_possibleCell(self):
        pawn = Pawn(1, 2, 2)
        possible_cells = self.game.possibleCell(pawn)
        self.assertIn((3, 4), possible_cells)
        self.assertNotIn((2, 2), possible_cells)  # The current position should not be in possible moves

    def test_movePawn(self):
        pawn = Pawn(1, 1, 1)
        self.game.movePawn(pawn, (2, 2))
        self.assertIs(self.game.getCell(2, 2), pawn)
        self.assertEqual(self.game.getCell(1, 1), 1)

    def test_checkDiagonals(self):
        player = Pawn(1)
        # Test a win on the right diagonal
        self.game.board = [[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]]
        self.assertTrue(self.game.checkDiagonals(player, 3, (2, 2)))

        # Test a win on the left diagonal
        self.game.board = [[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0]]
        self.assertTrue(self.game.checkDiagonals(player, 3, (0, 2)))

        # Test no win on diagonals
        self.assertFalse(self.game.checkDiagonals(player, 3, (0, 0)))

    def test_checkLines(self):
        player = Pawn(1)
        # Test a win horizontally
        self.game.board = [[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertTrue(self.game.checkLines(player, 3, (0, 2)))

        # Test a win vertically
        self.game.board = [[0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertTrue(self.game.checkLines(player, 3, (2, 0)))

        # Test no win on lines
        self.assertFalse(self.game.checkLines(player, 3, (0, 0)))

    def test_checkWin(self):
        player = Pawn(1)
        # Test a win horizontally
        self.game.board = [[1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertTrue(self.game.checkWin(player, 3))

        # Test a win vertically
        self.game.board = [[1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertTrue(self.game.checkWin(player, 3))

        # Test a win diagonally
        self.game.board = [[1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertTrue(self.game.checkWin(player, 3))

        # Test no win
        self.game.board = [[0, 1, 0, 0, 0],
                           [0, 1, 0, 1, 1],
                           [0, 0, 1, 0, 0],
                           [1, 0, 0, 0, 0],
                           [1, 0, 0, 1, 1]]
        self.assertFalse(self.game.checkWin(player, 3))

if __name__ == '__main__':
    unittest.main()
