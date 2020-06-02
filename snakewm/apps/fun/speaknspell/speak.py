import threading

import pygame
import pygame_gui

from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextEntryLine

import pyttsx3

class SpeakSpell(pygame_gui.elements.UIWindow):
    speakthrd = None

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (400,128)),
            manager=manager,
            window_display_title='speaknspell',
            object_id='#speaknspell'
        )

        self.label = UILabel(
            relative_rect=pygame.Rect(-20, 10, 400, 20),
            text='',
            manager=manager,
            container=self
        )

        self.input = UITextEntryLine(
            relative_rect=pygame.Rect(0, 40, 368, 30),
            manager=manager,
            container=self
        )

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.speakthrd = None

        self.speak('Hello, thank you for using snakeware!')

    def speak(self, text):
        if self.speakthrd is not None and self.speakthrd.is_alive():
            return

        if text == '':
            return

        self.engine.say(text)
        self.speakthrd = threading.Thread(target=self.engine.runAndWait, args=())
        self.speakthrd.start()
        self.label.set_text(text)
        self.input.set_text('')

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.USEREVENT and event.ui_element == self.input:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.speak(self.input.get_text())
