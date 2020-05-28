import pygame
import pygame_gui

def load(manager, params):
    """
    Launch a Colour Picker dialog to change the desktop background color.
    """

    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    pygame_gui.windows.UIColourPickerDialog(
        rect=pygame.Rect(pos, (420, 400)),
        manager=manager,
        window_title='Set Background Color',
        object_id='#desktop_colour_picker'
    )
