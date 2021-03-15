import pygame
import numpy as np
from sympy import Symbol, linsolve, linear_eq_to_matrix, solveset, FiniteSet, Eq, S, symbols, simplify, solve, And, satisfiable, Or
from ..core.constants import GAME_STATE, EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT, EVENT_OPEN_TILE, TILES
from ..board_utils.board import Board
from ..core.agent import Agent
import time
import random
from ..board_utils.board_tile import BoardTile
from constants import TILES

"""
Types of Operations:
    - 
"""

"""
Knowledge Base:
    knowledge_base = {
        x: [(x+y+z, 1)],
        y: [(x+y+z, 1)],
        z: [(x+y+z, 1)]
    }
    keys are symbols, values are a list of tuples (lhs = sympy equation, rhs = integer)
"""



def start(board: Board, agent: Agent):
    """
    Start the advanced agent
    """

    # first tile we look at is the agent's starting position
    start_tile = board.get_tile(agent.i, agent.j)

    # is the agent finished traversing (i.e. no more moves left)
    agent_done = False

    # generate symbols
    gen_symbols(board)
    

    # number of tiles flagged
    score = 0

    # stores safe tiles that we want to open (holds tile objects)
    tiles_to_open = [start_tile]  # start at the agent starting position

    # store visited tiles that we are not done with, tiles who still has unflagged/unopened neighbors (holds tile objects)
    unfinished_tiles = []

    while(not agent_done):
        time.sleep(0.01)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, attr1="force rerender"))


        if not tiles_to_open: #if the list to open new tiles is empty, then we must choose a new tile to get more information
            #TODO inference method
            
            random_tile = random_tile_to_open(board)
            
            #ends the game, no tiles remaining to open
            if not random_tile:
                print("GAME OVER, SCORE = ", score)
                #pygame.event.post(pygame.event.Event(pygame.QUIT, attr1={"Score": score})) #THIS CLOSES THE SCREEN TOO FAST
                return score
            tiles_to_open.append(random_tile)
        
        curr_tile = tiles_to_open.pop(0)

        i,j = curr_tile.i, curr_tile.j

        # update agent position
        agent.set_pos(i,j)

        # if the tile is unopened, we know (besides the very first) that it is safe
        if curr_tile.is_opened == False:
            board.open_tile(i,j)
            # we have to reassign curr_tile since the status has changed
            curr_tile = agent.get_tile()
        
        # now, check if we accidentally opened a mine
        if curr_tile.type == TILES.MINE:
            continue
        
        score = check_neighbors(curr_tile, board, unfinished_tiles, tiles_to_open, score)

        for i in range(len(unfinished_tiles)): #since we add elements back into the queue, we only want to iterate a specific amount of times
            tile = unfinished_tiles.pop(0) # we want to remove the top element from the queue
            score = check_neighbors(tile, board, unfinished_tiles, tiles_to_open, score)


def inference(board:Board, unfinished_tiles):
    # initialize KB with all tiles as keys
    knowledge_base = {tile : [] for tilelist in board.tiles for tile in tilelist}
    all_equations = []
    
    # look at each tile
    for tilelist in board.tiles:
        for tile in tilelist:

            # if the tile is not opened or is opened and a mine, we cant get any info
            if not tile.is_opened: 
                continue
            if tile.type == TILES.MINE:
                continue
            
            unopened_neighbors = [tile for tile in neighbors if not tile.is_opened and not tile.is_flagged]
            # since we only call this method when we have no more information we can collect using
            # the basic agent, unopened_neighbors should never have a length of 0.
            # But, just in case we assert
            assert len(unopened_neighbors) != 0 
            
            val = tile.type.value 

            # create the equation for the tile and value
            eqn = unopened_neighbors[0].get_symbol
            for i in range(1, len(unopened_neighbors)):
                eqn = eqn + unopened_neighbors[i].get_symbol
            
            index = len(all_equations)
            all_equations.append(eqn)

            # KB maps each variable in the equation to every equation it is present in
            for neighbors in unopened_neighbors:
                knowledge_base[neighbors.get_symbol].append([all_equations[index], val])

def random_tile_to_open(board: Board) -> BoardTile:
    """
    Pick a random tile to restart at by looking at board and choosing which 
    """
    available_tiles = []
    for tilelist in board.tiles:
        for tile in tilelist:
            if not tile.is_opened and not tile.is_flagged:
                available_tiles.append(tile)
    if not available_tiles:
        return
    # print(len(available_tiles))
    print("OPENING RANDOM TILE")
    rand = random.randint(0, len(available_tiles)-1)
    random_tile = available_tiles[rand]

    return random_tile

def check_neighbors(curr_tile: BoardTile, board: Board, unfinished_tiles: list, tiles_to_open: list, score: int):
    """
    looks at all neighbors for the current tiles, if it satisfies requirements, 
    it will either flag the neighboring tiles or add them to the tiles_to_open list
    returns the score (if we flag tiles, we want to increment score)
    """
    i, j = curr_tile.i, curr_tile.j
    # go over all neighboring cells
    neighbors = board.get_neighboring_tiles(i, j)
    unopened_neighbors = [
        tile for tile in neighbors if not tile.is_opened and not tile.is_flagged]
    mine_flagged_neighbors = [tile for tile in neighbors if tile.is_flagged or (
        tile.is_opened and tile.type == TILES.MINE)]

    total_neighbors = len(neighbors)
    total_unopened_neighbors = len(unopened_neighbors)
    total_mine_flagged_neighbors = len(mine_flagged_neighbors)

    clue = curr_tile.type.value

    # if we found all mines that are neighbors then the rest of the unopened neighbors are safe
    if total_mine_flagged_neighbors == clue:
        for tile in unopened_neighbors:
            if tile not in tiles_to_open:
                tiles_to_open.append(tile)
    # if the number of unopened neighbors equals the clue minus already flagged then all neighbors are mines
    elif total_unopened_neighbors == clue - total_mine_flagged_neighbors:
        for tile in unopened_neighbors:
            if not tile.is_flagged:
                tile.toggle_flag()
                print("FLAGGED TILE")
                print(tile.i, tile.j)
                score += 1
                print("Score = ", score)
    elif total_unopened_neighbors != 0:  # if the current tile still has unopened tiles, then we are not done with it
        unfinished_tiles.append(curr_tile)
    return score