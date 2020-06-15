from .help import Help


def load(manager, params):
    """
    Create and launch a new instance of Help.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Help(pos, manager)
