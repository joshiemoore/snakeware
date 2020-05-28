from .pongwindow import PongWindow

def load(manager, params):
    """
    Create Pong game and add it to the UI manager.
    params[0] should be the desired position. A default
    position will be used if a pos is not provided.
    """
    # default position
    pos = (50, 50)

    if params is not None and len(params) > 0:
        pos = params[0]

    PongWindow(pos, manager)
