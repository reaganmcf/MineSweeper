import pygame
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Agent:
    def __init__(self, x: int, y: int,  screen: any, tile_width: int, ):
        self._screen = screen
        self._x = x
        self._y = y

        # tile width is passed in so we know how large to make the agent
        self._tile_width = tile_width

    """
    BEGIN AI SPECIFIC FUNCTIONS

    The AI should ONLY be interacting with the following functions
    """

    def moveUp(self):
        # Make sure we don't go off screen
        self._y = max(0, self._y - self._tile_width)

    def moveDown(self):
        # Make sure we don't go off screen
        self._y = min(WINDOW_HEIGHT - self._tile_width,
                      self._y + self._tile_width)

    def moveLeft(self):
        # Make sure we don't go off screen
        self._x = max(0, self._x - self._tile_width)

    def moveRight(self):
        # Make sure we don't go off screen
        self._x = min(WINDOW_WIDTH - self._tile_width,
                      self._x + self._tile_width)

    """
    END AI SPECIFIC FUNCTIONS
    """

    @property
    def x_pixel(self):
        """
        Returns x PIXEL position of the agent
        """
        return self._x

    @property
    def y_pixel(self):
        """
        Returns y PIXEL position of the agent
        """
        return self._y

    @property
    def screen(self):
        """
        Return pygame screen instance
        """
        return self._screen

    def set_x(self, new_x: int):
        """
        Set x position of the agent
        """
        self._x = new_x

    def set_y(self, new_y: int):
        """
        Set y position of the agent
        """
        self._y = new_y

    def draw(self):
        """
        Returns pygame rect to draw on the screen
        """
        # Agent is 80% the size of a tile
        agent_width = self._tile_width * 0.8
        # Create agent rectangle (can use sprites later)
        rect = pygame.Rect(self._x, self._y, agent_width, agent_width)
        # Center (inplace) the agent rectangle
        rect.move_ip(self._tile_width * 0.1, self._tile_width * .1)
        # Draw the agent
        pygame.draw.rect(self._screen, '#000000', rect, 5)
