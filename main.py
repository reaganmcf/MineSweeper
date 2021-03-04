import sys
import argparse
import pygame
from threading import Thread

from pygame.locals import QUIT
from game.core.constants import DEFAULT_DIM, DEFAULT_BOMB_COUNT, GAME_STATE, WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT, EVENT_OPEN_TILE
from game.board_utils.board import Board
from game.core.agent import Agent
from game.ai_utils import ai, basic_agent

# Arguments
parser = argparse.ArgumentParser(description="Options")
# Add Arguments
parser.add_argument("--dim", help="dimension of the grid",
                    default=DEFAULT_DIM, type=int)
parser.add_argument(
    "--bomb_count", help="number of bombs to be placed randomly in the grid", default=DEFAULT_BOMB_COUNT, type=int)

parser.add_argument(
    "--agent", help="Which agent to use, either `basic` or `advanced`", type=str)

args = parser.parse_args()

# Game clock and event loop as well as game_state
clock = pygame.time.Clock()

# Initialize things and return a new instance of Board
def init():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('MineSweeper')

    # Calculate the width of a tile
    CELL_WIDTH = int((WINDOW_WIDTH) / args.dim)
    return Board(dim=args.dim, bomb_count=args.bomb_count, screen=screen, tile_width=CELL_WIDTH, game_state=GAME_STATE.RUNNING)

board = init()
agent = None
if args.agent == "basic":
    print("Using basic agent")
    agent = Agent(i=0, j=0, screen=board.screen, board=board)
elif args.agent == "advanced":
    print("Advanced Agent not yet supported")
else:
    print("Please pass in --agent flag")
    exit(1)

# debug flags
dbg_show_bombs = False

# Start AI Thread
basic_ai_thread = Thread(target = basic_agent.start, args=(board,agent))
basic_ai_thread.start()

while board.game_state != GAME_STATE.STOPPED:
    clock.tick(20)
    for event in pygame.event.get():
        # Close Window
        if event.type == QUIT:
            board.set_game_state(GAME_STATE.STOPPED)
            basic_ai_thread.join()
 
        # Custom Event Handlers from AI
        #elif event == EVENT_MOVE_UP:
        #    agent.move_up()
        #elif event == EVENT_MOVE_DOWN:
        #    agent.move_down()
        #elif event == EVENT_MOVE_LEFT:
        #    agent.move_left()
        #elif event == EVENT_MOVE_RIGHT:
        #    agent.move_right()
        #elif event == EVENT_OPEN_TILE:
        #    agent.open_tile()

        # Keyboard Press Events
        elif event.type == pygame.KEYDOWN:
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
            elif event.key == pygame.K_f:
                agent.flag_tile()

            # debug commands
            elif event.key == pygame.K_s: # show bombs while holding down
                dbg_show_bombs = True
            elif event.key == pygame.K_r: # reinitialize the board
                board.init_tiles()

        elif event.type == pygame.KEYUP:
            # turn off debug commands
            dbg_show_bombs = False
        
        # rendering stuff
        board.screen.fill(BACKGROUND_COLOR)
        board.draw(dbg_show_bombs = dbg_show_bombs)
        agent.draw()

    pygame.display.flip()
