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
def init():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('MineSweeper')

    # Calculate the width of a tile
    CELL_WIDTH = (WINDOW_WIDTH) / args.dim
    return Board(dim=args.dim, bomb_count=args.bomb_count, screen=screen, tile_width=CELL_WIDTH)


board = init()
agent = Agent(i=0, j=0, screen=board.screen, board=board)

# Game clock and event loop
clock = pygame.time.Clock()
game_state: GAME_STATE = GAME_STATE.RUNNING

# debug flags
dbg_show_bombs = False

while game_state != GAME_STATE.STOPPED:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:  # Close Window
            game_state = GAME_STATE.STOPPED
        elif event.type == pygame.KEYDOWN:  # Keyboard Presses
            if event.key == pygame.K_DOWN:
                agent.move_down()
            elif event.key == pygame.K_UP:
                agent.move_up()
            elif event.key == pygame.K_LEFT:
                agent.move_left()
            elif event.key == pygame.K_RIGHT:
                agent.move_right()
            elif event.key == pygame.K_RETURN:
                agent.open_tile()

            # debug commands
            elif event.key == pygame.K_s: # show bombs while holding down
                dbg_show_bombs = True

        elif event.type == pygame.KEYUP:
            # turn off debug commands
            dbg_show_bombs = False
        board.screen.fill(BACKGROUND_COLOR)
        board.draw(dbg_show_bombs = dbg_show_bombs)
        agent.draw()

    pygame.display.flip()
