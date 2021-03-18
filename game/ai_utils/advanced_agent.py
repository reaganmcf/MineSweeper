import pygame
import numpy as np
from sympy import Symbol, linsolve, linear_eq_to_matrix, solveset, FiniteSet, Eq, S, symbols, simplify, solve, And, satisfiable, Or
from ..core.constants import GAME_STATE, EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT, EVENT_OPEN_TILE, TILES
from ..board_utils.board import Board
from ..core.agent import Agent
import time
import random
from ..board_utils.board_tile import BoardTile
from ..core.constants import TILES

"""
Types of Operations:
    - we will first conduct subset reduction 
    - 
"""

"""
Knowledge Base:
    is a list of all equations:
        equations are a list where [0] = LHS, [1] = RHS
"""
SYMBOL_TO_TILE = dict()


def start(board: Board, agent: Agent):
    """
    Start the advanced agent
    """
    gen_symbol_to_tile(board)

    # first tile we look at is the agent's starting position
    start_tile = board.get_tile(agent.i, agent.j)

    # is the agent finished traversing (i.e. no more moves left)
    agent_done = False

    # number of tiles flagged
    score = 0

    # stores safe tiles that we want to open (holds tile objects)
    tiles_to_open = [start_tile]  # start at the agent starting position

    # store visited tiles that we are not done with, tiles who still has unflagged/unopened neighbors (holds tile objects)
    unfinished_tiles = []

    while(not agent_done):
        time.sleep(5)
        pygame.event.post(pygame.event.Event(
            pygame.USEREVENT, attr1="force rerender"))

        if not tiles_to_open:  # if the list to open new tiles is empty, then we must choose a new tile to get more information
            information_learned = inference(
                board=board, unfinished_tiles=unfinished_tiles, tiles_to_open=tiles_to_open, score=score)
            if information_learned:
                print("infrence worked")
            if not information_learned:
                print("infrence failed")
                random_tile = random_tile_to_open(board)
                # ends the game, no tiles remaining to open
                if not random_tile:
                    print("GAME OVER, SCORE = ", score)
                    # pygame.event.post(pygame.event.Event(pygame.QUIT, attr1={"Score": score})) #THIS CLOSES THE SCREEN TOO FAST
                    return score
                tiles_to_open.append(random_tile)

        if tiles_to_open:  # if we found a tile to open, we may have just flagged tiles in our inference methods
            curr_tile = tiles_to_open.pop(0)
            i, j = curr_tile.i, curr_tile.j

            # update agent position
            agent.set_pos(i, j)
            # if the tile is unopened, we know (besides the very first) that it is safe
            if curr_tile.is_opened == False:
                board.open_tile(i, j)
                # we have to reassign curr_tile since the status has changed
                curr_tile = agent.get_tile()

            # now, check if we accidentally opened a mine
            if curr_tile.type == TILES.MINE:
                continue

            score = check_neighbors(
                curr_tile, board, unfinished_tiles, tiles_to_open, score)

        # since we add elements back into the queue, we only want to iterate a specific amount of times
        for i in range(len(unfinished_tiles)):
            # we want to remove the top element from the queue
            tile = unfinished_tiles.pop(0)
            score = check_neighbors(
                tile, board, unfinished_tiles, tiles_to_open, score)


def gen_symbol_to_tile(board: Board):
    for tilelist in board.tiles:
        for tile in tilelist:
            SYMBOL_TO_TILE[tile.get_symbol()] = tile


def build_knowledge_base(board: Board, unfinished_tiles: list) -> list:
    # initialize KB with all tiles as keys
    # knowledge_base = {tile : [] for tilelist in board.tiles for tile in tilelist}
    all_equations = []

    # since we are looking at uninished tiles, we know that they are open and they have unopened neighbors, we also know they are not mines
    for tile in unfinished_tiles:
        neighbors = board.get_neighboring_tiles(tile.i, tile.j)
        unopened_neighbors = [
            tile for tile in neighbors if not tile.is_opened and not tile.is_flagged]
        mine_flagged_neighbors = [tile for tile in neighbors if tile.is_flagged or (
            tile.is_opened and tile.type == TILES.MINE)]

        # since we only call this method when we have no more information we can collect using
        # the basic agent, unopened_neighbors should never have a length of 0.
        # But, just in case we assert
        assert len(unopened_neighbors) != 0

        val = tile.type.value - len(mine_flagged_neighbors)

        # create the equation for the tile and value
        eqn = unopened_neighbors[0].get_symbol()
        for i in range(1, len(unopened_neighbors)):
            # print(eqn)
            # print(unopened_neighbors[i].get_symbol())
            eqn = eqn + unopened_neighbors[i].get_symbol()

        all_equations.append([eqn, val])
        # KB maps each variable in the equation to every equation it is present in
        # index = len(all_equations)-1
        # for neighbors in unopened_neighbors:
        #     knowledge_base[neighbors.get_symbol].append(all_equations[index])
    # sort the equations by size so when we do subset reduction, we do not miss anything
    all_equations = sorted(all_equations, key=lambda x: len(x[0].free_symbols))
    all_equations.reverse()

    return all_equations


