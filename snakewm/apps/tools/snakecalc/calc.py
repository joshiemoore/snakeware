"""Calculator"""

import pygame
from pygame.event import Event
import pygame_gui


class SnakeCalc(pygame_gui.elements.UIWindow):
    """Snake calculator"""

    # operations to be converted to buttons
    OPS = "789+" + "456-" + "123*" + "p0=/" + "C<x%"

    # button dimensions
    BSIZE = (67, 75)

    # user input
    USERCALC = ""

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 475)),
            manager=manager,
            window_display_title="snakecalc",
            object_id="#snaketerm",
            resizable=False,
        )

        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 1, 268, 40),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        # generate calculator buttons
        for i, op in enumerate(self.OPS):

            if op == "x":
                # skip placeholder ops
                continue

            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (i % 4 * self.BSIZE[0], 40 + int(i / 4) * self.BSIZE[1]), self.BSIZE
                ),
                text="." if op == "p" else op,
                manager=manager,
                container=self,
                object_id="#op-" + op,
            )

    def process_event(self, event: Event) -> bool:
        """Process event"""

        super().process_event(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.input_op(event.ui_object_id[-1])
                return True

        # TODO: should return bool in all cases

    def set_text(self, text):
        """Set text"""

        self.textbox.html_text = text
        self.textbox.rebuild()

    def append_text(self, text):
        """Append text"""

        self.textbox.html_text = self.textbox.html_text + text
        self.textbox.rebuild()

    def calculate(self, expression):
        """Perform the actual calculation based on user input."""

        try:
            result = str(eval(expression))
        except Exception:
            result = "Error"

        self.set_text(result)

    def input_op(self, op):
        """Called to append user input ops to the existing input."""

        if op in self.OPS:
            if op == "=":
                # perform the calculation
                self.calculate(self.textbox.html_text)
            elif op == "C":
                self.set_text("")
            elif op == "p":
                self.append_text(".")
            elif op == "<":
                self.set_text(self.textbox.html_text[:-1])
            else:
                self.append_text(op)
