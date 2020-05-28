"""
App menu panel containing a list of all apps or subdirectories in the
current directory.
"""

import pygame
import pygame_gui

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

    # the elements field is a dict object containing the structure of
    # the current directory and all subdirectories. If a value is None,
    # that means its corresponding key is represents an app.
    elements = None

    # child panel created when a directory button is hovered
    child = None

    def __init__(self, manager, pos, path, elements):
        """
        manager - UIManager to manage this panel
        pos - position indices to start drawing this panel at
        path - the directory this panel represents
        elements - list of elements in this directory
        """
        super().__init__(
            pygame.Rect(
                (
                    pos[0] * BUTTON_DIMS[0],
                    pos[1] * BUTTON_DIMS[1]
                ),
                (
                    BUTTON_DIMS[0] + 5,
                    BUTTON_DIMS[1] * len(elements.keys()) + 5
                )
            ),
            starting_layer_height=PANEL_LAYER,
            manager=manager
        )
        self.pos = pos
        self.path = path
        self.elements = elements

        # generate buttons
        ekeys = list(elements.keys())
        for i in range(len(ekeys)):
            UIButton(
                pygame.Rect(
                    (0, i * BUTTON_DIMS[1]),
                    BUTTON_DIMS
                ),
                text=ekeys[i],
                manager=manager,
                container=self,
                object_id = 'menu-' + self.path.replace('.', '-')
            )

    def process_event(self, event):
        if event.type != pygame.USEREVENT:
            return

        if event.user_type == pygame_gui.UI_BUTTON_PRESSED and\
            event.ui_object_id == ('panel.menu-' + self.path.replace('.', '-')):
            # open clicked app
            uitext = event.ui_element.text

            if self.elements[uitext] == None:
                #\TODO open app
                print("opening app: " + self.path + '.' + uitext)

        if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED and\
            event.ui_object_id == ('panel.menu-' + self.path.replace('.', '-')):
            uitext = event.ui_element.text

            if self.elements[uitext] != None:
                # first destroy the active child panel
                if self.child is not None:
                    self.child.destroy()

                # next open a new child panel
                self.child = AppMenuPanel(
                    self.ui_manager,
                    (
                        self.pos[0] + 1,
                        list(self.elements.keys()).index(uitext)
                    ),
                    self.path + '.' + uitext,
                    self.elements[uitext]
                )

    def destroy(self):
        """
        Recursively kill this panel and all child panels.
        """
        if self.child is not None:
            self.child.destroy()
            self.child = None
        self.kill()
