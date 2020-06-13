from .berlin import Berlin


def load(manager, params):
    """
    Create and launch a new instance of Berlin.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Berlin(pos, manager)
