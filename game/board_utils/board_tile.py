from ..core.constants import TILES, DEBUG__SHOW_TILES
import pygame
import os


class BoardTile:
    def __init__(self, tile: int, i: int, j: int):
        self._i = i
        self._j = j
        if tile not in TILES.get_list():
            raise ValueError("Argument 'tile = {}' is not valid. Must be either {}".format(
                tile, TILES.__tiles))
        self._is_open = False
        self._tile = TILES(tile)

    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j

    @property
    def type(self) -> TILES:
        """
        Return the type of the tile, according to constants.TILES
        """
        return self._tile

    @property
    def is_open(self) -> bool:
        """
        Return whether or not the tile has been opened
        """
        return self._opened
    
    def open(self):
        """
        Open a tile
        """
        self._is_open = True 

    def set_type(self, new_type: TILES):
        """
        Set type of tile to a new tile.
        """
        self._tile = new_type

    def get_component(self, tile_width: int) -> tuple:
        """ 
        Return a tuple (color, pygame.Rect, lineWidth) of the given tile and return it to be rendered by the board
        """
        color = '#ffffff'
        rect = pygame.Rect(self._i * tile_width, self._j * tile_width, tile_width, tile_width)
        width = 1

        if self._is_open or DEBUG__SHOW_TILES:
            if self._tile == TILES.MINE:
                color = 'red'
                width = 10
    
        return color, rect, width
