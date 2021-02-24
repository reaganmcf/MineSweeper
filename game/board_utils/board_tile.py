from typing import Union
from ..core.constants import TILES


class BoardTile:
    def __init__(self, tile: Union[str, int], i: int, j: int):
        self._i = i
        self._j = j
        if tile not in TILES.get_list():
            raise ValueError("Argument 'tile = {}' is not valid. Must be either {}".format(
                tile, TILES.__tiles))

        self._tile = tile

    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j

    @property
    def str(self) -> str:
        return str(self._tile)

    @property
    def val(self) -> int:
        return self._tile
