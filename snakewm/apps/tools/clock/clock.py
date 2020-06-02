import pygame
import pygame_gui

import datetime


class SnakeClock(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (195, 100)),
            manager=manager,
            window_display_title="clock",
            object_id="#clockterm",
            resizable=True,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 1, 163, 40),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

    def process_event(self, event):
        super().process_event(event)

    def update(self, time_delta):
        super().update(time_delta)

        dt = datetime.datetime.now()
        # %X formatted clock, %x formatted date
        current_time = dt.strftime("%X  %x")

        self.set_text(current_time)

    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()
