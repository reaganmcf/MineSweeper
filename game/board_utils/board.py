from .board_tile import BoardTile
from ..core.constants import TILES
import pygame


class Board:
    def __init__(self, dim: int, bomb_count: int, screen):
        self._dim = dim
        self._bomb_count = bomb_count
        self._tiles = [[]]
        self._screen = screen

        self.init_tiles()

    @property
    def dim(self) -> int:
        """
        Return the dimension of the board
        """
        return self._dim

    @property
    def bomb_count(self) -> int:
        """
        Return the total number of bombs on the board (NOT REMAINING!!)
        """
        return self._bomb_count

    @property
    def tiles(self) -> list:
        """
        Returns 2d list of BoardTile instances
        """
        return self._tiles

    @property
    def screen(self):
        """
        Returns pygame screen instance
        """
        return self._screen

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
        rect = pygame.Rect(50, 50, 50, 50)
        pygame.draw.rect(self._screen, '#ffffff', rect, 1)
