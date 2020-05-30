import pygame
import pygame_gui

import time

class SnakeClock(pygame_gui.elements.UIWindow):

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 100)),
            manager=manager,
            window_display_title='clock',
            object_id='#clockterm',
            resizable=True
        )

        self.textbox = pygame_gui.elements.UITextBox(
            '',
            relative_rect=pygame.Rect(0, 1, 268, 40),
            manager=manager,
            container=self,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        

    def process_event(self, event):
        super().process_event(event)

    def update(self, time_delta):
        super().update(time_delta)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.set_text(current_time)

    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()