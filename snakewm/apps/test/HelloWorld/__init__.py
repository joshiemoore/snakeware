import pygame
import pygame_gui


def load(manager, params):
    """
    An example implementation of the load() function called by the snakewm
    loadapp() function.
    """

    # default position
    pos = (10, 10)

    if params is not None and len(params) > 0:
        pos = params[0]

    pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect(pos, (300, 160)),
        window_title="snakeware",
        html_message="Hello World!",
        manager=manager,
    )
