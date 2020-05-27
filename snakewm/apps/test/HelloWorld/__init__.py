import pygame
import pygame_gui

def load(manager, params):
    """
    An example implementation of the load() function called by the snakewm
    loadapp() function.
    """
    pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((10, 10), (300, 160)),
        window_title="snakeware",
        html_message="Hello World!",
        manager=manager
    )
