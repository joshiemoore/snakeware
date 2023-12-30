"""FPS counter for Snakeware"""

import statistics
import time

import pygame
from pygame_gui.elements import UITextBox, UIWindow

MAXSAMP = 300


class SnakeFPS(UIWindow):
    """Snake FPS"""

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
        """Process event"""

        super().process_event(event)

    def update(self, time_delta):
        """Update"""

        super().update(time_delta)

        fps = 1 / (time.time() - self.last)
        self.samp.append(fps)
        if len(self.samp) > MAXSAMP:
            self.samp = self.samp[-MAXSAMP:]
        self.last = time.time()

        average = statistics.mean(self.samp)
        minimum = min(self.samp)
        maximum = max(self.samp)

        self.set_text(f"FPS: {fps:>3}  AVG: {average:>3}  MIN: {minimum:>3}  MAX:  {maximum:>3}")

    def set_text(self, text):
        """Set text"""

        self.textbox.html_text = text
        self.textbox.rebuild()
