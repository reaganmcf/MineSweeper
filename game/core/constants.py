import enum

WINDOW_WIDTH, WINDOW_HEIGHT = (800, 800)
DEFAULT_DIM, DEFAULT_BOMB_COUNT = 50, 12


# game states
class GAME_STATE(enum.Enum):
    RUNNING = 0
    WAITING_FOR_INPUT = 1
    STOPPED = 2


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

    def get_list() -> list:
        '''
        Returns board tiles as list, so you can check if they are one of the valid types above
        '''
        return [TILES.MINE, TILES.UNOPENED, TILES.ZERO, TILES.ONE, TILES.TWO, TILES.THREE, TILES.FOUR, TILES.FIVE, TILES.SIX, TILES.SEVEN, TILES.EIGHT]
