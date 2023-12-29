"""
App menu panel containing a list of all apps or subdirectories in the
current directory.
"""

import pygame
from pygame.event import Event
import pygame_gui
from pygame_gui.elements import UIButton, UIPanel

# panel draw layer
PANEL_LAYER = 10

# button dimensions
BUTTON_DIMS = (200, 25)


class AppMenuPanel(UIPanel):
    """App menu panel"""

    manager = None
    pos = None
    path = None

    # the elements field is a dict object containing the structure of
    # the current directory and all subdirectories. If a value is None,
    # that means its corresponding key represents an app.
    elements = None

    # child panel created when a directory button is hovered
    child = None

    def __init__(self, manager, pos, path, elements, loadfunc):
        """
        manager - UIManager to manage this panel
        pos - position indices to start drawing this panel at
        path - the directory this panel represents
        elements - list of elements in this directory
        """
        super().__init__(
            pygame.Rect(
                (pos[0] * BUTTON_DIMS[0], pos[1] * BUTTON_DIMS[1]),
                (BUTTON_DIMS[0] + 5, BUTTON_DIMS[1] * len(elements.keys()) + 5),
            ),
            starting_layer_height=PANEL_LAYER,
            manager=manager,
        )
        self.pos = pos
        self.path = path
        self.elements = elements
        self.loadfunc = loadfunc

        # sorted list of element keys to generate the panel from
        self.element_keys = sorted(list(elements.keys()))

        # generate buttons
        for i in range(len(self.element_keys)):
            UIButton(
                pygame.Rect((0, i * BUTTON_DIMS[1]), BUTTON_DIMS),
                text=self.element_keys[i],
                manager=manager,
                container=self,
                object_id="menu-" + self.path.replace(".", "-"),
            )

    def process_event(self, event: Event) -> bool:
        """Process event
        Overrides method in UIPanel.

        :return: Should return True if this element consumes this event.
        """

        if event.type != pygame.USEREVENT:
            return False

        if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == (
            "panel.menu-" + self.path.replace(".", "-")
        ):
            # open clicked app
            uitext = event.ui_element.text

            if self.elements[uitext] == None:
                self.loadfunc(self.path + "." + uitext)

        if (
            event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED
            and event.ui_object_id == ("panel.menu-" + self.path.replace(".", "-"))
        ):
            uitext = event.ui_element.text

            if self.elements[uitext] != None:
                # first destroy the active child panel
                if self.child is not None:
                    self.child.destroy()

                # next open a new child panel
                self.child = AppMenuPanel(
                    self.ui_manager,
                    (self.pos[0] + 1, self.pos[1] + self.element_keys.index(uitext)),
                    self.path + "." + uitext,
                    self.elements[uitext],
                    self.loadfunc,
                )

        return False

    def destroy(self):
        """Recursively kill this panel and all child panels."""

        if self.child is not None:
            self.child.destroy()
            self.child = None
        self.kill()
