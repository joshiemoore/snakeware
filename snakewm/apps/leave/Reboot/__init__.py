from .confirm import RebootConfirmationDialog


def load(manager, params):
    """Launch reboot confirmation dialog"""
    pos = (100, 100)

    if params and len(params) > 0:
        pos = params[0]

    RebootConfirmationDialog(pos, manager)
