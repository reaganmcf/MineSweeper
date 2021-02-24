"""
User Interface for the entire Game
"""

import pygame
from pygame.locals import QUIT
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT


def init_window():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('MineSweeper')


def event_handler(event):
    """
    Handle specific UI event
    """

    if event == QUIT:
        return
