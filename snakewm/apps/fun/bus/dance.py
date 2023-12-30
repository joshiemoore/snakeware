"""BusDance"""

import os

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements.ui_image import UIImage


class BusDance(UIWindow):
    """BusDance"""

    DIMS = (320, 240)

    FRAMES = []
    FRAMES_LEN = 0
    FRAME_INDEX = 0

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="BusDance",
            object_id="#busdance",
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )

        app_path = os.path.dirname(os.path.abspath(__file__))
        frames_path = app_path + "/frames/"

        for x in range(180):
            # load each frame from the GIF into the frame list
            frame = pygame.image.load(frames_path + "frame-" + str(x) + ".png")
            frame = pygame.transform.scale(frame, self.DIMS)

            # add each frame twice for half speed
            self.FRAMES.append(frame)
            self.FRAMES.append(frame)

        self.FRAMES_LEN = len(self.FRAMES)

        # \TODO find fun, groovin, royalty-free tune to play
        # load and play the song
        # pygame.mixer.init()
        # pygame.mixer.music.load(app_path + "/party.ogg")
        # pygame.mixer.music.play(loops=-1)

    def update(self, time_delta: float) -> None:
        """Update"""

        super().update(time_delta)
        self.dsurf.image.blit(self.FRAMES[self.FRAME_INDEX], (0, 0))
        self.FRAME_INDEX = (self.FRAME_INDEX + 1) % self.FRAMES_LEN

    # def kill(self):
    #    pygame.mixer.music.stop()
    #    super().kill()
