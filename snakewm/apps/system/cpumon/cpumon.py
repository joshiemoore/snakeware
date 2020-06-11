# CPU usage monitor

import time
import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

try:
    import psutil
except ImportError:
    psutil = None
    from .cpuproc import cpuproc

BLUE = 68, 174, 220
GRAY = 76, 80, 82


class SnakeMon(pygame_gui.elements.UIWindow):
    DIMS = (200, 100)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="cpumon",
            object_id="#cpumonterm",
            resizable=False,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.cpu = pygame.Surface(self.DIMS)
        self.cpu.fill(GRAY)
        self.last_time = 0

    def process_event(self, event):
        super().process_event(event)

    def update(self, delta):
        super().update(delta)
        # limit frame rate to 4 FPS
        if time.time() - self.last_time > 0.25:
            self.draw_cpu()
            self.last_time = time.time()
        self.dsurf.image.blit(self.cpu, (0, 0))

    def draw_cpu(self):
        if psutil:
            cpu_perc = int(psutil.cpu_percent(interval=None))
        else:
            cpu_perc = cpuproc()
        self.cpu.scroll(dx=-1)
        pygame.draw.line(
            self.cpu,
            GRAY,
            ((self.DIMS[0] - 1), self.DIMS[1] - 1),
            ((self.DIMS[0] - 1), 0),
            1,
        )
        pygame.draw.line(
            self.cpu,
            BLUE,
            ((self.DIMS[0] - 1), self.DIMS[1] - 1),
            ((self.DIMS[0] - 1), self.DIMS[1] - cpu_perc),
            1,
        )
