import sys
import argparse
import pygame
from threading import Thread

from pygame.locals import QUIT
from game.core.constants import DEFAULT_DIM, DEFAULT_BOMB_COUNT, GAME_STATE, WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR
from game.board_utils.board import Board
from game.core.agent import Agent
from game.ai_utils import advanced_agent, basic_agent, bonus_1_agent, hyper_advanced_agent, bonus_2_agent
from game.boolean_reference import BooleanReference

# Arguments
parser = argparse.ArgumentParser(description="Options")
# Add Arguments
parser.add_argument("--dim", help="dimension of the grid",
                    default=DEFAULT_DIM, required=True, type=int)
parser.add_argument(
    "--bomb_count", help="number of bombs to be placed randomly in the grid", required=True, default=DEFAULT_BOMB_COUNT, type=int)

parser.add_argument(
    "--agent", help="Which agent to use", required=True, choices=["basic", "advanced", "hyper_advanced", "bonus_1", "bonus_2", "none"], type=str)

parser.add_argument(
    "--use_stepping", help="DEBUG: Wait for keypress between agent events?", type=bool, default=False)

parser.add_argument(
    "--quit_when_finished", help="Quit when finished. Useful when averaging multiple scores.", type=bool, default=False)

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
agent = Agent(i=0, j=0, screen=board.screen, board=board)

# debug flags
dbg_show_bombs = False
# boolean reference for stepping debug feature
use_stepping = args.use_stepping
lock_boolean = BooleanReference(args.use_stepping)

# Start AI Thread
basic_ai_thread = None
advanced_ai_thread = None
hyper_advanced_ai_thread = None
if args.agent == "basic":
    print("Using AI agent - manual mode disabled")
    basic_ai_thread = Thread(target=basic_agent.start, args=(
        board, agent, use_stepping, lock_boolean))
    basic_ai_thread.start()
elif args.agent == "advanced":
    print("Using Advanced AI agent - manual mode disabled")
    advanced_ai_thread = Thread(
        target=advanced_agent.start, args=(board, agent, use_stepping, lock_boolean))
    advanced_ai_thread.start()
elif args.agent == "hyper_advanced":
    print("Using Hyper Advanced AI agent - manual mode disabled")
    hyper_advanced_ai_thread = Thread(
        target=hyper_advanced_agent.start, args=(board, agent, use_stepping, lock_boolean))
    hyper_advanced_ai_thread.start()
elif args.agent == "bonus_1":
    print("Using Bonus 1 Advanced AI agent - manual mode disabled")
    bonus_1_ai_thread = Thread(
        target=bonus_1_agent.start, args=(board, agent, use_stepping, lock_boolean))
    bonus_1_ai_thread.start()
elif args.agent == "bonus_2":
    print("Using Bonus 2 Advanced AI agent - manual mode disabled")
    bonus_2_ai_thread = Thread(
        target=bonus_2_agent.start, args=(board, agent, use_stepping, lock_boolean))
    bonus_2_ai_thread.start()
elif args.agent == "none":
    print("No agent being used - manual mode enabled")
else:
    print("No valid agent specified - refer to --help flag for more info")
    exit(0)

while board.game_state != GAME_STATE.STOPPED:
    clock.tick(20)
    for event in pygame.event.get():
        # Close Window
        if event.type == QUIT:
            board.set_game_state(GAME_STATE.STOPPED)
            if basic_ai_thread != None:
                basic_ai_thread.join()
            if advanced_ai_thread != None:
                advanced_ai_thread.join()
            if hyper_advanced_ai_thread != None:
                hyper_advanced_ai_thread.join()

        # there are 2 userevents that get sent - 1 is a re-render event
        # and the other is the game score event after the agent is finished
        elif event.type == pygame.USEREVENT and not hasattr(event, "render"):
            print(
                f"agent = {args.agent}, dim = {args.dim}, bomb_count = {args.bomb_count}, score = {event.score}")
            if args.quit_when_finished:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Keyboard Press Events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                # allow step forward
                lock_boolean.set(False)

            # manual mode is only enabled if agent is "none"
            if args.agent == 'none':
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
            elif event.key == pygame.K_s:  # show bombs while holding down
                dbg_show_bombs = True
            elif event.key == pygame.K_r:  # reinitialize the board
                board.init_tiles()

        elif event.type == pygame.KEYUP:
            # turn off debug commands
            dbg_show_bombs = False

        # rendering stuff
        board.screen.fill(BACKGROUND_COLOR)
        board.draw(dbg_show_bombs=dbg_show_bombs)
        agent.draw()

    pygame.display.flip()
