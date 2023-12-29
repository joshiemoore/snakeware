"""Maze 3D"""

from .maze3dwindow import Maze3DWindow


def load(manager, params):
    """Load"""

    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Maze3DWindow(pos, manager)
