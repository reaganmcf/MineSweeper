#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from ..core.constants import GAME_STATE, EVENT_MOVE_UP, EVENT_MOVE_DOWN, EVENT_MOVE_LEFT, EVENT_MOVE_RIGHT, EVENT_OPEN_TILE, TILES
from ..board_utils.board import Board
from ..core.agent import Agent
import time

"""
Note: agent should not be interacted with, instead use game events
"""

def start(board: Board, agent: Agent):
    """
    Start the basic agent
    """


   

    agent_start = (agent.i, agent.j)
    
    # is the agent finished traversing (i.e. no more moves left)
    agent_done = False

    # number of tiles flagged
    score = 0
    
    # start at agent start
    next_tiles = [agent_start]

    while(not agent_done):
        time.sleep(3)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, attr1="force rerender"))
        #if len(next_tiles) == 0:
         #   next_tiles.append(agent_start)
        
        # pop tile off queue
        i,j = next_tiles.pop(0)
        
        #DEBUG
        
        # update agent position
        agent.set_pos(i,j)
        print("agent postion: " , str(agent.i), str(agent.j))

        # check if tile has been opened
        curr_tile = agent.get_tile()
        print("tile position", str(curr_tile._i), str(curr_tile._j))
        print(curr_tile.type)

        # if the tile is unopened, we know (besides the very first) that it is safe
        if curr_tile.is_opened == False:
            print("Opening tile")
            agent.open_tile()
            # we have to reassign curr_tile since the status has changed
            curr_tile = agent.get_tile()
        
        # now, check if we accidentally opened mine
        if curr_tile.type == TILES.MINE:
            curr_tile.toggle_flag()
            continue
        
        # go over all neighboring cells
        neighbors = board.get_neighboring_tiles(i,j)
        unopened_neighbors = [tile for tile in neighbors if tile.type == TILES.UNOPENED and not tile.is_flagged]
        
        total_neighbors = len(neighbors)
        total_unopened_neighbors = len(unopened_neighbors)
        
        print("total_neighbors = " + str(total_neighbors))
        print("total_unopened_neighbors = " + str(total_unopened_neighbors))

        # value of the current cell (0-8)
        clue = curr_tile.type.value

        #something wrong here

        if clue == total_unopened_neighbors:
            # all unopened neighbors are mines, so flag them (and add to our score :) )
            for tile in unopened_neighbors:
                tile.toggle_flag()
                score += 1
        elif total_neighbors - clue >= total_unopened_neighbors:
            # add all unopened neighbors into the queue
            for tile in neighbors:
                next_tiles.append((tile.i, tile.j))
        elif total_unopened_neighbors == 0:
            # no more information to get from this tile
            continue
        else:
            # we add it back because there might be some information we are missing
            next_tiles.append((i,j))

        
        




