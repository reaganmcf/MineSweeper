from ..core.constants import TILES, DEBUG__SHOW_TILES, MINE_IMG, FLAG_IMG, ZERO_IMG, ONE_IMG, TWO_IMG, THREE_IMG, FOUR_IMG, FIVE_IMG, SIX_IMG, SEVEN_IMG, EIGHT_IMG, UNOPENED_IMG
import pygame
import os
from sympy import Symbol


class BoardTile:
    def __init__(self, tile: int, i: int, j: int):
        self._i = i
        self._j = j
        if tile not in TILES.get_list():
            raise ValueError("Argument 'tile = {}' is not valid. Must be either {}".format(
                tile, TILES.__tiles))
        self._is_open = False
        self._is_flagged = False
        self._tile = TILES(tile)

    def __str__(self):
        return str(self.i)+", " + str(self.j)

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
    def is_opened(self) -> bool:
        """
        Return whether or not the tile has been opened
        """
        return self._is_open

    @property
    def is_flagged(self) -> bool:
        """
        Return whether or not the tile has a flag on it
        """
        return self._is_flagged

    def open(self):
        """
        Open a tile
        """
        self._is_open = True

    def toggle_flag(self):
        """
        Toggle the flag status of a cell
        """
        self._is_flagged = not self._is_flagged

    def set_type(self, new_type: TILES):
        """
        Set type of tile to a new tile.
        """
        self._tile = new_type

    def get_symbol(self) -> Symbol:
        return Symbol('tile_{}_{}'.format(self.i, self.j))

    def get_component(self, tile_width: int, dbg_show_bombs: bool = False) -> tuple:
        """
        Return a tuple (color, pygame.Rect, lineWidth, image) of the given tile and return it to be rendered by the board
        """

        color = 'black'
        rect = pygame.Rect(self._j * tile_width, self._i *
                           tile_width, tile_width, tile_width)
        width = 1
        image = None

        if self._is_open or DEBUG__SHOW_TILES or dbg_show_bombs:
            # render mine on tile
            if self._tile == TILES.MINE:
                image = pygame.transform.scale(
                    MINE_IMG, (tile_width, tile_width))
            elif self._tile == TILES.ZERO:
                image = pygame.transform.scale(
                    ZERO_IMG, (tile_width, tile_width))
            elif self._tile == TILES.ONE:
                image = pygame.transform.scale(
                    ONE_IMG, (tile_width, tile_width))
            elif self._tile == TILES.TWO:
                image = pygame.transform.scale(
                    TWO_IMG, (tile_width, tile_width))
            elif self._tile == TILES.THREE:
                image = pygame.transform.scale(
                    THREE_IMG, (tile_width, tile_width))
            elif self._tile == TILES.FOUR:
                image = pygame.transform.scale(
                    FOUR_IMG, (tile_width, tile_width))
            elif self._tile == TILES.FIVE:
                image = pygame.transform.scale(
                    FIVE_IMG, (tile_width, tile_width))
            elif self._tile == TILES.SIX:
                image = pygame.transform.scale(
                    SIX_IMG, (tile_width, tile_width))
            elif self._tile == TILES.SEVEN:
                image = pygame.transform.scale(
                    SEVEN_IMG, (tile_width, tile_width))
            elif self._tile == TILES.EIGHT:
                image = pygame.transform.scale(
                    EIGHT_IMG, (tile_width, tile_width))
        # render flag on tile
        elif not self._is_open:
            if self._is_flagged:
                image = pygame.transform.scale(
                    FLAG_IMG, (tile_width, tile_width))
            else:
                image = pygame.transform.scale(
                    UNOPENED_IMG, (tile_width, tile_width))

        return color, rect, width, image
