import pygame
import pygame_gui

import datetime


class Stopwatch(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 300)),
            manager=manager,
            window_display_title="stopwatch",
            object_id="#stopwatch",
            resizable=True,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(1, 1, 199, 299),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        button_layout_rect = pygame.Rect(0, 0, 100,50)
        button_layout_rect.topright = (-1,-1)
        self.button = pygame_gui.elements.UIButton(
            relative_rect=button_layout_rect,
            anchors={"left" : "right",
                     "right" : "right",
                     "top" : "top",
                     "bottom" : "top"},
            text="s",
            container=self,
            manager=manager,
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
