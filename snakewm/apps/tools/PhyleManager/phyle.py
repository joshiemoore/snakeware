from pathlib import Path
import pygame
import pygame_gui


class PhyleManager(pygame_gui.windows.UIFileDialog):
    """
    For now this app hijacks the file dialog,
    to provide a simple file explorer.
    """

    def __init__(self, pos, manager):
        super().__init__(
            rect=pygame.Rect(0, 0, 600, 400),
            manager=manager,
            window_title='PhyleManager',
        )

        self.ok_button.kill()
        self.cancel_button.kill()

    def _change_directory_path(self, new_directory_file_path: Path):
        if new_directory_file_path.exists():
            if new_directory_file_path.is_file():
                pass  # open with 'default' app
            else:
                super()._change_directory_path(new_directory_file_path)

    def _process_ok_cancel_events(self, event):
        pass  # would kill()
