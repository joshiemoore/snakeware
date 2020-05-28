"""
App menu panel containing a list of all apps or subdirectories in the
current directory.
"""

import pygame

from pygame_gui.elements import UIPanel
from pygame_gui.elements import UIButton

# panel draw layer
PANEL_LAYER = 10

# button dimensions
BUTTON_DIMS = (200, 25)

class AppMenuPanel(UIPanel):
    manager = None
    pos = None
    path = None

    # the elements field contains a list of tuples, where each tuple
    # represents a single element the current directory:
    # (text, next)
    # where text is the text to display, and next is the directory this
    # element represents, or None if the element represents an app.
    elements = None

    def __init__(self, manager, pos, path, elements):
        """
        manager - UIManager to manage this panel
        pos - position indices to start drawing this panel at
        path - the directory this panel represents
        elements - list of elements in this directory
          \TODO replace elements with a dict structure representing the
          current directory
        """
        super().__init__(
            pygame.Rect(
                (
                    pos[0] * BUTTON_DIMS[0],
                    pos[1] * BUTTON_DIMS[1]
                ),
                (
                    BUTTON_DIMS[0] + 5,
                    BUTTON_DIMS[1] * len(elements) + 5
                )
            ),
            starting_layer_height=PANEL_LAYER,
            manager=manager
        )
        self.path = path
        self.elements = elements

        # generate buttons
        for i in range(len(elements)):
            UIButton(
                pygame.Rect(
                    (0, i * BUTTON_DIMS[1]),
                    BUTTON_DIMS
                ),
                text=elements[i][0],
                manager=manager,
                container=self
            )
