import pygame
from ..core.constants import GAME_STATE, EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT, EVENT_OPEN_TILE
from ..board_utils.board import Board
import time


def start(board: Board):
    """
    Thread Loop for the AI
    """
    while board.game_state != GAME_STATE.STOPPED:
        time.sleep(0.5)
        pygame.event.post(EVENT_MOVE_DOWN)
