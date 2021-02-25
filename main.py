import sys
import argparse
import pygame
from pygame.locals import QUIT

from game.core.constants import DEFAULT_DIM, DEFAULT_BOMB_COUNT, GAME_STATE, WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR
from game.board_utils.board import Board
from game.core.agent import Agent


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
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('MineSweeper')

    # Calculate the width of a tile
    CELL_WIDTH = (WINDOW_WIDTH) / args.dim
    return Board(dim=args.dim, bomb_count=args.bomb_count, screen=screen, tile_width=CELL_WIDTH)


board = init()
agent = Agent(x=0, y=0, screen=board.screen, tile_width=board.tile_width)

# Game clock and event loop
clock = pygame.time.Clock()
game_state: GAME_STATE = GAME_STATE.RUNNING
while game_state != GAME_STATE.STOPPED:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            game_state = GAME_STATE.STOPPED

        board.screen.fill(BACKGROUND_COLOR)
        board.draw()
        agent.draw()

    pygame.display.flip()
