import pygame
from ..core.constants import EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT
import time


def start():
    """
    Thread Loop for the AI
    """
    while(True):
        time.sleep(0.5)
        pygame.event.post(EVENT_MOVE_DOWN)
