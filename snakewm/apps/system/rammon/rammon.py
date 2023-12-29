# RAM usage monitor

import time

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements.ui_image import UIImage

from .ramproc import ramproc


BLUE = 68, 174, 220
GRAY = 76, 80, 82


class SnakeMon(UIWindow):
    DIMS = (200, 100)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="rammon",
            object_id="#rammonterm",
            resizable=False,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.ram = pygame.Surface(self.DIMS)
        self.ram.fill(GRAY)
        self.last_time = 0

    def process_event(self, event):
        super().process_event(event)

    def update(self, delta):
        super().update(delta)
        # limit frame rate to 4 FPS
        if time.time() - self.last_time > 0.25:
            self.draw_ram()
            self.last_time = time.time()
        self.dsurf.image.blit(self.ram, (0, 0))

    def draw_ram(self):
        ram_perc = ramproc()
        self.ram.scroll(dx=-1)
        pygame.draw.line(
            self.ram,
            GRAY,
            ((self.DIMS[0] - 1), self.DIMS[1] - 1),
            ((self.DIMS[0] - 1), 0),
            1,
        )
        pygame.draw.line(
            self.ram,
            BLUE,
            ((self.DIMS[0] - 1), self.DIMS[1] - 1),
            ((self.DIMS[0] - 1), self.DIMS[1] - ram_perc),
            1,
        )
