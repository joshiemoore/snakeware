"""CPU usage monitor"""

import time

import pygame
from pygame.event import Event
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

from .ramproc import ramproc, ramproc2

try:
    import psutil
except ImportError:
    psutil = None
    from .cpuproc import cpuproc, cpuproc2

BLUE = 68, 174, 220
GRAY = 76, 80, 82
RED = 255, 0, 0


class SnakeMon(pygame_gui.elements.UIWindow):
    """Snake Monitor"""

    DIMS = (200, 100)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 230, self.DIMS[1] + 110)),
            manager=manager,
            window_display_title="Sysmon",
            object_id="#sysmonterm",
            resizable=False,
        )

        self.textbox_ram = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(200, 100, 200, 100),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        self.textbox_cpu = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 100, 200, 100),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )

        self.surf_cpu = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.surf_ram = UIImage(
            pygame.Rect((200, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.cpu = pygame.Surface(self.DIMS)
        self.cpu.fill(GRAY)
        self.ram = pygame.Surface(self.DIMS)
        self.ram.fill(GRAY)
        self.last_time = 0

    def process_event(self, event: Event) -> bool:
        """Process event"""

        return super().process_event(event)

    def update(self, time_delta: float) -> None:
        """Update"""

        super().update(time_delta)
        # limit frame rate to 4 FPS
        if time.time() - self.last_time > 0.25:
            self.draw_cpu()
            self.draw_ram()
            self.last_time = time.time()
        self.surf_cpu.image.blit(self.cpu, (0, 0))
        self.surf_ram.image.blit(self.ram, (0, 0))

        self.set_text(f"{ramproc2()}")
        if psutil:
            self.set_text2(f"{str(psutil.cpu_percent(interval=None))}/100")
        else:
            self.set_text2(f"{cpuproc2()}")

    def draw_cpu(self):
        """Draw CPU"""

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

    def draw_ram(self):
        """Draw RAM"""

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
            RED,
            ((self.DIMS[0] - 1), self.DIMS[1] - 1),
            ((self.DIMS[0] - 1), self.DIMS[1] - ram_perc),
            1,
        )

    def set_text(self, text):
        """Set text"""

        self.textbox_ram.html_text = text
        self.textbox_ram.rebuild()

    def set_text2(self, text):
        """Set text"""

        self.textbox_cpu.html_text = text
        self.textbox_cpu.rebuild()
