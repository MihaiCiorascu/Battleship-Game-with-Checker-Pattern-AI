from game.game_logic import Game

import pygame


class GUI:
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Battleship")
    myfont = pygame.font.SysFont("fresansttf", 100)

    def __init__(self):
        self.game = None
        self.SQUARE_SIZE = 45
        self.HORIZONTAL_MARGIN = self.SQUARE_SIZE * 4
        self.VERTICAL_MARGIN = self.SQUARE_SIZE

        self.WIDTH = self.SQUARE_SIZE * 10 * 2 + self.HORIZONTAL_MARGIN
        self.HEIGHT = self.SQUARE_SIZE * 10 * 2 + self.VERTICAL_MARGIN
        self.INDENT = 10
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.HUMAN1 = True
        self.HUMAN2 = False

        # colors
        self.GREY = (40, 50, 60)
        self.WHITE = (255, 250, 250)
        self.GREEN = (50, 200, 150)
        self.RED = (250, 50, 100)
        self.BLUE = (0, 255, 255)
        self.ORANGE = (250, 140, 20)
        self.COLORS = {"U": self.GREY, "M": self.BLUE, "H": self.ORANGE, "S": self.RED}

    # function to draw a grid
    def draw_grid(self, player, left=0, top=0, search=False):
        for index in range(100):
            horizontal_index_grid = left + index % 10 * self.SQUARE_SIZE  # horizontal_index_grid = x in XoY Axis
            vertical_index_grid = top + index // 10 * self.SQUARE_SIZE  # vertical_index_grid = y in XoY Axis
            square = pygame.Rect(horizontal_index_grid, vertical_index_grid, self.SQUARE_SIZE, self.SQUARE_SIZE)
            pygame.draw.rect(self.SCREEN, self.WHITE, square, width=3)
            if search:
                horizontal_index_grid += self.SQUARE_SIZE // 2
                vertical_index_grid += self.SQUARE_SIZE // 2
                pygame.draw.circle(self.SCREEN, self.COLORS[player.search[index]],
                                   (horizontal_index_grid, vertical_index_grid),
                                   radius=self.SQUARE_SIZE // 4)

    # function to draw ships onto the position grids
    def draw_ships(self, player, left=0, top=0):
        for ship in player.ships:
            horizontal_index_ship = left + ship.column * self.SQUARE_SIZE + self.INDENT  # horizontal_index_ship = x in XoY Axis
            vertical_index_ship = top + ship.row * self.SQUARE_SIZE + self.INDENT  # horizontal_index_ship = x in XoY Axis
            if ship.orientation == 'horizontal':
                width = ship.size * self.SQUARE_SIZE - 2 * self.INDENT
                height = self.SQUARE_SIZE - 2 * self.INDENT
            else:
                width = self.SQUARE_SIZE - 2 * self.INDENT
                height = ship.size * self.SQUARE_SIZE - 2 * self.INDENT
            rectangle = pygame.Rect(horizontal_index_ship, vertical_index_ship, width, height)
            pygame.draw.rect(self.SCREEN, self.GREEN, rectangle, border_radius=15)

    def run(self):
        self.game = Game(self.HUMAN1, self.HUMAN2)

        # pygame loop
        animating = True
        pausing = False
        while animating:

            # track user interaction
            for event in pygame.event.get():

                # user closes the pygame window
                if event.type == pygame.QUIT:
                    animating = False

                # user clicks on mouse
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game.over:

                    # horizontal_index_mouse = x and vertical_index_mouse = y in XoY Axis
                    horizontal_index_mouse, vertical_index_mouse = pygame.mouse.get_pos()
                    if self.game.player1_turn and horizontal_index_mouse < self.SQUARE_SIZE * 10 and vertical_index_mouse < self.SQUARE_SIZE * 10:
                        row = vertical_index_mouse // self.SQUARE_SIZE
                        column = horizontal_index_mouse // self.SQUARE_SIZE
                        index = row * 10 + column
                        self.game.make_move(index)
                    elif (not self.game.player1_turn and horizontal_index_mouse > self.WIDTH - self.SQUARE_SIZE * 10 and
                          vertical_index_mouse > self.SQUARE_SIZE * 10 + self.VERTICAL_MARGIN):
                        row = (vertical_index_mouse - self.SQUARE_SIZE * 10 - self.VERTICAL_MARGIN) // self.SQUARE_SIZE
                        column = (horizontal_index_mouse - self.SQUARE_SIZE * 10 - self.HORIZONTAL_MARGIN) // self.SQUARE_SIZE
                        index = row * 10 + column
                        self.game.make_move(index)

                # user presses any key
                if event.type == pygame.KEYDOWN:

                    # escape key to close the animation
                    if event.key == pygame.K_ESCAPE:
                        animating = False

                    # space bar to pause and unpause the animation
                    if event.key == pygame.K_SPACE:
                        pausing = not pausing

                    # return key to restart the game
                    if event.key == pygame.K_RETURN:
                        self.game = Game(self.HUMAN1, self.HUMAN2)

            # execution
            if not pausing:
                # draw background
                self.SCREEN.fill(self.GREY)

                # draw search grids
                self.draw_grid(self.game.player1, search=True)
                self.draw_grid(self.game.player2, search=True,
                               left=(self.WIDTH - self.HORIZONTAL_MARGIN) // 2 + self.HORIZONTAL_MARGIN,
                               top=(self.HEIGHT - self.VERTICAL_MARGIN) // 2 + self.VERTICAL_MARGIN)

                # draw position grids
                self.draw_grid(self.game.player1, top=(self.HEIGHT - self.VERTICAL_MARGIN) // 2 + self.VERTICAL_MARGIN)
                self.draw_grid(self.game.player2,
                               left=(self.WIDTH - self.HORIZONTAL_MARGIN) // 2 + self.HORIZONTAL_MARGIN)

                # draw ships onto the position grids
                self.draw_ships(self.game.player1, top=(self.HEIGHT - self.VERTICAL_MARGIN) // 2 + self.VERTICAL_MARGIN)
                self.draw_ships(self.game.player2,
                                left=(self.WIDTH - self.HORIZONTAL_MARGIN) // 2 + self.HORIZONTAL_MARGIN)

                # computer moves
                if not self.game.over and self.game.computer_turn:
                    if self.game.player1_turn:
                        self.game.random_ai()
                        # self.game.basic.ai()
                    else:
                        self.game.basic_ai()

                # game over message
                if self.game.over:
                    text = "Player " + str(self.game.result) + " wins!"
                    textbox = self.myfont.render(text, False, self.GREY, self.WHITE)
                    self.SCREEN.blit(textbox, (self.WIDTH // 2 - 240, self.HEIGHT // 2 - 50))

                # update screen
                pygame.time.wait(200)
                pygame.display.flip()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
