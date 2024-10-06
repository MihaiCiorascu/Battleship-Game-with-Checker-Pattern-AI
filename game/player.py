from game.ship import Ship


class Player:
    def __init__(self):
        self.ships = []
        self.search = ["U" for _ in range(100)]  # U = Unknown

        # (5) Aircraft Carrier, (4) Battleship, (3) Submarine, (3) Cruiser, (2) Destroyer
        self.place_ships(sizes=[5, 4, 3, 3, 2])
        list_of_lists = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists for index in sublist]

    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:

                # create a new ship
                ship = Ship(size)

                # check if placement is possible
                placement_is_possible = True
                for index in ship.indexes:

                    # indexes must be < 100
                    if index >= 100:
                        placement_is_possible = False
                        break

                    # ships cannot behave like the "snake" in the "Snake Game"
                    new_row = index // 10
                    new_column = index % 10
                    if new_row != ship.row and new_column != ship.column:
                        placement_is_possible = False
                        break

                    # ships cannot intersect
                    for other_ship in self.ships:
                        if index in other_ship.indexes:
                            placement_is_possible = False
                            break

                # place the ship
                if placement_is_possible:
                    self.ships.append(ship)
                    placed = True


