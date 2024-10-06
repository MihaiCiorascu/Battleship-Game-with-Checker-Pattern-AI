from unittest import TestCase
from game.board import Board


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board()

    def test_create_board(self):
        self.assertEqual(len(self.board.SEA), 10)
        self.assertEqual(len(self.board.SEA[0]), 10)
        self.assertEqual(self.board.SEA[0][0], "0")
        self.assertEqual(self.board.SEA[9][9], "0")
