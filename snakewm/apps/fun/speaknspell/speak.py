import threading
import re

import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.elements import UITextEntryLine

import pyttsx3


class SpeakSpell(pygame_gui.elements.UIWindow):
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

    def speak(self, text):
        if self.speakthrd is not None and self.speakthrd.is_alive():
            return

        if text == "":
            return

        text = text.replace("\n", "<br>")

        spoken = re.sub(r"<(.*?)>", "", text)
        self.engine.say(spoken)
        self.speakthrd = threading.Thread(target=self.engine.runAndWait, args=())
        self.speakthrd.start()
        self.box.html_text = text
        self.box.rebuild()
        self.input.set_text("")

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.USEREVENT and event.ui_element == self.input:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.speak(self.input.get_text())
