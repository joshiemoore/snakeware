"""Music player"""

import glob
import os

import pygame
import pygame_gui

from .mixer import Mixer


class MusicPlayer(pygame_gui.elements.UIWindow):
    """Music Player"""

    DIMS = (400, 250)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="MusicPlayer",
            object_id="#musicplayer",
        )

        # Create mixer
        self.mixer = Mixer()
        # Load list of musics
        app_path = os.path.dirname(os.path.abspath(__file__))
        self.musics_path = app_path + "/musics"
        self.musics = glob.glob(self.musics_path + "/*.ogg")
        self.musics_dict = dict(
            (music_path.split("/")[-1], music_path) for music_path in self.musics
        )

        self.isPaused = False

        btns_names = ["play", "pause", "stop", "+", "-"]
        # Button dimensions
        self.BSIZE = (self.DIMS[0] / len(btns_names), 30)
        # Init buttons
        for i, btn in enumerate(btns_names):
            self.play_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    # Calculate button width by dividing width of window by number of buttons
                    (i % len(btns_names) * self.BSIZE[0], self.DIMS[1] - self.BSIZE[1]),
                    self.BSIZE,
                ),
                text=btn.upper(),
                manager=manager,
                container=self,
                object_id="#op-" + btn + "btn",
            )

        # Add list of musics
        self.music_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(
                (0, 0), (self.DIMS[0], self.DIMS[1] - self.BSIZE[1])
            ),
            manager=manager,
            container=self,
            object_id="#op-musiclist",
            item_list=list(self.musics_dict.keys()),
        )

    def process_event(self, event):
        """Process event"""

        super().process_event(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#musicplayer.#op-playbtn":
                    selected_music = self.music_list.get_single_selection()
                    # Check if some music was selected
                    if selected_music is None:
                        music_path = next(iter(self.musics_dict.values()))
                    else:
                        music_path = self.musics_dict[selected_music]
                    # If the music is paused, resume music. Else load and play
                    if self.isPaused:
                        self.mixer.resume()
                        self.isPaused = False
                    else:
                        self.mixer.load(music_path)
                        self.mixer.play()
                elif event.ui_object_id == "#musicplayer.#op-pausebtn":
                    # Pause button
                    self.mixer.pause()
                    self.isPaused = True
                elif event.ui_object_id == "#musicplayer.#op-stopbtn":
                    # Stop button
                    self.mixer.stop()
                elif event.ui_object_id == "#musicplayer.#op-+btn":
                    # Increase volume
                    volume = min((self.mixer.get_volume() + 0.1), 1.0)
                    self.mixer.set_volume(value=volume)
                elif event.ui_object_id == "#musicplayer.#op--btn":
                    # Decrease volume
                    volume = max((self.mixer.get_volume() - 0.1), 0.0)
                    self.mixer.set_volume(value=volume)
                return True

    def update(self, delta):
        """Update"""

        super().update(delta)

    def kill(self):
        """Kill"""

        self.mixer.stop()
        super().kill()
