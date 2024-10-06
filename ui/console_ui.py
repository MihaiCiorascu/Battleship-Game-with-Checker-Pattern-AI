from random import randint
from game.board import Board


class UI:
    def __init__(self):
        self.board = Board()

    def start(self):
        print("Let's play Battleship!")
        self.board.print_board()
        ai_guess_row = None
        ai_guess_column = None
        while self.board.player_alive and self.board.ai_alive:
            try:
                guess_row = int(input("Guess Row:"))
                guess_column = int(input("Guess Column:"))
                while not self.board.is_ocean_in(guess_row, guess_column, self.board.player_radar):
                    print("Sorry, that is not a valid shot")
                    guess_row = int(input("Guess Row:"))
                    guess_column = int(input("Guess Column:"))
            except ValueError:
                print("Sorry, that is not a valid shot")
                continue

            # Legal Guess
            if self.board.ai_board[guess_row][guess_column] != self.board.ocean:
                self.board.ai_alive -= 1
                if self.board.ai_alive:
                    print("Admiral, we've hit the enemy ship!")
                    self.board.player_radar[guess_row][guess_column] = self.board.hit
                else:
                    self.board.player_radar[guess_row][guess_column] = self.board.hit
                    print("Congratulations! You sunk my battleship!")
                    break
            else:
                print("Admiral, we've missed the enemy battleship!")
                self.board.player_radar[guess_row][guess_column] = self.board.fire

            # AI turn
            print("target orientation: ", self.board.orientation)
            if not len(self.board.ship_length):  # No current targets
                # print("No Current Targets")
                self.board.second_shot = 0
                ai_guess_row = randint(0, self.board.size - 1)
                ai_guess_column = randint(0, self.board.size - 1)
                while not self.board.is_ocean(ai_guess_row, ai_guess_column, self.board.ai_radar):
                    ai_guess_row = randint(0, self.board.size - 1)
                    ai_guess_column = randint(0, self.board.size - 1)
                if not self.board.is_ocean(ai_guess_row, ai_guess_column, self.board.player_board):  # AI hit
                    self.board.miss = 0
                    self.board.player_alive -= 1
                    # print("Hit ship length: ", ship_number(ai_guess_row, ai_guess_col))
                    self.board.ship_length.append((self.board.ship_number(ai_guess_row, ai_guess_column)))
                    # print("ship_position length: ", str(len(ship_position)))
                    self.board.ship_position.extend([ai_guess_row, ai_guess_column])
                    # print("ship_position length: ", str(len(ship_position)))
                    self.board.orientation = -1
                    self.board.player_board[ai_guess_row][ai_guess_column] = self.board.hit
                    self.board.ai_radar[ai_guess_row][ai_guess_column] = self.board.hit
                    self.board.total_hits.append(self.board.number_board[ai_guess_row][ai_guess_column])
                    print("Attention Admiral! You have been hit!")
                else:
                    self.board.miss = 1
                    self.board.player_board[ai_guess_row][ai_guess_column] = self.board.fire
                    self.board.ai_radar[ai_guess_row][ai_guess_column] = self.board.fire
                    print("Good news! They've missed!")
            else:  # Find next spot to shoot on ship
                if self.board.orientation == -1:  # shot-test for orientation of hit ship
                    # ship_position swapped for ai_hit
                    print("Ship has no orientation")
                    horizontal_coordinate = 0
                    vertical_coordinate = 1
                    if self.board.is_ocean(self.board.ship_position[horizontal_coordinate] + 1, self.board.ship_position[vertical_coordinate], self.board.ai_radar):
                        ai_guess_row = self.board.ship_position[horizontal_coordinate] + 1
                        ai_guess_column = self.board.ship_position[vertical_coordinate]
                    elif self.board.is_ocean(self.board.ship_position[horizontal_coordinate] - 1, self.board.ship_position[vertical_coordinate], self.board.ai_radar):
                        ai_guess_row = self.board.ship_position[horizontal_coordinate] - 1
                        ai_guess_column = self.board.ship_position[vertical_coordinate]
                    elif self.board.is_ocean(self.board.ship_position[horizontal_coordinate], self.board.ship_position[vertical_coordinate] - 1, self.board.ai_radar):
                        ai_guess_row = self.board.ship_position[horizontal_coordinate]
                        ai_guess_column = self.board.ship_position[vertical_coordinate] - 1
                    else:
                        ai_guess_row = self.board.ship_position[horizontal_coordinate]
                        ai_guess_column = self.board.ship_position[vertical_coordinate] + 1
                elif self.board.orientation:  # Shoot at vertical ship
                    for item in self.board.ai_radar:
                        print(item[0], ' '.join(map(str, item[1:])))
                    if self.board.is_ocean(ai_guess_row + 1, ai_guess_column, self.board.ai_radar) and not self.board.miss:
                        ai_guess_row += 1
                    else:
                        # print("Adjusting guess to lower row number")
                        ai_guess_row -= 1

                        while not self.board.is_ocean(ai_guess_row, ai_guess_column, self.board.ai_radar):  # not is important here
                            ai_guess_row -= 1
                else:  # Shoot at horizontal ship
                    # print("Previous Guess: ", ai_guess_row, ":", ai_guess_col)
                    for item in self.board.ai_radar:
                        print(item[0], ' '.join(map(str, item[1:])))
                    if self.board.is_ocean(ai_guess_row, ai_guess_column - 1, self.board.ai_radar) and not self.board.miss:
                        ai_guess_column = ai_guess_column - 1
                    else:
                        # print("Adjusting guess to higher col number")
                        ai_guess_column = ai_guess_column + 1
                        while not self.board.is_ocean(ai_guess_row, ai_guess_column, self.board.ai_radar):
                            ai_guess_column += 1
                        # print("New Guess: ", ai_guess_row, ":", ai_guess_col)

                # Set boards after shots
                if not self.board.is_ocean(ai_guess_row, ai_guess_column, self.board.player_board):

                    # print("Setting Board: ", ai_guess_row, ":", ai_guess_col)
                    self.board.player_board[ai_guess_row][ai_guess_column] = self.board.hit
                    self.board.ai_radar[ai_guess_row][ai_guess_column] = self.board.hit
                    self.board.total_hits.append(self.board.number_board[ai_guess_row][ai_guess_column])
                    self.board.player_alive -= 1

                    # if second_shot: # set orientation
                    horizontal_coordinate = 0
                    vertical_coordinate = 1
                    two_hits_on_same_ship = 2
                    if (self.board.total_hits.count(self.board.total_hits[horizontal_coordinate]) == two_hits_on_same_ship
                            and self.board.ship_number(ai_guess_row, ai_guess_column) ==
                            self.board.ship_number(self.board.ship_position[horizontal_coordinate],
                                                   self.board.ship_position[vertical_coordinate])):
                        if ai_guess_column != self.board.ship_position[vertical_coordinate]:
                            orientation = 0
                        else:
                            orientation = 1
                        print("New Orientation: ", orientation)
                    elif self.board.total_hits[horizontal_coordinate] != self.board.number_board[ai_guess_row][ai_guess_column]:  # Other ship was shot
                        self.board.ship_length.append((self.board.ship_number(ai_guess_row, ai_guess_column)))
                        self.board.ship_position.extend([ai_guess_row, ai_guess_column])
                    if self.board.player_alive:
                        self.board.miss = 0
                        print("Attention Admiral! You have been hit!")
                    else:
                        print("I'm sorry sir, but we're going down")
                        self.board.print_board()
                        break
                else:  # AI missed
                    self.board.miss = 1
                    self.board.player_board[ai_guess_row][ai_guess_column] = self.board.fire
                    self.board.ai_radar[ai_guess_row][ai_guess_column] = self.board.fire
                    print("Good news! They've missed!")
                if self.board.ship_sunk():  # Reset variables
                    # print("Ship sunk")
                    zero = 0
                    self.board.orientation = -1
                    self.board.ship_position.pop(zero)
                    self.board.ship_position.pop(zero)
                    self.board.ship_length.pop(zero)

                    total_hits = self.board.total_hits[zero]
                    for x in range(self.board.total_hits.count(total_hits)):
                        self.board.total_hits.remove(total_hits)

                    if len(self.board.ship_length) != 0:
                        self.board.miss = 0
                    else:
                        self.board.miss = 1
            self.board.print_board()


if __name__ == "__main__":
    ui = UI()
    ui.start()
