from unittest import TestCase
from game.player import Player


class TestPlayer(TestCase):
    def setUp(self):
        self.player = Player()

    def test_place_ships(self):
        self.player.place_ships(sizes=[5, 4, 3, 3, 2])
        self.assertRaises(TypeError, len(self.player.ships), 5)
        self.assertEqual(len(self.player.indexes), 17)


