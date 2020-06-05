import pygame
import pygame_gui


class ProgrammingCalc(pygame_gui.elements.UIWindow):
    # operations to be converted to buttons
    OPS = "789B" "456H" "123C" "<"

    # button dimensions
    BSIZE = (67, 75)

    # user input
    USERCALC = ""

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 400)),
            manager=manager,
            window_display_title="Programming Calc",
            object_id="#snaketerm",
            resizable=True,
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
        for i in range(len(self.OPS)):
            op = self.OPS[i]
            if op == "_":
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

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.input_op(event.ui_object_id[-1])
                return True

    def set_text(self, text):
        self.textbox.html_text = text
        self.textbox.rebuild()

    def append_text(self, text):
        self.textbox.html_text = self.textbox.html_text + text
        self.textbox.rebuild()


    def calcBin(self, expression):
        """
        Converts integer into binary
        """
        result = ""

        try:
            result = str(int(bin(int(expression)).replace("0b", "")))
        except Exception:
            result = "Error"

        self.set_text(result)

    def calcHex(self, expression):
        """Converts integer into Hex"""
        result = ""

        try:
            result = str(hex(int(expression)))
        except Exception:
            result = "Error"

        self.set_text(result)


    def input_op(self, op):
        """
        Called to append user input ops to the existing input.
        """
        if op in self.OPS:
            if op == "B":
                self.calcBin(self.textbox.html_text)
            elif op == "H":
                self.calcHex(self.textbox.html_text)
            elif op == "C":
                self.set_text("")
            elif op == "<":
                self.set_text(self.textbox.html_text[:-1])
            else:
                self.append_text(op)
