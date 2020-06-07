from .dazzler import Snazzler


def load(manager, params):
    """
    Create and launch a new instance of Snazzler.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Snazzler(pos, manager)
