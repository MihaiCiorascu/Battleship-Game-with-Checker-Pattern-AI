import copy
from random import randint


class Board:
    def __init__(self):
        self.ocean = "0"
        self.fire = "X"
        self.hit = "*"
        self.size = 10
        self.ships = [5, 4, 3, 3, 2]
        self.orientation = -1
        self.total_hits = []
        self.miss = 1
        self.player_alive = 17
        self.player_radar = []
        self.player_board = []
        self.ai_alive = 17
        self.ai_radar = []
        self.ai_board = []
        self.ship_position = []
        self.ship_length = []
        self.SEA = []
        self.create_board()
        self.player_radar = copy.deepcopy(self.SEA)
        self.player_board = copy.deepcopy(self.SEA)
        self.ai_radar = copy.deepcopy(self.SEA)
        self.ai_board = copy.deepcopy(self.SEA)
        self.number_board = copy.deepcopy(self.SEA)
        self.make_ship()

    def make_ship(self):
        for x in range(len(self.ships)):
            self.player_board = self.place_ship(self.ships[x], self.player_board, x)
            self.ai_board = self.place_ship(self.ships[x], self.ai_board)

    def create_board(self):
        for x in range(self.size):
            self.SEA.append([self.ocean] * self.size)

    def print_board(self):
        # print(numbers.join(""))
        print("  0 1 2 3 4 5 6 7 8 9 || 0 1 2 3 4 5 6 7 8 9")
        i = 0
        for row in range(self.size):
            print(i, " ".join(self.player_radar[row]), "||", " ".join(self.player_board[row]))
            i += 1

    def random_row(self, is_vertical, size):
        if is_vertical:
            return randint(0, self.size - size)
        else:
            return randint(0, self.size - 1)

    def random_column(self, is_vertical, size):
        if is_vertical:
            return randint(0, self.size - 1)
        else:
            return randint(size - 1, self.size - 1)

    def is_ocean(self, row, column, board):  # true if ocean
        if row < 0 or row >= self.size:
            return 0
        elif column < 0 or column >= self.size:
            return 0
        if board[row][column] == self.ocean:
            return 1
        else:
            return 0

    def is_ocean_in(self, row, column, board):
        if type(row) is not int or type(column) is not int:
            return 0
        if row < 0 or row >= self.size:
            return 0
        elif column < 0 or column >= self.size:
            return 0
        if board[row][column] == self.ocean:
            return 1
        else:
            return 0

    def place_ship(self, size, board, set_ship=None):
        # Find an unoccupied spot, then place ship on board
        # Put set_ship on ship_number_board if set_ship
        ship_row = None
        ship_column = None
        is_vertical = randint(0, 1)  # vertical ship if true
        occupied = True
        while occupied:
            occupied = False
            ship_row = self.random_row(is_vertical, size)
            ship_column = self.random_column(is_vertical, size)
            if is_vertical:
                for position in range(size):
                    if not self.is_ocean(ship_row + position, ship_column, board):
                        occupied = True
            else:
                for position in range(size):
                    if not self.is_ocean(ship_row, ship_column - position, board):
                        occupied = True
        # Place ship on boards
        if is_vertical:
            board[ship_row][ship_column] = "^"
            board[ship_row + size - 1][ship_column] = "v"
            if set_ship is not None:
                self.number_board[ship_row][ship_column] = set_ship
                self.number_board[ship_row + size - 1][ship_column] = set_ship
            for position in range(size - 2):
                board[ship_row + position + 1][ship_column] = "+"
                if set_ship is not None:
                    self.number_board[ship_row + position + 1][ship_column] = set_ship
        else:
            board[ship_row][ship_column] = ">"
            board[ship_row][ship_column - size + 1] = "<"

            if set_ship is not None:
                self.number_board[ship_row][ship_column] = set_ship
                self.number_board[ship_row][ship_column - size + 1] = set_ship
            for position in range(size - 2):
                board[ship_row][ship_column - position - 1] = "+"
                if set_ship is not None:
                    self.number_board[ship_row][ship_column - position - 1] = set_ship
        return board

    def ship_number(self, row, column):
        # Returns -1 if not found
        if self.is_ocean(row, column, self.number_board):
            return -1
        return self.ships[self.number_board[row][column]]

    def ship_sunk(self):  # true if ship sunk
        zero = 0
        if self.total_hits.count(self.total_hits[zero]) == self.ship_length[zero]:
            return 1
        return 0
