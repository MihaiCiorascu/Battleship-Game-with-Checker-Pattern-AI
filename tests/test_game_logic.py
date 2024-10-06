import unittest
from game.game_logic import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(human1=True, human2=False)

    def test_make_move(self):
        self.game.make_move(0)
        self.assertEqual(self.game.player1.search[0], "M")
        self.game.make_move(1)
        self.assertEqual(self.game.player1.search[1], "U")

