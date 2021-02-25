from .board_tile import BoardTile
from ..core.constants import TILES, SPRITESHEET_PATH
from .sprite_sheet import SpriteSheet
import pygame


class Board:
    def __init__(self, dim: int, bomb_count: int, screen: any, tile_width: float):
        self._dim = dim
        self._bomb_count = bomb_count
        self._tiles = [[]]
        self._screen = screen
        self._tile_width = tile_width

        # init sprite sheet
        self._spritesheet = SpriteSheet(SPRITESHEET_PATH)

        self.init_tiles()

    @property
    def dim(self):
        """
        Return the dimension of the board
        """
        return self._dim

    @property
    def bomb_count(self):
        """
        Return the total number of bombs on the board (NOT REMAINING!!)
        """
        return self._bomb_count

    @property
    def tiles(self):
        """
        Return 2d list of BoardTile instances
        """
        return self._tiles

    @property
    def screen(self):
        """
        Return pygame screen instance
        """
        return self._screen

    @property
    def tile_width(self):
        """
        Return the width of a tile for the board (precalculated on initialization)
        """
        return self._tile_width

    def init_tiles(self):
        """
        Initialize a list of tiles
        """
        self._tiles = [
            [BoardTile(TILES.UNOPENED, i, j) for i in range(self._dim)]
            for j in range(self._dim)
        ]

    def draw(self):
        """
        Draw board state on pygame window
        """
        for tile_row in self._tiles:
            for tile in tile_row:
                pygame.draw.rect(self._screen, '#ffffff',
                                 tile.get_component(self._tile_width), 1)
