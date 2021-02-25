import enum
import pygame
import os

# debug flags
DEBUG__SHOW_TILES = False # show tile states even when they are still closed



WINDOW_WIDTH, WINDOW_HEIGHT = (800, 800)
DEFAULT_DIM, DEFAULT_BOMB_COUNT = 10, 12


BACKGROUND_COLOR = pygame.Color(192, 192, 192)


# game states
class GAME_STATE(enum.Enum):
    RUNNING = 0
    WAITING_FOR_INPUT = 1
    STOPPED = 2


# assets
SPRITESHEET_PATH = os.path.join(os.path.dirname(__file__),
                                "../../assets/SpriteSheet.png")
SPRITESHEET_CELL_WIDTH = 32


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

    def get_sprite_coords_for_tile(tile):
        """
        Returns (x,y,width,height) for a given tile representing the sprite image location and width/height
        """

        if tile == TILES.MINE:
            return ((32, 0, 32, 32))  # MINE SPRITE
        else:
            return ((0, 0, 32, 32))  # NULL SPRITE
