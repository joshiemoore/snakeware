import pygame
import pygame_gui
import os

def load(manager, params):
    """
    Launch a file dialog to change the desktop background.
    """

    # default position
    pos = (30, 30)

    if params is not None and len(params) > 0:
        pos = params[0]

    pygame_gui.windows.UIFileDialog(
        rect=pygame.Rect(pos, (600, 400)),
        manager=manager,
        window_title='Set Background Image',
        initial_file_path=os.path.dirname(os.path.realpath(__file__)),
        object_id='#background_picker'
    )
