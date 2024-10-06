import random
from game.player import Player


class Game:
    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.computer_turn = True if not self.human1 else False
        self.over = False
        self.result = None

    def make_move(self, index):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False

        # set miss "M" or hit "H"
        if index in opponent.indexes:
            player.search[index] = "H"
            hit = True

            # check if ship is sunk ("S")
            for ship in opponent.ships:
                sunk = True
                for index in ship.indexes:
                    if player.search[index] == "U":
                        sunk = False
                        break
                if sunk:
                    for index in ship.indexes:
                        player.search[index] = "S"

        else:
            player.search[index] = "M"

        # check if game over
        game_over = True
        for index in opponent.indexes:
            if player.search[index] == "U":
                game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        # change the active team
        if not hit:
            self.player1_turn = not self.player1_turn

            # switch between human and computer turns
            if (self.human1 and not self.human2) or (not self.human1 and self.human2):
                self.computer_turn = not self.computer_turn

    def random_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "U"]
        if len(unknown) > 0:
            random_index = random.choice(unknown)
            self.make_move(random_index)

    def basic_ai(self):

        # setup
        search = self.player1.search if self.player1_turn else self.player2.search
        unknowns = [i for i, square in enumerate(search) if square == "U"]
        hits = [i for i, square in enumerate(search) if square == "H"]

        # search in neighborhood of hits
        unknown_with_neighboring_hits1 = []
        unknown_with_neighboring_hits2 = []

        for unknown in unknowns:
            if unknown+1 in hits or unknown-1 in hits or unknown-10 in hits or unknown+10 in hits:
                unknown_with_neighboring_hits1.append(unknown)
            if unknown+2 in hits or unknown-2 in hits or unknown-20 in hits or unknown+20 in hits:
                unknown_with_neighboring_hits2.append(unknown)

        # pick "U" square with direct and level-2 neighbor both marked as "H"
        for unknown in unknowns:
            if unknown in unknown_with_neighboring_hits1 and unknown in unknown_with_neighboring_hits2:
                self.make_move(unknown)
                return

        # pick "U" square that has a neighbor marked as "H"
        if len(unknown_with_neighboring_hits1) > 0:
            self.make_move(random.choice(unknown_with_neighboring_hits1))
            return

        # checker board pattern
        checker_board = []
        for unknown in unknowns:
            row = unknown // 10
            column = unknown % 10
            if (row + column) % 2 == 0:
                checker_board.append(unknown)
        if len(checker_board) > 0:
            self.make_move(random.choice(checker_board))
            return

        # random move
        self.random_ai()
