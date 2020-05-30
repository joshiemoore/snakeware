from .phyle import PhyleManager


def load(manager, params):
    """
    Create an launch a new instance of PhyleManager.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    PhyleManager(pos, manager)
