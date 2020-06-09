import sys
import traceback

from io import StringIO

import pygame
import pygame_gui

from pygame_gui.elements import UITextBox


class SnakeTerm(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (400, 300)),
            manager,
            window_display_title="snaketerm",
            object_id="#snaketerm",
            resizable=True,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 0, 368, 200),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        self.input = pygame_gui.elements.UITextEntryLine(
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

        self.input.focus()

        # history attributes
        self.histsize = 100
        self.histindex = -1
        self.history = list()
        self.cached_command = str()

        # jump attributes
        self.jump_chars = (" ", "-", "_", "/")

        # TODO: load this from a file so users can configure
        self.hotkeys = {
            "ctrl": {
                "l": self.clear_text,
                "left": self.jump_left,
                "right": self.jump_right,
                "backspace": self.jump_backspace,
            }
        }

    def set_text(self, text):
        self.textbox.html_text = text.replace("\n", "<br>")
        self.textbox.rebuild()

    def clear_text(self):
        self.set_text(str())

    def jump_left(self):
        command = self.input.get_text()
        ep = self.input.edit_position
        while ep > 0 and command[ep - 1] not in self.jump_chars:
            ep -= 1
        self.input.edit_position = ep

    def jump_right(self):
        command = self.input.get_text()
        ep = self.input.edit_position
        while ep < len(command) and command[ep] not in self.jump_chars:
            ep += 1
        self.input.edit_position = ep

    def jump_backspace(self):
        command = self.input.get_text()
        ep = to_pos = self.input.edit_position
        while ep > 0 and command[ep - 1] not in self.jump_chars:
            ep -= 1
        self.input.set_text(command[:ep] + command[to_pos:])
        self.input.edit_position = ep

    def append_text(self, text, is_command=False):
        if is_command:
            self.textbox.html_text = self.textbox.html_text + ">>> " + text.replace("\n", "<br>") + "<br>" 
        else:
            self.textbox.html_text = self.textbox.html_text + text.replace("\n", "<br>")
        self.textbox.rebuild()
        if self.textbox.scroll_bar is not None:
            self.textbox.scroll_bar.scroll_position = (
                len(self.textbox.html_text.split("<br>")) * 5
            )
            self.textbox.scroll_bar.scroll_wheel_down = True

    def add_to_history(self, command):
        self.history = [command] + self.history
        if len(self.history) > self.histsize:
            del self.history[-1]

    def set_from_history(self):
        if self.histindex > -1:
            self.input.set_text(self.history[self.histindex])
        else:
            self.input.set_text(self.cached_command)
        self.input.edit_position = len(self.input.get_text())

    def set_histindex(self, increment):
        try:
            self.history[self.histindex + increment]
            self.histindex += increment
        except IndexError:
            return self.histindex
        return self.histindex

    def cache_command(self):
        self.cached_command = self.input.get_text()

    def flush_command_cache(self):
        self.cached_command = str()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            _stdout = sys.stdout
            sys.stdout = tout = StringIO()

            input_command = self.input.get_text()
            try:
                code = compile(input_command, "snaketerm_code", "exec")
                exec(code, globals())
            except Exception:
                e_type, e_val, e_traceback = sys.exc_info()
                print("Traceback (most recent call last):")
                traceback.print_tb(e_traceback, None, tout)
                print(e_type, e_val)

            sys.stdout = _stdout
            result = tout.getvalue()
            self.append_text(input_command, is_command=True)
            self.append_text(result)
            self.add_to_history(input_command)
            self.histindex = -1
            self.flush_command_cache()
            self.input.set_text(str())

        # ctrl hotkeys
        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
            if event.type == pygame.KEYUP:
                name = pygame.key.name(event.key)
                callback = self.hotkeys["ctrl"].get(name)
                if callback and callable(callback):
                    self.hotkeys["ctrl"][name]()

        # other special keys (history, etc)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                increment = 1 if event.key == pygame.K_UP else -1
                if self.histindex == -1:
                    self.cache_command()
                self.set_histindex(increment)
                self.set_from_history()
