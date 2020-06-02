import pygame
import pygame_gui
import os


class ShutdownConfirmationDialog(pygame_gui.windows.UIConfirmationDialog):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (300, 160)),
            manager=manager,
            window_title="Shutdown?",
            action_long_desc="Are you sure you want to shut down the system?",
            action_short_name="Shut down",
            blocking=False,
            object_id="#shutdown",
        )

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            os.system("/sbin/poweroff -f")
            return True
        return False
