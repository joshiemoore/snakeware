from .pongwindow import PongWindow

def load(manager, params):
    """
    Create Pong game and add it to the UI manager.
    params[0] should be the desired size, if other than default.
    """
    default_size = (50, 50)

    if params is not None and len(params) > 0:
        # create PongWindow of user-specified size
        PongWindow(params[0], manager)
    else:
        # create PongWindow of default size
        PongWindow(default_size, manager)
    
