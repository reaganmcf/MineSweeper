from .board_tile import BoardTile
from ..core.constants import TILES, GAME_STATE
import pygame
import numpy as np


class Board:
    def __init__(self, dim: int, bomb_count: int, screen: any, tile_width: float, game_state: GAME_STATE):
        self._dim = dim
        self._bomb_count = bomb_count
        self._tiles = [[]]
        self._screen = screen
        self._tile_width = tile_width
        self._game_state = game_state
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

    @property
    def game_state(self):
        """
        Return the current game state
        """
        return self._game_state

    def set_game_state(self, new_game_state: GAME_STATE):
        """
        Set the game state
        """
        self._game_state = new_game_state

    def get_tile(self, i, j):
        """
        Get tile at given position
        """
        return self._tiles[i][j]

    def init_tiles(self):
        """
        Initialize a list of tiles
        """
        self._tiles = [
            [BoardTile(TILES.UNOPENED, i, j) for j in range(self._dim)]
            for i in range(self._dim)
        ]

        # place bombs randomly
        bombs_left = self._bomb_count
        while bombs_left > 0:
            rand_i, rand_j = np.random.randint(
                0, self._dim), np.random.randint(0, self._dim)
            if self._tiles[rand_i][rand_j].type == TILES.UNOPENED:
                self._tiles[rand_i][rand_j].set_type(TILES.MINE)
                bombs_left -= 1

    def open_tile(self, i: int, j: int):
        """
        Open (or interact with) a tile at a given index
        """

        # calculate the new tile type by checking adjacent neighbors
        if self._tiles[i][j].type != TILES.MINE:
            neighbors = self.get_neighboring_tiles(i, j)
            num_mines = 0
            for tile in neighbors:
                if tile.type == TILES.MINE:
                    num_mines += 1

            # update tile type
            self._tiles[i][j].set_type(TILES(num_mines))

        self._tiles[i][j].open()

    def get_score(self) -> int:
        score = 0
        for tilelist in self.tiles:
            for tile in tilelist:
                if tile.type == TILES.MINE and not tile.is_opened and tile.is_flagged:
                    score += 1
        return score

    def get_neighboring_tiles(self, i: int, j: int) -> list:
        """
        Return a list of all neighboring cells
        """
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []
        for dx, dy in dirs:
            nx, ny = i + dx, j + dy
            # check bounds
            if 0 <= nx and nx < self._dim and 0 <= ny and ny < self._dim:
                neighbors.append(self._tiles[nx][ny])

        return neighbors

    def flag_tile(self, i: int, j: int):
        """
        Toggle the flag status for a tile at a given index 
        """
        self._tiles[i][j].toggle_flag()

    def draw(self, dbg_show_bombs: bool = False):
        """
        Draw board state on pygame window
        """
        for tile_row in self._tiles:
            for tile in tile_row:
                color, rect, line_width, image = tile.get_component(
                    self._tile_width, dbg_show_bombs=dbg_show_bombs)
                if image:
                    self._screen.blit(image, rect)
                else:
                    pygame.draw.rect(self._screen, color, rect, line_width)
