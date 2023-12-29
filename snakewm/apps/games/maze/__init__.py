"""Maze"""

from .mazewindow import MazeWindow


def load(manager, params):
    """Load"""

    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    MazeWindow(pos, manager)
