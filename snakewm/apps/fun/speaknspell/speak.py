import re
import threading

import pygame
import pygame_gui
from pygame_gui.elements import UITextBox, UITextEntryLine, UIWindow
import pyttsx3


class SpeakSpell(UIWindow):
    speakthrd = None

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (400, 200)),
            manager=manager,
            window_display_title="speaknspell",
            object_id="#speaknspell",
            resizable=True,
        )

        self.box = UITextBox(
            "",
            relative_rect=pygame.Rect(0, 0, 368, 100),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        self.input = UITextEntryLine(
            relative_rect=pygame.Rect(0, -35, 368, 30),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.speakthrd = None

        self.speak("Hello, thank you for using snakeware!")
        self.input.focus()

        # history attributes
        self.histsize = 100
        self.histindex = -1
        self.history = ["Hello, thank you for using snakeware!"]
        self.cached_command = ""

    def speak(self, text):
        if self.speakthrd is not None and self.speakthrd.is_alive():
            return

        if text == "":
            return

        text = re.sub(r"(\\r)?\\n", "<br>", text)
        spoken = re.sub(r"<(.*?)>", "", text)
        self.engine.say(spoken)
        self.speakthrd = threading.Thread(target=self.engine.runAndWait, args=())
        self.speakthrd.start()
        self.box.html_text = text
        self.box.rebuild()
        self.input.set_text("")

    def cache_command(self):
        self.cached_command = self.input.get_text()

    def flush_command_cache(self):
        self.cached_command = ""

    def set_histindex(self, increment):
        try:
            # self.history[self.histindex + increment]
            self.histindex += increment
        except IndexError:
            pass
        return self.histindex

    def set_from_history(self):
        if self.histindex > -1:
            self.input.set_text(self.history[self.histindex])
        else:
            self.input.set_text(self.cached_command)
        self.input.edit_position = len(self.input.get_text())

    def add_to_history(self, text):
        self.history = [text] + self.history
        if len(self.history) > self.histsize:
            del self.history[-1]

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.USEREVENT and event.ui_element == self.input:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                text = self.input.get_text()
                self.add_to_history(text)
                self.histindex = -1
                self.flush_command_cache()
                self.speak(text)
        elif event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN):
            increment = 1 if event.key == pygame.K_UP else -1
            if self.histindex == -1:
                self.cache_command()
            self.set_histindex(increment)
            self.set_from_history()
