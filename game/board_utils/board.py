from .board_tile import BoardTile
from ..core.constants import TILES
import pygame
import numpy as np


class Board:
    def __init__(self, dim: int, bomb_count: int, screen: any, tile_width: float):
        self._dim = dim
        self._bomb_count = bomb_count
        self._tiles = [[]]
        self._screen = screen
        self._tile_width = tile_width

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

        # place bombs randomly
        bombs_left = self._bomb_count
        while bombs_left > 0:
            rand_i, rand_j = np.random.randint(0, self._dim), np.random.randint(0, self._dim)
            if self._tiles[rand_i][rand_j].type == TILES.UNOPENED:
                self._tiles[rand_i][rand_j].set_type(TILES.MINE)
                bombs_left -= 1

    def open_tile(self, i: int, j: int):
        """
        Open (or interact with) a tile at a given index
        """
        self._tiles[i][j].open()

    def draw(self, dbg_show_bombs: bool = False):
        """
        Draw board state on pygame window
        """
        for tile_row in self._tiles:
            for tile in tile_row:
                color, rect, line_width, image = tile.get_component(self._tile_width, dbg_show_bombs=dbg_show_bombs)
                if image:
                    self._screen.blit(image, rect)
                else:
                    pygame.draw.rect(self._screen, color, rect, line_width)
