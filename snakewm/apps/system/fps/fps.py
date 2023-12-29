# FPS counter for Snakeware

import statistics
import time

import pygame
from pygame_gui.elements import UITextBox, UIWindow


MAXSAMP = 300


class SnakeFPS(UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (370, 100)),
            manager=manager,
            window_display_title="fps",
            object_id="#fps",
            resizable=False,
        )

        self.textbox = UITextBox(
            "",
            relative_rect=pygame.Rect(0, 1, 338, 40),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        self.last = 0
        self.samp = []

    def process_event(self, event):
        super().process_event(event)

    def update(self, time_delta):
        super().update(time_delta)

        fps = 1 / (time.time() - self.last)
        self.samp.append(fps)
        if len(self.samp) > MAXSAMP:
            self.samp = self.samp[-MAXSAMP:]
        self.last = time.time()
        self.set_text(
            "FPS: %3u  AVG: %3u  MIN: %3u  MAX:  %3u"
            % (fps, statistics.mean(self.samp), min(self.samp), max(self.samp))
        )

    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()
