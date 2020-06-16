import pygame
import pygame_gui

import time


class Stopwatch(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (362, 75)),
            manager=manager,
            window_display_title="stopwatch",
            object_id="#stopwatch",
            resizable=True,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "0 : 0 : 0",
            relative_rect=pygame.Rect(0, 3, 130, 35),
            manager=manager,
            container=self,
        )

        button_layout_rect = pygame.Rect(130, 3, 100, 35)
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=button_layout_rect,
            text="start/pause",
            container=self,
            manager=manager,
            object_id="#start_button",
        )

        button2_layout_rect = pygame.Rect(230, 3, 100, 35)
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=button2_layout_rect,
            text="reset",
            container=self,
            manager=manager,
            object_id="#reset_button",
        )

        self.time_counter = 0
        self.currently_counting = False

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.currently_counting = not self.currently_counting
                elif event.ui_element == self.reset_button:
                    self.reset_time()

    def update(self, time_delta):
        super().update(time_delta)
        if self.currently_counting:
            self.time_counter += time_delta
        secs = int(self.time_counter % 60)
        mins = int( (self.time_counter % (60**2)) // 60 )
        hours = int(self.time_counter // (60**2))

        counter_str = f"{str(hours)} : {str(mins)} : {str(secs)}"
        self.set_text(counter_str)
    
    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()

    def reset_time(self):
        self.time_counter = 0
        self.currently_counting = False
        self.update(0)