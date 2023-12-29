"""Snake terminal"""

from .term import SnakeTerm


def load(manager, params):
    """
    Create and launch a new instance of SnakeTerm.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    SnakeTerm(pos, manager)
