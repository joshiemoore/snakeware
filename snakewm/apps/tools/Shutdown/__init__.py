from .confirm import ShutdownConfirmationDialog


def load(manager, params):
    """Launch shutdown confirmation manager"""
    pos = (100, 100)

    if params and len(params) > 0:
        pos = params[0]

    ShutdownConfirmationDialog(pos, manager)
