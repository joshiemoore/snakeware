"""Background color"""

import pygame
from pygame_gui.windows import UIColourPickerDialog


def load(manager, params):
    """Launch a Colour Picker dialog to change the desktop background color."""

    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    UIColourPickerDialog(
        rect=pygame.Rect(pos, (600, 400)),
        manager=manager,
        window_title="Set Background Color",
        object_id="#desktop_colour_picker",
    )
