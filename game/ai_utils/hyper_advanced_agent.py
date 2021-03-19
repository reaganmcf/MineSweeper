from .advanced_agent import start_outside


def start(board: Board, agent: Agent, use_stepping: bool = False, lock_boolean=None):
    start_outside(board, agent, use_stepping, lock_boolean)
