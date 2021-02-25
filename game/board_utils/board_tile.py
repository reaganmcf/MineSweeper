from ..core.constants import TILES
import pygame
import os


class BoardTile:
    def __init__(self, tile: int, i: int, j: int):
        self._i = i
        self._j = j
        if tile not in TILES.get_list():
            raise ValueError("Argument 'tile = {}' is not valid. Must be either {}".format(
                tile, TILES.__tiles))

        self._tile = tile
        self._image = None

    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j

    @property
    def type(self) -> int:
        """
        Return the type of the tile, according to constants.TILES
        """
        return self._tile

    def set_type(self, new_type: TILES):
        """
        Set type of tile to a new tile.
        """
        self._tile = new_type

    def get_component(self, tile_width: int):
        """ 
        Create a PyGame Rectangle object of the given tile and return it to be rendered by the board
        """

        return pygame.Rect(self._i * tile_width, self._j * tile_width, tile_width, tile_width)
