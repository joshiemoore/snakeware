from .cell import Cell


def load(manager, params):
    """
    Create and launch a new instance of Cell.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Cell(pos, manager)
