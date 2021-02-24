import sys
import argparse
import pygame
from pygame.locals import QUIT

from game.core.constants import DEFAULT_DIM, DEFAULT_BOMB_COUNT, GAME_STATE
from game.board_utils.board import Board
from game.core import agent, ui


# Arguments
parser = argparse.ArgumentParser(description="Options")
# Add Arguments
parser.add_argument("dim", help="dimension of the grid",
                    default=DEFAULT_DIM, type=int)
parser.add_argument(
    "bomb_count", help="number of bombs to be placed randomly in the grid", default=DEFAULT_BOMB_COUNT, type=int)

args = parser.parse_args()


# Initialize things and return a new instance of Board
def init() -> Board:
    screen = ui.init_window()
    return Board(dim=args.dim, bomb_count=args.bomb_count, screen=screen)


board = init()

# Game clock and event loop
clock = pygame.time.Clock()
game_state: GAME_STATE = GAME_STATE.RUNNING
while game_state != GAME_STATE.STOPPED:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            game_state = GAME_STATE.STOPPED
        board.draw()

    pygame.display.flip()