def inference(board: Board, unfinished_tiles: list, tiles_to_open: list, score: int):
    all_equations = build_knowledge_base(
        board=board, unfinished_tiles=unfinished_tiles)
    print("kb built")
    for eq in all_equations:
        print(eq)
    new_info_learned = False
    subset_reduction(all_equations=all_equations, tiles_to_open=tiles_to_open)
    print("subset reduced")
    new_info_learned = simplify_known_equations(all_equations=all_equations,
                                                tiles_to_open=tiles_to_open, score=score)
    print("simplify 1")
    if new_info_learned:  # early termination, dont waste time on unnessary inferences that can be easily found a few steps down the line
        return True
    new_info_learned = double_inference(
        all_equations=all_equations, tiles_to_open=tiles_to_open, score=score)
    print("double inference")
    if new_info_learned:
        return True
    new_info_learned = simplify_known_equations(all_equations=all_equations,
                                                tiles_to_open=tiles_to_open, score=score)
    print("simplify 2")
    if new_info_learned:
        return True
    # we can add constraint satisfaction here
    return False


def simplify_known_equations(all_equations: list, tiles_to_open: list, score: int) -> bool:
    '''
    Simplifies the equation so that if we know all vars =0 or all vars=1 we can replace all vals and simplify other eqs as well
    '''
    # if we made any changes anecho $td need to check for more potential simplification, set check_again to true
    check_again = True
    new_info_learned = False

    # while more simplification is possible
    while check_again:
        check_again = False
        for i in range(len(all_equations)):
            if all_equations[i][1] == 0:
                check_again = True
                new_info_learned = True
                # all variables left in equation equate to 0
                for var in all_equations[i][0].free_symbols:
                    # add the var to tiles to open
                    tiles_to_open.append(SYMBOL_TO_TILE[var])
                    # replace the var in all equations
                    replace_value_in_all_eq(all_equations, var, 0)
                    # changes were made so need to check again
            if all_equations[i][1] == len(all_equations[i][0].free_symbols):
                check_again = True
                new_info_learned = True
                # all variable left in equation equate to 1
                for var in all_equations[i][0].free_symbols:
                    if not SYMBOL_TO_TILE[var].is_flagged:
                        # flag the var as bomb
                        SYMBOL_TO_TILE[var].toggle_flag
                        score += 1
                        # replace the var in all equations
                        replace_value_in_all_eq(all_equations, var, 1)
                        # changes were made so need to check again
    return new_info_learned


def replace_value_in_all_eq(all_equations: list, var: Symbol, val: int):
    '''
    Removes all instances of the variables in the list of equations and updates the value of the equation accordingly 
    '''
    for i in range(len(all_equations)):
        # if the var is in equation i
        if var in all_equations[i][0].free_symbols:
            # remove the var from the LHS
            all_equations[i][0] = all_equations[i][0] - var
            # subtract val from the RHS
            all_equations[i][1] = all_equations[i][1] - val


def subset_reduction(all_equations: list, tiles_to_open: list):
    '''
    Reduces redundancies in equations
    i.e.
    A+C+D+E = 2
    A+D = 1
    Then we can reduce A+C+D+E = 2 into C+E = 1 when we invoke simplify known equations
    '''
    for i in range(len(all_equations)):
        for j in range(i+1, len(all_equations)):
            eq1 = all_equations[i][0]
            eq2 = all_equations[j][0]
            set1 = eq1.free_symbols
            set2 = eq2.free_symbols
            if set1.issubset(set2):
                # eq2 is a superset of eq1 so we can reduce eq2
                all_equations[j][0] = eq2 - eq1
                # update value of equation
                all_equations[j][1] = all_equations[j][1] - all_equations[i][1]
            elif set2.issubset(set1):
                # eq1-eq2
                all_equations[i][0] = eq1 - eq2
                all_equations[i][1] = all_equations[i][1] - all_equations[j][1]


def double_inference(all_equations: list, tiles_to_open: list, score: int):
    '''
    looks at 2 equations and if they share the some of the same variables, we may be able to infer more info
    eq1 = A+B+C+D =2
    eq2 = B+D+E= 1
    eq1-eq2 = A+C - E = 1, then we can infer that E=0, then we can also infer A+C=1, B+D = 1 (Using subset reduction)
    '''
    new_information_learned = False

    for i in range(len(all_equations)):
        for j in range(i+1, len(all_equations)):
            eq1 = all_equations[i][0]
            eq2 = all_equations[j][0]
            set1 = eq1.free_symbols
            set2 = eq2.free_symbols
            # if they dont share any of the same variables cant get any new info
            if set1.isdisjoint(set2):
                continue
            # subtract the equation with a higher value from the other equation
            if all_equations[i][1] > all_equations[j][1]:
                derived_eq = eq1-eq2
                derived_val = all_equations[i][1] - all_equations[j][1]
            else:
                derived_eq = eq2 - eq1
                derived_val = all_equations[j][1] - all_equations[i][1]

            # TODO FIGURE OUT WHAT WE NEED TO DO AFTER WE SUBTRACT 2 EQS
                # if we just look at the value of the derived equation and the number of positive symbols
                # if they are equal then we know that all are equal to 1 and if we

            vars = derived_eq.free_symbols  # look at all symbols in derived eq
            positive_vars = []
            negative_vars = []
            for var in vars:
                # args for a+b+c-d-e will be (a,b,c, -d,-e), so if the free_symbol is in args, then it will be positive
                if var in derived_eq.args:
                    positive_vars.append(var)
                else:
                    negative_vars.append(var)

            # then we know all symbols being added are 1 and all symbols being subtracted are = 0
            if len(positive_vars) == derived_val:
                new_information_learned = True
                for var in positive_vars:
                    if not SYMBOL_TO_TILE[var].is_flagged:
                        SYMBOL_TO_TILE.toggle_flag
                        score += 1
                    replace_value_in_all_eq(all_equations, var, 1)
                for var in negative_vars:
                    tiles_to_open.append(SYMBOL_TO_TILE[var])
                    replace_value_in_all_eq(all_equations, var, 0)
    return new_information_learned


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
