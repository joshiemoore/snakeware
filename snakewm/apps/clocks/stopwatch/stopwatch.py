import pygame
import pygame_gui

import time


class Stopwatch(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (232, 310)),
            manager=manager,
            window_display_title="stopwatch",
            object_id="#stopwatch",
            resizable=False,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "0 : 0 : 0 : 0",
            relative_rect=pygame.Rect(0, 3, 200, 35),
            manager=manager,
            container=self,
        )

        button_layout_rect = pygame.Rect(0, 40, 100, 35)
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=button_layout_rect,
            text="start/pause",
            container=self,
            manager=manager,
            object_id="#start_button",
        )

        button2_layout_rect = pygame.Rect(100, 40, 100, 35)
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=button2_layout_rect,
            text="reset",
            container=self,
            manager=manager,
            object_id="#reset_button",
        )
        button3_layout_rect = pygame.Rect(0, 75, 200, 35)
        self.save_time = pygame_gui.elements.UIButton(
            relative_rect=button3_layout_rect,
            text="save time",
            container=self,
            manager=manager,
            object_id="#flag_button",
        )

        self.time_box = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 110, 200, 150),
            manager=manager,
            container=self,
        )

        self.arr = []
        self.saver = False
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
                elif event.ui_element == self.save_time:
                    self.saver = True

    def update(self, time_delta):
        super().update(time_delta)
        if self.currently_counting:
            self.time_counter += time_delta
        mili = int(self.time_counter * 100 % 100)
        secs = int(self.time_counter % 60)
        mins = int((self.time_counter % (60**2)) // 60)
        hours = int(self.time_counter // (60**2))

        counter_str = f"     {str(hours)} : {str(mins)} : {str(secs)} : {str(mili)}"
        self.set_text(counter_str)

    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()
        if self.saver:
            self.arr.append(text.replace("     ", "  "))
            self.time_box.html_text = "<br>".join(self.arr)
            self.time_box.rebuild()
            self.saver = False

    def reset_time(self):
        self.time_counter = 0
        self.currently_counting = False
        self.update(0)
        self.time_box.html_text = ""
        self.time_box.rebuild()
        self.arr.clear()
