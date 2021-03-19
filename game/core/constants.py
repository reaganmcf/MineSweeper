import enum
import pygame
import os

# debug flags
# these are different than the debugging commands, which are basically toggling these features
DEBUG__SHOW_TILES = False  # show tile states even when they are still closed


WINDOW_WIDTH, WINDOW_HEIGHT = (800, 800)
DEFAULT_DIM, DEFAULT_BOMB_COUNT = 10, 12
BACKGROUND_COLOR = pygame.Color(29, 31, 33)

# game states
class GAME_STATE(enum.Enum):
    RUNNING = 0
    WAITING_FOR_INPUT = 1
    STOPPED = 2


# assets
MINE_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/bomb.png"))
FLAG_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/flag.png"))
UNOPENED_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/unopened.png"))
ZERO_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/zero.png"))
ONE_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/one.png"))
TWO_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/two.png"))
THREE_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/three.png"))
FOUR_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/four.png"))
FIVE_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/five.png"))
SIX_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/six.png"))
SEVEN_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/seven.png"))
EIGHT_IMG = pygame.image.load(os.path.join(
    os.path.dirname(__file__), "../../assets/eight.png"))


# board tiles
class TILES(enum.Enum):
    MINE = -2
    UNOPENED = -1
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

    def get_list():
        """
        Returns board tiles as list, so you can check if they are one of the valid types above
        """
        return [TILES.MINE, TILES.UNOPENED, TILES.ZERO, TILES.ONE, TILES.TWO, TILES.THREE, TILES.FOUR, TILES.FIVE, TILES.SIX, TILES.SEVEN, TILES.EIGHT]
