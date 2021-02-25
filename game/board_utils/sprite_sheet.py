import pygame
from ..core.constants import TILES


class SpriteSheet:
    """
    SpriteSheet to handle game assets

    NOT BEING USED YET 
    """

    def __init__(self, filename):
        """
        Load SpriteSheet
        """
        try:
            self._sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle: tuple):
        """
        Load specific image from a specific rectangle in the SpriteSheet
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self._sheet, (0, 0), rect)
        return image

    def get_tile_image(self, tile: TILES):
        """
        Return tile's corresponding spriteimage
        """
        return self.image_at(TILES.get_sprite_coords_for_tile(tile))
