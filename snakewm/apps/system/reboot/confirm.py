import pygame
import pygame_gui
import os


class RebootConfirmationDialog(pygame_gui.windows.UIConfirmationDialog):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 160)),
            manager=manager,
            window_title="Reboot?",
            action_long_desc="Are you sure you want to reboot the system?",
            action_short_name="Reboot",
            blocking=False,
            object_id="#reboot"
        )

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            os.system("/sbin/reboot -f")
            return True
        return False
