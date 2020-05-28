import sys
import traceback

from io import StringIO

import pygame
import pygame_gui

from pygame_gui.elements import UITextBox

class SnakeTerm(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (400,300)),
            manager,
            window_display_title='snaketerm',
            object_id='#snaketerm',
            resizable=True
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 0, 368, 200),
            manager=manager,
            container=self,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        self.input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(0, -35, 368, 30),
            manager=manager,
            container=self,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'bottom',
                'bottom': 'bottom'
            }
        )

    def set_text(self, text):
        self.textbox.html_text = text.replace('\n', '<br>')
        self.textbox.rebuild()

    def append_text(self, text):
        self.textbox.html_text = self.textbox.html_text + text.replace('\n', '<br>')
        self.textbox.rebuild()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            _stdout = sys.stdout
            sys.stdout = tout = StringIO()

            try:
                code = compile(self.input.get_text(), 'snaketerm_code', 'exec')
                exec(code, globals())
            except Exception:
                e_type,e_val,e_traceback = sys.exc_info()
                print('Traceback (most recent call last):')
                traceback.print_tb(e_traceback, None, tout)
                print(e_type, e_val)

            sys.stdout = _stdout
            result = tout.getvalue()
            self.append_text(result)
            self.input.set_text('')
