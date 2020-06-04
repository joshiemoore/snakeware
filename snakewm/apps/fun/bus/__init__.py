from .dance import BusDance

def load(manager, params):
    """
    Create and launch a new instal of BusDance.
    """
    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    BusDance(pos, manager)
