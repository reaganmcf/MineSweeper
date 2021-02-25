import pygame


class Agent:
    def __init__(self, x: int, y: int,  screen: any, tile_width: int, ):
        self._screen = screen
        self._x = x
        self._y = y

        # tile width is passed in so we know how large to make the agent
        self._tile_width = tile_width

    @property
    def x(self):
        """
        Returns x position of the agent
        """
        return self._x

    @property
    def y(self):
        """
        Returns y position of the agent
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
