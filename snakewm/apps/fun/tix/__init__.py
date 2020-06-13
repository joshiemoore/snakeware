from .tix import TIX


def load(manager, params):
    """
    Create and launch a new instance of TIX.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    TIX(pos, manager)
